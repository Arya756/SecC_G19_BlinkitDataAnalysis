#!/usr/bin/env python3
"""
ETL Pipeline (Corrected) — The Unplanned Basket.

Changes vs. the original `scripts/etl_pipeline.py`:
  1. `is_impulse_category` restricted to {Snacks, Beverages, Bakery} — Dairy and
     F&V removed. See audit fix #1 in 02_complete_walkthrough.md.
  2. `is_perishable` threshold tightened from 30 days to 14 days (audit fix #2).
  3. `is_small_pack` threshold set to ≤ 250 g (audit fix #3).
  4. Dead-code `fillna(median/mode)` removed — no nulls exist anywhere except
     `offer_type`, and that is handled explicitly (audit fix #4).
  5. Casing preserved on categorical columns so Tableau legends read
     "No Offer" not "no offer" (audit fix #5).
  6. `city_impulse_index` uses vectorised np.where for clarity (audit fix #11).

Run:
    python etl_pipeline_corrected.py

Expects raw file at ../data/raw/blinkit_dataset.csv
Writes:
  ../data/processed/cleaned.csv
  ../data/processed/final_dataset.csv
"""
import os
import sys
import numpy as np
import pandas as pd

BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_PATH   = os.path.join(BASE_DIR, "data", "raw", "blinkit_dataset.csv")
CLEAN_PATH = os.path.join(BASE_DIR, "data", "processed", "cleaned.csv")
FINAL_PATH = os.path.join(BASE_DIR, "data", "processed", "final_dataset.csv")

# ── Constants (single source of truth) ──────────────────────────────────────
IMPULSE_CATEGORIES = {"Snacks", "Beverages", "Bakery"}
SMALL_PACK_G       = 250    # ≤ 250 g  → small
PERISHABLE_DAYS    = 14     # ≤ 14 d   → daily-top-up
SCORE_WEIGHTS      = {"is_small_pack": 0.30,
                      "is_perishable": 0.25,
                      "is_impulse_category": 0.25,
                      "has_offer": 0.20}


def extract(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    print(f"[EXTRACT] {df.shape[0]:,} rows × {df.shape[1]} cols loaded from {path}")
    return df


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Only two real cleaning steps: recode offer_type nulls, parse dates."""
    before_nulls = df["offer_type"].isna().sum()
    df["offer_type"] = df["offer_type"].fillna("No Offer")
    print(f"[CLEAN]   offer_type nulls recoded → 'No Offer'  ({before_nulls:,} rows)")

    df["date_added"]  = pd.to_datetime(df["date_added"],  errors="coerce")
    df["expiry_date"] = pd.to_datetime(df["expiry_date"], errors="coerce")

    full_dupes = df.duplicated().sum()
    if full_dupes:
        df = df.drop_duplicates().reset_index(drop=True)
        print(f"[CLEAN]   dropped {full_dupes:,} duplicate rows")

    # Integrity pass
    checks = {
        "final_price ≤ price"          : bool((df["final_price"] <= df["price"] + 0.01).all()),
        "discount_pct ∈ [0,100]"       : bool(df["discount_pct"].between(0, 100).all()),
        "rating ∈ [0,5]"               : bool(df["rating"].between(0, 5).all()),
        "weight_g > 0"                 : bool((df["weight_g"] > 0).all()),
        "shelf_life_days > 0"          : bool((df["shelf_life_days"] > 0).all()),
        "sold_quantity ≥ 0"            : bool((df["sold_quantity"] >= 0).all()),
        "profit_margin_pct ∈ [0,100]"  : bool(df["profit_margin_pct"].between(0, 100).all()),
    }
    for k, v in checks.items():
        flag = "OK" if v else "FAIL"
        print(f"[CHECK]   {flag:4s}  {k}")
    if not all(checks.values()):
        sys.exit("[ABORT] Integrity checks failed.")
    return df


def engineer(df: pd.DataFrame) -> pd.DataFrame:
    # Monetary
    df["revenue"]         = df["final_price"] * df["sold_quantity"]
    df["gross_profit"]    = df["revenue"] * df["profit_margin_pct"] / 100
    df["price_per_100g"]  = df["final_price"] / df["weight_g"] * 100
    df["discount_amount"] = df["price"] - df["final_price"]

    # Flags
    df["is_discounted"]       = df["discount_pct"] > 0
    df["has_offer"]           = df["offer_type"].ne("No Offer")
    df["is_small_pack"]       = df["weight_g"] <= SMALL_PACK_G
    df["is_perishable"]       = df["shelf_life_days"] <= PERISHABLE_DAYS
    df["is_impulse_category"] = df["category"].isin(IMPULSE_CATEGORIES)
    df["is_delayed"]          = df["delivery_status"].eq("Delayed")
    df["stock_risk"]          = df["stock"] <= df["reorder_level"]

    # Weight bucket
    df["weight_bucket"] = np.where(df["weight_g"] <= SMALL_PACK_G, "small",
                          np.where(df["weight_g"] <= 700, "mid", "bulk"))

    # Flagship impulse score
    df["impulse_proxy_score"] = sum(
        w * df[f].astype(int) for f, w in SCORE_WEIGHTS.items()
    ).round(4)
    df["basket_type"] = np.where(df["impulse_proxy_score"] >= 0.6, "Impulse",
                        np.where(df["impulse_proxy_score"] <= 0.4, "Planned", "Mixed"))

    # Advanced
    cat_mean = df.groupby("category")["price_per_100g"].transform("mean")
    df["impulse_premium_pct"] = ((df["price_per_100g"] - cat_mean) / cat_mean * 100).round(2)

    city_mean   = df.groupby("city")["impulse_proxy_score"].transform("mean")
    global_mean = df["impulse_proxy_score"].mean()
    df["city_impulse_index"] = np.where(global_mean > 0, city_mean / global_mean, 1.0)

    # Temporal helpers
    df["year_added"]    = df["date_added"].dt.year
    df["month_added"]   = df["date_added"].dt.to_period("M").astype(str)
    df["quarter_added"] = df["date_added"].dt.to_period("Q").astype(str)

    print(f"[ENGINEER] score mean={df['impulse_proxy_score'].mean():.3f}  "
          f"basket={df['basket_type'].value_counts().to_dict()}")
    return df


def tableau_aggregate(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["cost_price"] = df["final_price"] * (1 - df["profit_margin_pct"] / 100)
    df["margin_inr"] = (df["final_price"] - df["cost_price"]) * df["sold_quantity"]

    agg = (df.groupby(["city", "category", "basket_type", "offer_type"])
             .agg(revenue=("revenue", "sum"),
                  margin =("margin_inr", "sum"),
                  avg_price=("final_price", "mean"),
                  total_qty=("sold_quantity", "sum"),
                  impulse_premium=("impulse_premium_pct", "mean"))
             .reset_index())

    agg["margin_pct"] = (agg["margin"] / agg["revenue"] * 100).round(2)
    base = (agg[agg["offer_type"] == "No Offer"]
            .groupby(["city", "category", "basket_type"])["total_qty"]
            .mean()
            .reset_index(name="base_qty"))
    agg = agg.merge(base, on=["city", "category", "basket_type"], how="left")
    agg["offer_lift"] = np.where(agg["base_qty"].fillna(0) > 0,
                                  agg["total_qty"] / agg["base_qty"], 1.0)

    tot = agg.groupby(["city", "category"])["revenue"].transform("sum")
    agg["impulse_pct"] = np.where(agg["basket_type"] == "Impulse",
                                   (agg["revenue"] / tot * 100).round(2), 0)
    cols = ["city", "category", "basket_type", "offer_type",
            "revenue", "impulse_pct", "avg_price", "offer_lift", "margin_pct"]
    return agg[cols]


if __name__ == "__main__":
    df    = extract(RAW_PATH)
    df    = clean(df)
    df    = engineer(df)
    os.makedirs(os.path.dirname(CLEAN_PATH), exist_ok=True)
    df.to_csv(CLEAN_PATH, index=False)
    print(f"[SAVE]    {CLEAN_PATH}")

    final = tableau_aggregate(df)
    final.to_csv(FINAL_PATH, index=False)
    print(f"[SAVE]    {FINAL_PATH}  ({len(final):,} rows)")
    print("[DONE]    ETL corrected pipeline complete.")

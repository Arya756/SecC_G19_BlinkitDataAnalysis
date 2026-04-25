#!/usr/bin/env python3
"""
ETL Pipeline — The Unplanned Basket
Runs extraction, cleaning, feature engineering, and final load prep
in a single script. Mirrors the logic in notebooks 01–05.
"""

import pandas as pd
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_PATH = os.path.join(BASE_DIR, "data", "raw", "blinkit_dataset (2).csv")
CLEAN_PATH = os.path.join(BASE_DIR, "data", "processed", "cleaned.csv")
FINAL_PATH = os.path.join(BASE_DIR, "data", "processed", "final_dataset.csv")


def extract(path):
    """Load raw data and print basic stats."""
    df = pd.read_csv(path)
    print(f"[EXTRACT] Loaded {df.shape[0]} rows × {df.shape[1]} cols from {path}")
    print(f"  Nulls: {df.isnull().sum().sum()}  |  offer_type NaN: {df['offer_type'].isna().sum()}")
    return df


def clean_and_engineer(df):
    """Clean data and engineer impulse-behaviour features."""
    # Missing values
    df['offer_type'] = df['offer_type'].fillna('No Offer')
    for c in df.select_dtypes('number').columns:
        df[c] = df[c].fillna(df[c].median())
    for c in df.select_dtypes('object').columns:
        df[c] = df[c].fillna(df[c].mode()[0])

    # Duplicates
    before = len(df)
    df.drop_duplicates(inplace=True)
    print(f"[CLEAN] Removed {before - len(df)} duplicates → {len(df)} rows")

    # Standardise text
    for c in df.select_dtypes('object').columns:
        df[c] = df[c].astype(str).str.lower().str.strip()

    # Feature engineering
    df['revenue_inr'] = df['final_price'] * df['sold_quantity']
    df['price_per_100g'] = df['final_price'] / (df['weight_g'] / 100)
    df['weight_bucket'] = np.where(df['weight_g'] < 300, 'small',
                          np.where(df['weight_g'] <= 700, 'mid', 'bulk'))
    df['is_perishable'] = (df['shelf_life_days'] <= 30).astype(int)
    impulse_cats = ['snacks', 'dairy', 'beverages', 'bakery', 'fruits & vegetables']
    df['is_impulse_category'] = df['category'].isin(impulse_cats).astype(int)
    df['has_offer'] = (df['offer_type'] != 'no offer').astype(int)
    df['is_small'] = (df['weight_bucket'] == 'small').astype(int)

    # Impulse score & basket classification
    df['impulse_score'] = (0.30 * df['is_small'] + 0.25 * df['is_perishable']
                         + 0.25 * df['is_impulse_category'] + 0.20 * df['has_offer'])
    df['basket_type'] = np.where(df['impulse_score'] >= 0.6, 'Impulse',
                        np.where(df['impulse_score'] <= 0.4, 'Planned', 'Mixed'))

    # Advanced features
    cat_avg = df.groupby('category')['price_per_100g'].transform('mean')
    df['impulse_premium_pct'] = ((df['price_per_100g'] - cat_avg) / cat_avg) * 100
    city_mean = df.groupby('city')['impulse_score'].transform('mean')
    global_mean = df['impulse_score'].mean()
    df['city_impulse_index'] = city_mean / global_mean if global_mean > 0 else 1.0

    print(f"[ENGINEER] Features created. Basket split: {df['basket_type'].value_counts().to_dict()}")
    return df


def load_final(df):
    """Aggregate and export Tableau-ready dataset."""
    df['cost_price'] = df['final_price'] * (1 - df['profit_margin_pct'] / 100)
    df['margin_inr'] = (df['final_price'] - df['cost_price']) * df['sold_quantity']

    agg = df.groupby(['city', 'category', 'basket_type', 'offer_type']).agg(
        revenue=('revenue_inr', 'sum'),
        margin=('margin_inr', 'sum'),
        avg_price=('final_price', 'mean'),
        total_qty=('sold_quantity', 'sum'),
        impulse_premium=('impulse_premium_pct', 'mean')
    ).reset_index()

    agg['margin_pct'] = (agg['margin'] / agg['revenue'] * 100).round(2)
    base = agg[agg['offer_type'] == 'no offer'].groupby(
        ['city', 'category', 'basket_type'])['total_qty'].mean().reset_index(name='base_qty')
    agg = agg.merge(base, on=['city', 'category', 'basket_type'], how='left')
    agg['offer_lift'] = np.where(agg['base_qty'] > 0, agg['total_qty'] / agg['base_qty'], 1.0)
    tot = agg.groupby(['city', 'category'])['revenue'].transform('sum')
    agg['impulse_pct'] = np.where(agg['basket_type'] == 'Impulse',
                                   (agg['revenue'] / tot * 100).round(2), 0)

    final = agg[['city', 'category', 'basket_type', 'revenue', 'impulse_pct',
                  'avg_price', 'offer_lift', 'margin_pct']].copy()
    return final


if __name__ == "__main__":
    # Extract
    df = extract(RAW_PATH)

    # Clean & Engineer
    df = clean_and_engineer(df)
    os.makedirs(os.path.dirname(CLEAN_PATH), exist_ok=True)
    df.to_csv(CLEAN_PATH, index=False)
    print(f"[SAVE] Cleaned data → {CLEAN_PATH}")

    # Final Load
    final = load_final(df)
    final.to_csv(FINAL_PATH, index=False)
    print(f"[SAVE] Final dataset → {FINAL_PATH} ({final.shape[0]} rows)")
    print("[DONE] ETL pipeline complete.")

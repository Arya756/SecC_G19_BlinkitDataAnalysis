# The Unplanned Basket

**How quick-commerce is converting India's weekly grocery list into a daily stream of impulse spending**

*Newton School of Technology — Data Visualization & Analytics, Capstone 2*

---

## Project Overview

| Field | Details |
|---|---|
| **Project Title** | The Unplanned Basket |
| **Sector** | Retail / Quick Commerce |
| **Team ID** | DVA-C-G19 |
| **Section** | C |
| **Faculty Mentor** | _To be filled_ |
| **Institute** | Newton School of Technology |
| **Submission Date** | April 2026 |

### Team Members

| Role | Name | GitHub Username |
|---|---|---|
| Project Lead | Aryan Patel | `aryanpatel6215` |
| Data Lead | Ayush Aryan | `Arya756` |
| ETL Lead | _Name_ | `github-handle` |
| Analysis Lead | _Name_ | `github-handle` |
| Visualization Lead | _Name_ | `github-handle` |
| Strategy Lead | _Name_ | `github-handle` |
| PPT and Quality Lead | _Name_ | `github-handle` |

---

## Business Problem

India's quick-commerce platforms deliver groceries in under 10 minutes, eliminating the friction that once separated a craving from a purchase. This near-zero friction environment creates a structural incentive for unplanned buying — but the exact size and economics of that impulse layer in Blinkit's catalogue have never been quantified. This project builds an impulse-proxy scoring model across 13,000 SKUs in 10 cities to measure what share of revenue is planned necessity versus unplanned convenience, and to price the premium consumers pay for that convenience.

**Core Business Question**

> What share of Blinkit's sales is driven by impulse behaviour — and how much more are consumers paying per gram for the convenience of small-pack, quick-delivery formats?

**Decision Supported**

> This analysis enables Blinkit's category and pricing teams to reallocate assortment investment toward high-impulse categories, reprice small-pack SKUs based on empirically validated premiums, and redirect promotional spend away from discounts that do not drive incremental volume.

---

## Dataset

| Attribute | Details |
|---|---|
| **Source Name** | Blinkit Product-Level Operational Dataset (Kaggle) |
| **Direct Access Link** | _Paste direct download URL_ |
| **Row Count** | 13,000 SKUs |
| **Column Count** | 25 columns |
| **Time Period Covered** | Product-level snapshot (single period) |
| **Format** | CSV |

**Key Columns Used**

| Column Name | Description | Role in Analysis |
|---|---|---|
| `category` | Product category (8 types) | Impulse classification, segmentation |
| `final_price` | Price after discount (₹) | Revenue computation, pricing analysis |
| `sold_quantity` | Units sold | Revenue computation, demand analysis |
| `weight_g` | Product weight in grams | Pack-size segmentation, convenience premium |
| `shelf_life_days` | Shelf life in days | Perishability flag for impulse scoring |
| `offer_type` | Offer type applied | Promotional impact testing |
| `city` | City of sale (10 cities) | Geographic segmentation |
| `discount_pct` | Discount percentage (0–30%) | Pricing and offer analysis |

For full column definitions and engineered features, see [`docs/data_dictionary.md`](docs/data_dictionary.md).

---

## KPI Framework

| KPI | Definition | Formula / Computation |
|---|---|---|
| Impulse Revenue Share % | Share of total revenue attributable to impulse-classified SKUs | `Σ revenue (basket_type = Impulse) / Σ total revenue × 100` — computed in `notebooks/05_final_load_prep.ipynb` |
| Convenience Premium (Tap Tax) | Price-per-100g ratio of small vs bulk packs | `median(price_per_100g, small) / median(price_per_100g, bulk)` — Welch t-test in `notebooks/04_statistical_analysis.ipynb` |
| Impulse Score | Composite proxy score per SKU for impulse likelihood | `0.30×is_small + 0.25×is_perishable + 0.25×is_impulse_category + 0.20×has_offer` — engineered in `notebooks/02_cleaning.ipynb` |
| City Impulse Index | City's impulse propensity relative to the national average | `city_mean_impulse_score / global_mean_impulse_score` — computed in `scripts/etl_pipeline.py` |
| Offer Lift Ratio | Demand uplift from promotional offers | `avg_sold_qty_with_offer / avg_sold_qty_no_offer` — ANOVA test in `notebooks/04_statistical_analysis.ipynb` |

---

## Tableau Dashboard

| Item | Details |
|---|---|
| **Dashboard 1 — Anatomy of the Basket** | URL: _Paste Tableau Public link_ |
| **Dashboard 2 — Geography of Impulse** | URL: _Paste Tableau Public link_ |
| **Dashboard 3 — The Trigger Engine** | URL: _Paste Tableau Public link_ |
| **Dashboard 4 — The Hidden Bill** | URL: _Paste Tableau Public link_ |
| **Executive View** | Revenue split (Impulse / Mixed / Planned) by category and city, KPI scorecards |
| **Operational View** | SKU-level drill-down by basket type, offer type, and weight bucket |
| **Main Filters** | City, Category, Basket Type, Offer Type, Weight Bucket |

Store dashboard screenshots in [`tableau/screenshots/`](tableau/screenshots/) and document public links in [`tableau/dashboard_links.md`](tableau/dashboard_links.md).

---

## Key Insights

1. **The impulse layer is real and significant.** 21.6% of Blinkit's total revenue comes from SKUs with impulse characteristics. When Mixed baskets are included, 48.8% of revenue carries some impulse signal.

2. **Three categories own the impulse business.** Bakery (38.8%), Fruits & Vegetables (30.2%), and Dairy (20.1%) together account for 89% of all impulse revenue. These are the categories that must receive priority assortment and supply-chain investment.

3. **Fruits & Vegetables, Bakery, and Dairy are structurally impulse-driven.** 62–70% of revenue in these categories comes from impulse-classified SKUs. Personal Care, Grocery, and Household are the opposite — over 80% planned.

4. **Small packs charge a 6× convenience premium.** Median price-per-100g is ₹110 for small packs (<300g) versus ₹18 for bulk (>700g). This difference is statistically undeniable (Welch t-test: t=49.40, p≈0.00) and represents the core monetisation lever in quick-commerce.

5. **Impulse is a pricing story, not a volume story.** Impulse SKUs do not sell more units than planned SKUs (Mann-Whitney U, p=0.80). The revenue premium comes entirely from higher per-gram prices — not from lifting purchase frequency or basket size.

6. **Offers do not trigger impulse purchases.** Promotions do not significantly increase sold quantity (ANOVA, p=0.41). Discount spend is not converting to incremental demand. The impulse decision is driven by category, pack size, and perishability, not price cuts.

7. **Impulse buying is a national urban pattern.** City impulse share ranges from 17.8% (Pune) to 24.9% (Ahmedabad), but this variation is not statistically significant (Kruskal-Wallis, p=0.43). A single national assortment and pricing strategy is more defensible than city-by-city customisation.

8. **The Pareto principle partially holds.** The top 20% of SKUs drive 60.3% of revenue — concentrated, but not the classic 80/20. A meaningful long tail of mid-revenue SKUs contributes to assortment depth and cannot be pruned without consequence.

9. **demand_index is a reliable operational proxy.** Correlation between demand_index and sold_quantity is 0.91 — it can be used confidently in inventory and supply-chain planning without requiring transactional history.

10. **Consumer quantity decisions are not explained by standard levers.** Linear regression of sold_quantity on impulse score, offers, price, and discount produces R² ≈ 0.000 (F-stat p=0.675). Volume is driven by factors outside this dataset — likely habit, household need, and availability.

---

## Recommendations

| # | Insight | Recommendation | Expected Impact |
|---|---|---|---|
| 1 | Bakery, F&V, and Dairy drive 89% of impulse revenue | Rebalance assortment investment toward these three categories with disproportionate shelf-space and supply-chain priority | Higher impulse revenue capture; reduced stockouts in the highest-margin basket type |
| 2 | Small packs charge a 6× per-gram premium | Expand small-pack SKUs in mid-performing impulse categories (Snacks, Beverages) where the premium is currently under-exploited | Increased margin-per-transaction without volume investment |
| 3 | Offers do not lift demand significantly | Redirect promotional spend from price discounts to visibility investments — placement, push notifications, in-app placement | Same or better demand at lower promotional cost |
| 4 | Impulse share is uniform across all 10 cities | Deploy a single national impulse-assortment playbook rather than city-customised approaches, saving operational complexity | Faster rollout, consistent margin performance, reduced localisation overhead |
| 5 | Impulse is a pricing phenomenon, not a volume one | Build pricing models around price-per-100g economics rather than absolute price to optimise margin extraction across pack-size tiers | Defensible pricing architecture grounded in empirically validated consumer willingness-to-pay |

---

## Repository Structure

```text
DVA_Capstone2_C_G19/
|
|-- README.md
|
|-- data/
|   |-- raw/                         # Original dataset (never edited)
|   `-- processed/                   # Cleaned output from ETL pipeline
|
|-- notebooks/
|   |-- 01_extraction.ipynb          # Data sourcing and initial profiling
|   |-- 02_cleaning.ipynb            # Cleaning, imputation, feature engineering
|   |-- 03_eda.ipynb                 # Exploratory data analysis
|   |-- 04_statistical_analysis.ipynb # Hypothesis testing and regression
|   `-- 05_final_load_prep.ipynb     # Tableau-ready dataset preparation
|
|-- scripts/
|   `-- etl_pipeline.py              # Standalone ETL pipeline (mirrors notebooks 01–05)
|
|-- tableau/
|   |-- screenshots/
|   `-- dashboard_links.md
|
|-- reports/
|   |-- project_report.md
|   `-- The_Unplanned_Basket_Presentation.pdf
|
`-- docs/
    `-- data_dictionary.md
```

---

## Analytical Pipeline

1. **Define** — Sector selected (Quick Commerce / Retail), problem statement scoped around impulse vs planned basket classification, mentor approval obtained.
2. **Extract** — Blinkit product-level dataset (13,000 SKUs × 25 columns) sourced and committed to `data/raw/`; data dictionary drafted in `docs/data_dictionary.md`.
3. **Clean and Transform** — Missing values imputed (median for numeric, mode for categorical; `offer_type` NaN recoded as "No Offer"), duplicates removed, text standardised. Impulse proxy features engineered: `revenue_inr`, `price_per_100g`, `weight_bucket`, `is_perishable`, `impulse_score`, `basket_type`, `city_impulse_index`. Pipeline in `notebooks/02_cleaning.ipynb` and `scripts/etl_pipeline.py`.
4. **Analyze** — EDA covering revenue distribution, category breakdown, and city-level patterns (`notebooks/03_eda.ipynb`). Five hypothesis tests (Mann-Whitney U, ANOVA, Kruskal-Wallis, Welch t-test, Pareto analysis) and linear regression in `notebooks/04_statistical_analysis.ipynb`.
5. **Visualize** — Interactive Tableau dashboard built across four views: Anatomy of the Basket, Geography of Impulse, The Trigger Engine, The Hidden Bill.
6. **Recommend** — Five data-backed business recommendations on assortment, pricing, promotions, and geographic strategy.
7. **Report** — Final project report and presentation deck exported to PDF in `reports/`.

---

## Tech Stack

| Tool | Status | Purpose |
|---|---|---|
| Python + Jupyter Notebooks | Mandatory | ETL, cleaning, feature engineering, statistical analysis, KPI computation |
| Google Colab | Supported | Cloud notebook execution environment |
| Tableau Public | Mandatory | Dashboard design, publishing, and sharing |
| GitHub | Mandatory | Version control, collaboration, contribution audit |

**Python libraries used:** `pandas`, `numpy`, `matplotlib`, `seaborn`, `scipy`, `statsmodels`

---

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install pandas numpy scipy statsmodels matplotlib seaborn jupyter
jupyter notebook
```

Run notebooks in order: `01_extraction` → `02_cleaning` → `03_eda` → `04_statistical_analysis` → `05_final_load_prep`

Or run the standalone pipeline:

```bash
python scripts/etl_pipeline.py
```

---

## Submission Checklist

**GitHub Repository**

- [x] All notebooks committed in `.ipynb` format
- [x] `data/raw/` contains the original, unedited dataset
- [x] `data/processed/` contains the cleaned pipeline output (`cleaned.csv`, `final_dataset.csv`)
- [x] `docs/data_dictionary.md` is complete
- [x] `scripts/etl_pipeline.py` mirrors notebook logic end-to-end
- [ ] `tableau/screenshots/` contains dashboard screenshots
- [ ] `tableau/dashboard_links.md` contains Tableau Public URLs
- [ ] All members have visible commits and pull requests

**Tableau Dashboard**

- [ ] Published on Tableau Public and accessible via public URL
- [ ] At least one interactive filter included
- [ ] Dashboard directly addresses the business problem

**Project Report**

- [x] Final report in `reports/project_report.md`
- [ ] Final report exported as PDF into `reports/`
- [x] Executive summary, sector context, problem statement
- [x] Data description, cleaning methodology, KPI framework
- [x] EDA with written insights, statistical analysis results
- [x] 8-12 key insights in decision language
- [x] 3-5 actionable recommendations with impact estimates
- [ ] Contribution matrix matches GitHub history

**Presentation Deck**

- [x] Presentation PDF in `reports/`

---

## Contribution Matrix

| Team Member | Dataset and Sourcing | ETL and Cleaning | EDA and Analysis | Statistical Analysis | Tableau Dashboard | Report Writing | PPT and Viva |
|---|---|---|---|---|---|---|---|
| Aryan Patel | Owner | Owner | Owner | Owner | Support | Owner | Support |
| Ayush Aryan | Support | Support | Support | Support | Owner | Support | Owner |
| _Member 3_ | | | | | | | |
| _Member 4_ | | | | | | | |
| _Member 5_ | | | | | | | |
| _Member 6_ | | | | | | | |

**Team Lead:** Aryan Patel

---

*Newton School of Technology — Data Visualization & Analytics | Capstone 2*

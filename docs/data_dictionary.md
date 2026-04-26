# Data Dictionary — Blinkit Dataset

## Raw Dataset (`data/raw/blinkit_dataset (2).csv`)

| # | Column | Type | Description |
|---|--------|------|-------------|
| 1 | `product_id` | int | Unique product identifier |
| 2 | `product_name` | str | Product display name |
| 3 | `category` | str | Product category (8 categories) |
| 4 | `brand` | str | Brand name (28 brands) |
| 5 | `price` | float | MRP / list price (₹) |
| 6 | `discount_pct` | int | Discount percentage applied (0–30) |
| 7 | `final_price` | float | Price after discount (₹) |
| 8 | `rating` | float | Customer rating (1–5) |
| 9 | `num_reviews` | int | Number of customer reviews |
| 10 | `delivery_time_min` | int | Delivery time in minutes |
| 11 | `city` | str | City of sale (10 cities) |
| 12 | `seller` | str | Seller name |
| 13 | `stock` | int | Current stock level |
| 14 | `sold_quantity` | int | Units sold |
| 15 | `profit_margin_pct` | float | Profit margin percentage |
| 16 | `is_organic` | bool | Whether product is organic |
| 17 | `packaging_type` | str | Packaging type (Can, Jar, Bottle, etc.) |
| 18 | `weight_g` | int | Product weight in grams |
| 19 | `shelf_life_days` | int | Shelf life in days |
| 20 | `reorder_level` | int | Reorder threshold |
| 21 | `demand_index` | int | Demand index (0–100) |
| 22 | `date_added` | date | Date product was added |
| 23 | `expiry_date` | date | Product expiry date |
| 24 | `offer_type` | str | Offer type (None/FreeDelivery/FlatDiscount/Buy1Get1/Cashback) |
| 25 | `delivery_status` | str | Delivery status (On-Time/Delayed) |

## Engineered Features (`data/processed/cleaned.csv`)

| # | Feature | Definition |
|---|---------|------------|
| 1 | `revenue_inr` | `final_price × sold_quantity` |
| 2 | `price_per_100g` | `final_price / (weight_g / 100)` |
| 3 | `weight_bucket` | small (<300g) · mid (300–700g) · bulk (>700g) |
| 4 | `is_perishable` | 1 if `shelf_life_days ≤ 30` |
| 5 | `is_impulse_category` | 1 if category ∈ {snacks, dairy, beverages, bakery, fruits & vegetables} |
| 6 | `has_offer` | 1 if `offer_type ≠ 'no offer'` |
| 7 | `is_small` | 1 if `weight_bucket == 'small'` |
| 8 | `impulse_score` | 0.30×is_small + 0.25×is_perishable + 0.25×is_impulse_category + 0.20×has_offer |
| 9 | `basket_type` | Impulse (≥0.6) · Planned (≤0.4) · Mixed |
| 10 | `impulse_premium_pct` | (price_per_100g − category_avg) / category_avg × 100 |
| 11 | `city_impulse_index` | city_mean_impulse_score / global_mean_impulse_score |

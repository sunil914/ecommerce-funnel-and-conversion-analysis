# E-commerce Funnel & Conversion Analysis

> **Status:** Validated data and executable SQLite analysis complete · Tableau dashboard in progress

## Overview

This project analyses 120,000 synthetic direct-to-consumer shopping sessions from website visit through product view, add to cart, checkout and purchase. The goal is to locate the largest funnel losses and compare conversion quality across acquisition and experience segments.

**Dataset:** [Direct-to-Consumer E-commerce Funnel Dataset](https://www.kaggle.com/datasets/yashch05/direct-to-consumer-e-commerce-funnel-dataset)

## Key KPIs

| Metric | Result |
|---|---:|
| Sessions | 120,000 |
| Product views | 77,870 |
| Added to cart | 27,156 |
| Checkouts started | 16,234 |
| Purchases | 8,181 |
| Session purchase rate | 6.82% |
| Revenue | $17.02M |
| Average order value | $2,080.01 |

## Analysis completed

- Parsed dates and standardised channel, campaign, device, user type and region.
- Converted funnel stages into numeric flags and validated stage monotonicity.
- Reconciled all summaries to 120,000 unique sessions.
- Analysed funnel drop-off, acquisition channel, campaign, device, region, user type and monthly performance.
- Identified the largest absolute loss before Add to Cart.

## Validated funnel diagnostics

The executable `v_funnel_stages` view reports the previous-stage population, absolute drop-off, stage-to-stage conversion and overall conversion for every step:

| Stage | Sessions | Drop-off from previous stage | Stage conversion | Overall conversion |
|---|---:|---:|---:|---:|
| Visited website | 120,000 | — | 100.00% | 100.00% |
| Viewed product | 77,870 | 42,130 | 64.89% | 64.89% |
| Added to cart | 27,156 | 50,714 | 34.87% | 22.63% |
| Checkout started | 16,234 | 10,922 | 59.78% | 13.53% |
| Purchase completed | 8,181 | 8,053 | 50.39% | 6.82% |

The largest absolute loss is the **50,714-session drop from product view to cart**. This identifies the first optimisation area to investigate, but the synthetic data does not establish why users left or prove that a product-page change would cause improvement.

## Repository contents

- [`data/`](data/) — cleaned full dataset, preview sample, source and validation notes
- [`sql/`](sql/) — executable SQLite schema, funnel analysis views and run guide
- [`scripts/build_database.py`](scripts/build_database.py) — standard-library loader that rebuilds and validates `project.db`
- [`tableau/`](tableau/) — build guide; workbook and screenshots are still pending

## Tableau dashboard — in progress

Planned views:

- Five-stage conversion funnel and drop-off table
- Purchase rate and revenue per session by channel
- Campaign performance
- Monthly conversion trend
- Device × user-type heatmap
- Regional comparison and interactive filters

## Key insights

- Overall session-to-purchase conversion was **6.82%**.
- Email had the highest observed channel purchase rate.
- New users had the highest observed user-type purchase rate.
- Product-page optimisation is the first testing priority because the largest loss occurred before Add to Cart.

## Repository roadmap

- [x] Business problem and KPI definition
- [x] Cleaning and validation approach
- [x] SQL analysis documented
- [x] Findings and recommendations documented
- [x] Add cleaned data with source and validation notes
- [x] Add reproducible SQLite database loader
- [ ] Add reproducible preparation code
- [x] Add complete SQL schema and analysis views
- [ ] Build and publish Tableau dashboard
- [ ] Add dashboard screenshots and Tableau Public link

## Responsible interpretation

This dataset is synthetic. The results demonstrate funnel-analysis methods and should not be presented as the performance of a real retailer.

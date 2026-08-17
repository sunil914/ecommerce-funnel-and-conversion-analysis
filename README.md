# E-commerce Funnel & Conversion Analysis

> **Status:** Core analysis documented · Tableau dashboard in progress

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
- [ ] Add cleaned data and reproducible preparation code
- [ ] Add complete SQL script and analysis outputs
- [ ] Build and publish Tableau dashboard
- [ ] Add dashboard screenshots and Tableau Public link

## Responsible interpretation

This dataset is synthetic. The results demonstrate funnel-analysis methods and should not be presented as the performance of a real retailer.

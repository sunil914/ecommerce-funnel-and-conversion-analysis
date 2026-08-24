# Data

## File

`ecommerce_funnel_clean.csv.gz` contains 120,000 synthetic shopping sessions and 23 columns. `ecommerce_funnel_sample.csv` provides the first 500 rows for browser preview. Decompress the full file with `gzip -dk ecommerce_funnel_clean.csv.gz`.

## Source

- Dataset: Direct-to-Consumer E-Commerce Funnel Dataset
- URL: https://www.kaggle.com/datasets/yashch05/direct-to-consumer-e-commerce-funnel-dataset
- Creator: Yash Chauhan
- Nature: synthetically generated for educational and portfolio analysis
- License note: Kaggle currently lists the formal license as `Unknown`; reuse should follow the creator's dataset page and Kaggle terms.

## Preparation

Dates were standardised to `YYYY-MM-DD`. Numeric flags were added for visit, product view, add to cart, checkout, purchase and discount stages while preserving the original Yes/No fields. No sessions or values were fabricated or removed.

## Validation

| Check | Result |
|---|---:|
| Sessions | 120,000 |
| Product views | 77,870 |
| Added to cart | 27,156 |
| Checkouts started | 16,234 |
| Purchases | 8,181 |
| Session purchase rate | 6.82% |
| Revenue | $17,016,599.15 |

Uncompressed CSV SHA-256: `af9b9f975924f0b7a09588c9d21b6f316a8440d88ec1e2883a0d2f3bf0d87eb9`

Compressed file SHA-256: `3d6464f5c966fc1cc3971cfa81223681fa7ce53dbc65d4172f346e911d2c57bb`

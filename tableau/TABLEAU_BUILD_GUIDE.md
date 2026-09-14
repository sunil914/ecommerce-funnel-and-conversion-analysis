# Tableau Dashboard Build Guide

> **Project status:** Dashboard design and publishing are still in progress.  
> This guide translates the documented analysis into a reproducible Tableau build plan without claiming that the final dashboard is complete.

## 1. Dashboard purpose

Build an executive-friendly funnel dashboard that answers four questions:

1. Where are users leaving the purchase journey?
2. Which acquisition channels and campaign types produce the strongest purchase quality?
3. How does performance vary across device, user type, region and month?
4. Which observations should become controlled optimisation tests?

## 2. Required Tableau input

The cleaned session-level input is already committed in `data/ecommerce_funnel_clean.csv.gz.part-*`. From the repository root, reconstruct and decompress it before connecting the resulting CSV to Tableau:

```bash
cd data
cat ecommerce_funnel_clean.csv.gz.part-* > ecommerce_funnel_clean.csv.gz
gzip -dk ecommerce_funnel_clean.csv.gz
```

Check the uncompressed CSV against the SHA-256 in [`data/README.md`](../data/README.md) before using it. Keep the original 120,000 session rows as the Tableau source; do not join the separately aggregated SQL views to session rows, since that would multiply counts. Alternatively, `python3 scripts/build_database.py` rebuilds `project.db` and its views for independent reconciliation.

| CSV field | Tableau role |
|---|---|
| `session_id` | Unique session identifier (text) |
| `date` / `month` | Date / chronological year-month |
| `channel`, `campaign_type` | Acquisition comparisons |
| `device`, `user_type`, `region` | Experience comparisons |
| `visited_website_flag`, `viewed_product_flag`, `added_to_cart_flag`, `checkout_started_flag`, `purchase_completed_flag` | Numeric 0/1 funnel indicators |
| `revenue` | Revenue from completed purchases |
| `discount_applied_flag` | Numeric 0/1 segmentation filter |

In Tableau, confirm `session_id` stays text, `date` parses as a date, `month` sorts chronologically, the flags are numeric and `revenue` is decimal. If Tableau displays underscores or changes case in field labels, update the calculated-field references below to the names it actually shows.

## 3. Reconciliation checks

Create a temporary validation sheet and confirm that Tableau reproduces the documented totals:

| Check | Expected result |
|---|---:|
| Distinct sessions | 120,000 |
| Product views | 77,870 |
| Added to cart | 27,156 |
| Checkouts started | 16,234 |
| Purchases | 8,181 |
| Session purchase rate | 6.82% |
| Revenue | $17.02M |
| Average order value | $2,080.01 |

Also confirm the funnel relationship:

```text
Purchases ≤ Checkouts ≤ Carts ≤ Product Views ≤ Sessions
```

Do not publish if filters or joins cause these totals to stop reconciling.

## 4. Calculated fields

Adjust field names only if the cleaned export uses a different naming convention.

### Session Purchase Rate

```text
SUM([Purchase Completed Flag]) / COUNTD([Session ID])
```

### Product View Rate

```text
SUM([Viewed Product Flag]) / COUNTD([Session ID])
```

### View-to-Cart Rate

```text
IF SUM([Viewed Product Flag]) > 0 THEN
    SUM([Added To Cart Flag]) / SUM([Viewed Product Flag])
END
```

### Cart-to-Checkout Rate

```text
IF SUM([Added To Cart Flag]) > 0 THEN
    SUM([Checkout Started Flag]) / SUM([Added To Cart Flag])
END
```

### Checkout-to-Purchase Rate

```text
IF SUM([Checkout Started Flag]) > 0 THEN
    SUM([Purchase Completed Flag]) / SUM([Checkout Started Flag])
END
```

### Revenue per Session

```text
SUM([Revenue]) / COUNTD([Session ID])
```

### Average Order Value

```text
IF SUM([Purchase Completed Flag]) > 0 THEN
    SUM([Revenue]) / SUM([Purchase Completed Flag])
END
```

Format rates as percentages, revenue measures as currency, and session counts as whole numbers.

## 5. Recommended worksheets

### A. KPI cards

Create individual cards for:

- Sessions
- Purchases
- Session Purchase Rate
- Revenue
- Average Order Value

Each card should respond to the dashboard filters.

### B. Five-stage funnel

Use a stage/value structure containing, in fixed order:

1. Sessions: `SUM([Visited Website Flag])`
2. Product Views: `SUM([Viewed Product Flag])`
3. Added to Cart: `SUM([Added To Cart Flag])`
4. Checkout Started: `SUM([Checkout Started Flag])`
5. Purchases: `SUM([Purchase Completed Flag])`

Build these values from the same filtered session-level source (for example, with Measure Names/Measure Values), rather than hard-coding the unfiltered totals into a separate table. For each stage, divide its count by the filtered Sessions value to show overall conversion. With no filters, the stage totals must match `v_funnel_stages` in `project.db`.

### C. Funnel drop-off table

For every stage transition, display:

- Previous-stage count
- Next-stage count
- Absolute drop-off
- Stage-to-stage conversion rate
- Stage-to-stage drop-off rate

The documented analysis identifies the largest absolute loss before Add to Cart; the chart should make this visible without overstating causality.

### D. Channel performance

Compare Channel using:

- Sessions
- Purchases
- Purchase Rate
- Revenue per Session
- Average Order Value

Sort primarily by Purchase Rate, but retain session volume so small segments are not mistaken for the strongest commercial opportunity.

### E. Monthly trend

Plot Year Month with:

- Sessions
- Purchases
- Purchase Rate

Use a dual-axis view only if labels and scales remain clear. Otherwise, use aligned charts.

### F. Device × User Type heatmap

- Rows: Device
- Columns: User Type
- Colour: Purchase Rate
- Label or tooltip: Sessions and Purchases

Include volume because rate comparisons can mislead when group sizes differ.

### G. Campaign and regional comparison

Use ranked bars for Campaign Type and Region. Show Sessions, Purchase Rate and Revenue per Session in the tooltip.

## 6. Dashboard layout

Recommended reading order:

1. Title, scope and synthetic-data disclosure
2. KPI row
3. Funnel and drop-off analysis
4. Channel and campaign performance
5. Monthly trend
6. Device/user-type and regional comparisons
7. Filters and definitions

Use consistent colours:

- Neutral colour for total sessions
- One accent colour for progression
- A contrasting alert colour for drop-off
- Avoid red/green-only encoding so the dashboard remains accessible

## 7. Filters and interactions

Add filters for:

- Month
- Channel
- Campaign Type
- Device
- User Type
- Region
- Discount Applied

Apply each filter to all relevant worksheets. Add a reset button and test that filter combinations still reconcile to the filtered session population.

## 8. Tooltip standard

Every analytical tooltip should state:

- Segment name
- Session count
- Purchase count
- Purchase Rate
- Revenue per Session where relevant

Avoid causal language. Prefer “observed purchase rate” over “caused conversion.”

## 9. Publishing checklist

- [x] Clean session-level input committed as multipart gzip (reconstruct and checksum before connecting)
- [ ] KPI totals reconcile to documented results
- [ ] Funnel order and stage logic validated
- [ ] All filters tested
- [ ] Titles describe metric and population
- [ ] Percentages and currencies formatted consistently
- [ ] Synthetic-data disclosure visible
- [ ] Dashboard tested at desktop and mobile sizes
- [ ] Workbook published to Tableau Public
- [ ] Screenshot added to `images/`
- [ ] Tableau Public link added to the README
- [ ] Repository status changed only after the live dashboard is verified

## 10. Responsible interpretation

The dataset is synthetic. Segment differences are descriptive and should be framed as hypotheses for controlled testing, not proof that a channel, device or user characteristic caused the observed outcome.

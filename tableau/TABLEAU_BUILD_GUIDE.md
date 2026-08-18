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

Use the cleaned session-level export when it is added to this repository. The Tableau source should contain one row per session and include:

| Field | Expected role |
|---|---|
| Session ID | Unique session identifier |
| Date / Year Month | Time-series analysis |
| Channel | Acquisition comparison |
| Campaign Type | Campaign comparison |
| Device | Experience comparison |
| User Type | New/returning-user comparison |
| Region | Geographic comparison |
| Viewed Product Flag | Funnel stage indicator |
| Added To Cart Flag | Funnel stage indicator |
| Checkout Started Flag | Funnel stage indicator |
| Purchase Completed Flag | Funnel stage indicator |
| Revenue | Revenue from completed purchases |
| Discount Applied | Optional segmentation filter |

Before building charts, confirm that each stage flag is numeric (0/1), dates are recognised as dates, and Revenue is numeric.

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

Use a stage/value structure containing:

1. Sessions
2. Product Views
3. Added to Cart
4. Checkout Started
5. Purchases

Show both the stage count and percentage of total sessions. Keep the stage order fixed.

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

- [ ] Clean session-level Tableau input added
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

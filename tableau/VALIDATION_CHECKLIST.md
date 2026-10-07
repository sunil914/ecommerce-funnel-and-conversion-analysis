# Tableau Validation Checklist

> **Status:** Pre-publication quality-assurance specification. The workbook, screenshots and Tableau Public link remain pending.

Run the validated preparation workflow before opening Tableau:

```bash
python3 scripts/prepare_tableau_data.py
```

Use `data/ecommerce_funnel_clean.csv` as the only Tableau data source. Keep SQLite views separate for reconciliation; joining aggregate views to session rows would multiply counts.

## 1. Source and field checks

- [ ] The source contains 120,000 rows and 120,000 distinct `session_id` values.
- [ ] `session_id` remains text.
- [ ] `date` is a date and `month` sorts chronologically.
- [ ] All stage and discount flags are numeric 0/1 measures.
- [ ] `revenue` is decimal currency and is not summed from a duplicated join.
- [ ] The dashboard visibly identifies the dataset as synthetic.

## 2. Opening reconciliation

Clear every filter before recording the opening state.

| Check | Expected result | Pass condition |
|---|---:|---|
| Sessions | 120,000 | Exact distinct count |
| Product views | 77,870 | Exact |
| Added to cart | 27,156 | Exact |
| Checkouts started | 16,234 | Exact |
| Purchases | 8,181 | Exact |
| Session purchase rate | 6.82% | Equal after two-decimal display rounding |
| Revenue | $17,016,599.15 | Equal to the cent |
| Average order value | $2,080.01 | Equal after two-decimal display rounding |

- [ ] Opening counts satisfy Purchases ≤ Checkouts ≤ Carts ≤ Product Views ≤ Sessions.
- [ ] The product-view-to-cart drop-off is 50,714 sessions and is the largest absolute stage loss.
- [ ] KPI cards return to the opening values after clearing filters or using **Revert All**.

## 3. Filtered funnel tests

For Month, Channel, Campaign Type, Device, User Type, Region and Discount Applied:

- [ ] Every stage is calculated from the same filtered session population.
- [ ] Stage counts remain monotonic for every tested selection.
- [ ] Stage conversion uses the immediately preceding stage as its denominator.
- [ ] Overall conversion uses filtered Sessions as its denominator.
- [ ] Zero-denominator selections return null or an explanatory state, not an error or infinity.
- [ ] Revenue per Session uses filtered distinct sessions.
- [ ] Average Order Value uses filtered purchases and returns null when purchases are zero.
- [ ] Resetting filters restores the documented opening totals.

## 4. Interaction and interpretation tests

- [ ] Selecting a channel, campaign or region updates all compatible worksheets.
- [ ] Funnel clicks do not unintentionally exclude earlier-stage sessions.
- [ ] Tooltips state session count, purchase count, observed purchase rate and revenue per session where relevant.
- [ ] Segment comparisons show volume alongside rates.
- [ ] Titles and tooltips use “observed” language and avoid causal claims.
- [ ] The 50,714-session loss is framed as an optimisation hypothesis, not proof of a cause.

## 5. Visual and accessibility checks

- [ ] Funnel order is fixed from Website Visit to Purchase.
- [ ] Important values have text labels and do not rely on colour alone.
- [ ] Drop-off is distinguishable without red/green-only encoding.
- [ ] Text and marks have sufficient contrast.
- [ ] Keyboard and reading order follow title → KPIs → funnel → supporting views → filters.
- [ ] Desktop layout has no clipped labels, overlapping marks or unnecessary scrolling.
- [ ] Phone layout keeps KPIs and funnel first, uses touch-friendly controls and avoids tiny legends.
- [ ] Every worksheet title identifies its metric and population.

## 6. Publication gate

- [ ] Workbook title, data source, synthetic-data disclosure and analytical limitations are visible.
- [ ] All unfiltered values reconcile with `project.db` and the documented KPIs.
- [ ] Representative single- and multi-filter cases pass the monotonicity and denominator checks.
- [ ] Desktop and phone screenshots match the final workbook.
- [ ] Tableau Public URL opens successfully and displays the intended default state.
- [ ] Repository status changes only after the workbook, screenshots and verified public link exist.

Do not mark the Tableau dashboard complete until every required reconciliation, interaction, accessibility and responsible-interpretation check passes.

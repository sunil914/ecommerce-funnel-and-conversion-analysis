# SQLite analysis

Run `python3 scripts/build_database.py` to reconstruct the committed multipart gzip dataset, load all 120,000 sessions into `project.db`, validate integrity and create Tableau-ready views.

The views cover the five-stage funnel, acquisition channels, campaigns, monthly results, device × user type and regions. Expected reconciliation: **120,000 sessions**, **77,870 product views**, **27,156 carts**, **16,234 checkouts**, **8,181 purchases**, **6.82% purchase rate** and **$17,016,599.15 revenue**.

The generated database can be opened in DB Browser for SQLite and is ignored by Git because it can be rebuilt from the committed data.


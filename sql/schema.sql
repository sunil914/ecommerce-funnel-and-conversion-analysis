DROP TABLE IF EXISTS ecommerce_sessions;

CREATE TABLE ecommerce_sessions (
    user_id TEXT, session_id TEXT PRIMARY KEY, date TEXT, month TEXT,
    channel TEXT, campaign_type TEXT, device TEXT, user_type TEXT, region TEXT,
    visited_website INTEGER, viewed_product INTEGER, added_to_cart INTEGER,
    checkout_started INTEGER, purchase_completed INTEGER, discount_applied INTEGER,
    order_value REAL, revenue REAL, visited_website_flag INTEGER,
    viewed_product_flag INTEGER, added_to_cart_flag INTEGER,
    checkout_started_flag INTEGER, purchase_completed_flag INTEGER,
    discount_applied_flag INTEGER
);

CREATE INDEX idx_ecommerce_date ON ecommerce_sessions (date);
CREATE INDEX idx_ecommerce_channel ON ecommerce_sessions (channel);


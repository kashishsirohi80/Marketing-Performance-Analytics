-- ===============================
-- FACT SALES
-- ===============================
CREATE TABLE fact_sales (
    order_id TEXT,
    date DATE,
    product_id TEXT,
    product_type TEXT,
    shipping_country TEXT,
    total_sales REAL,
    net_sales REAL,
    gross_sales REAL,
    orders INTEGER,
    items_sold INTEGER,
    items_returned INTEGER,
    return_rate REAL,
    aov REAL
);

-- ===============================
-- FACT CAMPAIGN
-- ===============================
CREATE TABLE fact_campaign (
    campaign_name TEXT,
    date DATE,
    country TEXT,
    impressions INTEGER,
    clicks INTEGER,
    spend REAL,
    purchases INTEGER,
    revenue REAL,
    CTR REAL,
    CPC REAL,
    CPM REAL,
    ROI REAL
);

-- ===============================
-- DATE DIMENSION
-- ===============================
CREATE TABLE date_dim (
    date DATE PRIMARY KEY,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    quarter INTEGER
);

-- ===============================
-- INDEXES (🔥 IMPORTANT)
-- ===============================

CREATE INDEX idx_sales_date ON fact_sales(date);
CREATE INDEX idx_campaign_date ON fact_campaign(date);
CREATE INDEX idx_campaign_name ON fact_campaign(campaign_name);
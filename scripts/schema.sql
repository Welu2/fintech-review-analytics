-- Fintech Review Analytics Database Schema Dump
-- Target DBMS: PostgreSQL

-- 1. Create Metadata Master Table for Financial Entities
CREATE TABLE IF NOT EXISTS banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(255) UNIQUE NOT NULL,
    app_name VARCHAR(255)
);

-- 2. Create Transactional Table for Granular Review Tracking
CREATE TABLE IF NOT EXISTS reviews (
    review_id SERIAL PRIMARY KEY,
    bank_id INT NOT NULL,
    review_text TEXT,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    review_date DATE NOT NULL,
    sentiment_label VARCHAR(50),
    sentiment_score NUMERIC(4,3),
    identified_theme VARCHAR(255),
    source VARCHAR(100) NOT NULL,
    FOREIGN KEY (bank_id) REFERENCES banks(bank_id) ON DELETE CASCADE
);

-- 3. Create Optimization Indexes for Faster Query Metrics
CREATE INDEX IF NOT EXISTS idx_reviews_bank_id ON reviews(bank_id);
CREATE INDEX IF NOT EXISTS idx_reviews_sentiment ON reviews(sentiment_label);

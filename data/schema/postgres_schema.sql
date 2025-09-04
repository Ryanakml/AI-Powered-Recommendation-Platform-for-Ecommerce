CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR(255) PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE,
    profile JSONB
);

CREATE TABLE IF NOT EXISTS items (
    item_id VARCHAR(255) PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR(512),
    description TEXT,
    price NUMERIC(10, 2),
    category VARCHAR(255),
    brand VARCHAR(255),
    metadata JSONB
);

CREATE TABLE IF NOT EXISTS interactions (
    interaction_id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) REFERENCES users(user_id),
    item_id VARCHAR(255) REFERENCES items(item_id),
    event_type VARCHAR(50),
    event_timestamp TIMESTAMP WITH TIME ZONE,
    session_id VARCHAR(255)
);
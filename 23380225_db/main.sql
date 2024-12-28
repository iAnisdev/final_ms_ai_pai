# PostgreSQL 16.x
CREATE DATABASE crypto_analysis;

CREATE TABLE IF NOT EXISTS bitcoin (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP UNIQUE,
    open NUMERIC(20, 8) NOT NULL,
    high NUMERIC(20, 8) NOT NULL,
    low NUMERIC(20, 8) NOT NULL,
    close NUMERIC(20, 8) NOT NULL,
    volume NUMERIC(20, 8) NOT NULL,
    number_of_trades NUMERIC(20, 8) NOT NULL
);

CREATE TABLE IF NOT EXISTS ethereum (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP UNIQUE,
    open NUMERIC(20, 8) NOT NULL,
    high NUMERIC(20, 8) NOT NULL,
    low NUMERIC(20, 8) NOT NULL,
    close NUMERIC(20, 8) NOT NULL,
    volume NUMERIC(20, 8) NOT NULL,
    number_of_trades NUMERIC(20, 8) NOT NULL
);

CREATE TABLE IF NOT EXISTS binance (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP UNIQUE,
    open NUMERIC(20, 8) NOT NULL,
    high NUMERIC(20, 8) NOT NULL,
    low NUMERIC(20, 8) NOT NULL,
    close NUMERIC(20, 8) NOT NULL,
    volume NUMERIC(20, 8) NOT NULL,
    number_of_trades NUMERIC(20, 8) NOT NULL
);

CREATE TABLE IF NOT EXISTS solana (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP UNIQUE,
    open NUMERIC(20, 8) NOT NULL,
    high NUMERIC(20, 8) NOT NULL,
    low NUMERIC(20, 8) NOT NULL,
    close NUMERIC(20, 8) NOT NULL,
    volume NUMERIC(20, 8) NOT NULL,
    number_of_trades NUMERIC(20, 8) NOT NULL
);
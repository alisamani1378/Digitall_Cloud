# Telegram Shop Bot (Docker + PostgreSQL)

A basic Telegram bot with PostgreSQL as the database, designed for a simple shop/e-commerce system.

## How to run

1. Copy `.env.example` to `.env` and set your environment variables (Telegram bot token, DB credentials, etc.).
2. Build and start the containers:
   ```bash
   cd docker
   docker compose build
   docker compose up -d

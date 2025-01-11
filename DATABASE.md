# Database Setup and Configuration Guide

This guide will walk you through installing PostgreSQL, setting it up, and configuring your environment for the project.

## Prerequisites

Ensure you have the following installed on your system:
- PostgreSQL
- A command-line interface (CLI) or a PostgreSQL GUI tool (e.g., pgAdmin)

---

## Installation Instructions

### macOS
1. Install PostgreSQL using Homebrew:
   ```bash
   brew install postgresql
   ```
2. Start the PostgreSQL service:
   ```bash
   brew services start postgresql
   ```

### Ubuntu/Debian
1. Update the package list and install PostgreSQL:
   ```bash
   sudo apt update
   sudo apt install postgresql postgresql-contrib
   ```
2. Start the PostgreSQL service:
   ```bash
   sudo systemctl start postgresql
   ```

### Windows
1. Download the PostgreSQL installer from [the official website](https://www.postgresql.org/download/).
2. Run the installer and follow the setup instructions.
3. Start the PostgreSQL service via the pgAdmin GUI or Services Manager.

---

## Setup a Database

1. **Login to PostgreSQL:**
   ```bash
   psql -U postgres
   ```
   Use the default `postgres` user and enter the password you set during installation.

2. **Create a New Database:**
   Run the following command to create the `crypto_analysis` database:
   ```sql
   CREATE DATABASE crypto_analysis;
   ```

3. **Create a User (Optional):**
   Create a user named `postgres` with a password:
   ```sql
   CREATE USER postgres WITH PASSWORD 'password';
   ```

4. **Grant Permissions:**
   Grant all privileges on the `crypto_analysis` database to the `postgres` user:
   ```sql
   GRANT ALL PRIVILEGES ON DATABASE crypto_analysis TO postgres;
   ```

5. **Exit:**
   Exit the `psql` terminal:
   ```bash
   \q
   ```

---

## Environment Configuration

Update your `.env` file to include the following line:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/crypto_analysis
```

### Explanation of `DATABASE_URL`

- **`postgresql://`**: Specifies the PostgreSQL protocol.
- **`postgres`**: The username for the PostgreSQL database.
- **`password`**: The password associated with the `postgres` user.
- **`localhost`**: The hostname where PostgreSQL is running (use `127.0.0.1` if `localhost` fails).
- **`5432`**: The default port on which PostgreSQL listens.
- **`crypto_analysis`**: The name of the database.

Ensure that the username, password, and database name in your `.env` file match your PostgreSQL setup.

---

## Testing the Connection

Access the database using a local query in the terminal:
   ```bash
   psql -U postgres -d crypto_analysis
   ```
   This connects to the `crypto_analysis` database as the user `postgres`. You can now run SQL queries directly in the terminal.

If successful, your database setup is complete.

---

## Troubleshooting

- **PostgreSQL not running:**
  Make sure the PostgreSQL service is running on your system.
  ```bash
  sudo systemctl start postgresql  # Ubuntu
  brew services start postgresql   # macOS
  ```

- **Connection refused:**
  Ensure that your `DATABASE_URL` is correctly configured and PostgreSQL is listening on the specified port.

- **Permission denied:**
  Verify that the user has the correct permissions for the database.
  ```sql
  GRANT ALL PRIVILEGES ON DATABASE crypto_analysis TO postgres;
  ```

You're now ready to proceed with your project!

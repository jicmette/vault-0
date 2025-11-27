def create_tables(cursor):
  print("⌛ Creating Vault 0 database schema...")

  # Clients table
  cursor.execute("""
  CREATE TABLE IF NOT EXISTS clients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password_hash BYTEA NOT NULL
  );
  """)

  # Accounts table
  cursor.execute("""
  CREATE TABLE IF NOT EXISTS accounts (
    id SERIAL PRIMARY KEY,
    client_id INTEGER REFERENCES clients(id) ON DELETE CASCADE,
    name VARCHAR(50) NOT NULL,
    type VARCHAR(20) CHECK (type IN ('Asset', 'Liability', 'Equity', 'Revenue', 'Expense')),
    balance DECIMAL(15, 2) DEFAULT 0.00
  );
  """)

  # Transactions table
  cursor.execute("""
  CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    date DATE DEFAULT CURRENT_DATE,
    description TEXT NOT NULL
  );
  """)

  # Entries
  cursor.execute("""
  CREATE TABLE IF NOT EXISTS entries (
    id SERIAL PRIMARY KEY,
    transactions_id INTEGER REFERENCES transactions(id) ON DELETE CASCADE,
    account_id INTEGER REFERENCES accounts(id) ON DELETE CASCADE,
    amount DECIMAL (15, 2) NOT NULL
  );
  """)

print("✅ Schema applied successfully.")

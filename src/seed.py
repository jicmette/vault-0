import auth

def run(cursor):
  print("\n 🌱 Starting Database Seed...")

  bank_email = "admin@vault0.com"

  cursor.execute("SELECT id FROM clients WHERE email = %s", (bank_email,))
  if cursor.fetchone():
    print("⚠️ Seed skipped: Data already exists.")
    return

  print("... Creating 'Vault0' Internal Entity")
  bank_id = auth.create_client(cursor, "Vault 0 Bank", bank_email, "admin123")
  cursor.execute("""
    INSERT INTO accounts (client_id, name, type, balance)
    VALUES (%s, %s, 'Asset', 1000000.00);
  """, (bank_id, "Vault Cash"))
  cursor.execute("""
    INSERT INTO accounts (client_id, name, type, balance)
    VALUES (%s, %s, 'Revenue', 0.00);
    """, (bank_id, "Service Revenue"))
  cursor.execute("""
    INSERT INTO accounts (client_id, name, type, balance)
    VALUES (%s, %s, 'Expense', 0.00);
    """, (bank_id, "Operations Expense"))

  print("✅ Bank Accounts Created (Vault, Revenue, Expense)")

  print("... Creating Customers")

  alice_id = auth.create_client(cursor, "Alice Anderson", "alice@test.com", "alice123")
  cursor.execute("""
    INSERT INTO accounts (client_id, name, type, balance)
    VALUES (%s, %s, 'Liability', -5000.00);
    """, (alice_id, 'Alice Checking'))

  bob_id = auth.create_client(cursor, "Bob Builder", "bob@test.com", "bob123")
  cursor.execute("""
    INSERT INTO accounts (client_id, name, type, balance)
    VALUES (%s, %s, 'Liability', -150.00);
    """, (bob_id, "Bob Savings"))

  print(f"✅ Customers Created: Alice, Bob)")
  print("🌱 Seed Complete! The Vault is populated.")


import ledger
from decimal import Decimal

def get_vault_id(cursor):
  cursor.execute("SELECT id FROM accounts WHERE name = 'Vault Cash';")
  result = cursor.fetchone()
  if not result:
    raise ValueError("Vault Cash account not foundyes! Did you run seed.py?")
  return result[0]

def deposit(cursor, account_id, amount):
  amount = Decimal(str(amount))
  if amount <= 0:
    raise ValueError("Amount must be positive.")

  vault_id = get_vault_id(cursor)

  # Bank Cash (+), User Debt (-)
  entries = [
    (vault_id, amount),
    (account_id, -amount)
  ]

  return ledger.post_transaction(cursor, "Deposit", entries)

def withdraw(cursor, account_id, amount):
  amount = Decimal(str(amount))
  if amount <= 0:
    raise ValueError("Amount must be positive.")

  vault_id = get_vault_id(cursor)

  cursor.execute("SELECT balance FROM accounts WHERE id = %s", (account_id,))
  current_balance = cursor.fetchone()[0]

  if (current_balance + amount) > 0:
    raise ValueError("Insuficient funds.")

  # Bank Cash (-), User Debt (+)
  entries = [
    (vault_id, -amount),
    (account_id, amount)
  ]

  return ledger.post_transaction(cursor, "Withdrawal", entries)






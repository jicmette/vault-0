from decimal import Decimal

def post_transaction(cursor, description, entries):
  total_amount = sum(Decimal(str(amount)) for _, amount in entries)

  if total_amount != 0:
    raise ValueError(f"Transaction Unbalanced! Sum is {total_amount}, but must be 0.")

  try:
    print(f"📝 Posting Transaction: '{description}'")
    cursor.execute("""
      INSERT INTO transactions (description)
      VALUES (%s)
      RETURNING id;
    """, (description,))
    transaction_id = cursor.fetchone()[0]

    for account_id, amount in entries:
      cursor.execute("""
        INSERT INTO entries (transaction_id, account_id, amount)
        VALUES (%s, %s, %s);
        """, (transaction_id, account_id, amount))

      cursor.execute("""
        UPDATE accounts
        SET balance = balance + %s
        WHERE id = %s
        """, (amount, account_id))

    print(f"✅ Transaction #{transaction_id} Posted Successfully.")
    return transaction_id

  except Exception as e:
    print(f"❌ Transaction Failed {e}")
    raise e



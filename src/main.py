import db
import schema
import auth
import sys
import getpass
import seed
import ops
from tabulate import tabulate

def main():
  conn = db.get_db_connection()
  if not conn:
    print("❌ Could not connect to the database.")
    return

  try:
    with conn.cursor() as cursor:
      schema.create_tables(cursor)
      conn.commit()
    print("✅ Vault 0 is Online")
  except Exception as e:
    print(f"❌ Error initializing system: {e}")

  current_user = None

  while True:
    if current_user is None:
      print("\n=== 🔒 VAULT 0: SECURE LOGIN ===")
      print("[1] Login")
      print("[2] Register New Client")
      print("[3] Exit")
      print("[9] RESET & SEED DATA (Dev Only)")

      choice = input("Select an option: ")

      if choice == '1':
        print("\n=== LOGIN ===")
        email = input("Email: ")
        password = getpass.getpass("Password: ")
        with conn.cursor() as cursor:
          user = auth.login(cursor, email, password)
        if user:
          print(f"✅ Welcome back, {user['name']}!")
          current_user = user
        else:
          print("❌ Invalid email or password.")
      elif choice == '2':
        print("\n=== NEW CLIENT REGISTRATION ===")
        name = input("Full Name: ")
        email = input("Email: ")
        password = getpass.getpass("Password: ")
        try:
          with conn.cursor() as cursor:
            new_id = auth.create_client(cursor, name, email, password)
            if new_id:
              cursor.execute("""
                INSERT INTO accounts (client_id, name, type, balance)
                VALUES (%s, %s, 'Liability', 0.00);
              """, (new_id, f"{name} Checking"))
              conn.commit()
              print(f"✅ Registration successful! Created 'Checking Account for {name}")
            else:
              print("❌ Registration failed.")
        except Exception as e:
          print(f"❌ Error during registration: {e}")
          if conn: conn.rollback()
      elif choice == '3':
        print("👋 Goodbye!")
        break
      elif choice == '9':
        confirm = input("⚠️ WARNING: This will wipe the database. Type 'yes' to confirm: ")
        if confirm == 'yes':
          with conn.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS entries CASCADE;")
            cursor.execute("DROP TABLE IF EXISTS transactions CASCADE;")
            cursor.execute("DROP TABLE IF EXISTS accounts CASCADE;")
            cursor.execute("DROP TABLE IF EXISTS clients CASCADE;")

            schema.create_tables(cursor)
            seed.run(cursor)
            conn.commit()
            print("♻️ Database Reset & Seeded successfully.")

    else:
      account_id = None
      balance_display = 0.00

      with conn.cursor() as cursor:
        cursor.execute("""SELECT id, balance FROM accounts
        WHERE client_id = %s AND type = 'Liability'
        LIMIT 1;
        """, (current_user['id'],))
        account = cursor.fetchone()
      if account:
        account_id = account[0]
        balance_display = abs(account[1])
      else:
        print("⚠️ No checking account found for this user.")

      print(f"\n=== 🔓 VAULT 0 DASHBOARD ({current_user['name']}) ===")
      print(f"💰 Balance: ${balance_display:,.2f}")
      print("--------------------------------")
      print("[1] Deposit")
      print("[2] Withdraw")
      print("[3] History")
      print("[4] Monthly Stats")
      print("[5] Log Out")

      choice = input("Select: ")

      try:
        if choice == '1':
          if not account_id:
            print("❌ No account to deposit into.")
            continue

          amount = float(input("Amount to Deposit: $"))
          with conn.cursor() as cursor:
            ops.deposit(cursor, account_id, amount)
            conn.commit()
            print("✅ Deposit Successful!")

        elif choice == '2':
          if not account_id:
            print("❌ No account to withdraw from.")
            continue

          amount = float(input("Amount to Withdraw: $"))

          with conn.cursor() as cursor:
            ops.withdraw(cursor, account_id, amount)
            conn.commit()
            print("✅ Withdrawal Successful!")

        elif choice == '3':
          if not account_id:
            print("❌ No account found.")
            continue

          with conn.cursor() as cursor:
            raw_history = ops.get_history(cursor, account_id)
            clean_history = []
            for row in raw_history:
              date = row[0]
              desc = row[1]
              amount = -row[2]
              clean_history.append([date, desc, amount])
          print("\n📃 TRANSACTION HISTORY (Last 10)")

          if not clean_history:
            print("No transactions found.")
          else: print(tabulate(clean_history, headers=["Date", "Description", "Amount"], tablefmt="psql", floatfmt=".2f"))

          input("\nPress Enter to continue...")

        elif choice == '4':
          if not account_id:
            print("❌ No account found.")
            continue
          with conn.cursor() as cursor:
            stats = ops.get_monthly_stats(cursor, account_id)
            count = stats[0]
            raw_total = stats[1]
            total = -raw_total if raw_total is not None else 0.00

          print(f"\n📊 LAST 30 DAYS ACTIVITY")
          print(f"Total Transactions: {count}")
          print(f"Net Movement: ${total:,.2f}")
          input("\nPress Enter to continue...")

        elif choice == '5':
          print("✅ You logged out.")
          current_user = None

      except ValueError as ve:
        print(f"❌ Operation Error: {ve}")
        if conn: conn.rollback()
      except Exception as e:
        print(f"❌ System Error: {e}")
        if conn: conn.rollback()

  if conn:
    conn.close()
    print("🔒 Connection closed.")


if __name__ == "__main__":
  main()

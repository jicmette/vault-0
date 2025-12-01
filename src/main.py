import db
import schema
import auth
import sys
import getpass

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
        with conn.cursor() as cursor:
          new_id = auth.create_client(cursor, name, email, password)
          conn.commit()
        if new_id:
          print("✅ Registration successful! Please log in.")
      elif choice == '3':
        print("👋 Goobye!")
        break
    else:
      print(f"\n=== 🔓 VAULT 0 DASHBOARD ({current_user['name']}) ===")
      print("[1] Log Out")

      choice = input("Select: ")
      if choice == '1':
        current_user = None

if __name__ == "__main__":
  main()

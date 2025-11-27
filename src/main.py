import db
import schema

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
    conn.rollback()
  finally:
    conn.close()

if __name__ == "__main__":
  main()

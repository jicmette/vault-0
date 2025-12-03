import bcrypt

def create_client(cursor, name, email, password):
  try:
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    query = """
      INSERT INTO clients (name, email, password_hash)
      VALUES (%s, %s, %s)
      RETURNING id;
    """
    cursor.execute(query, (name, email, hashed_password))

    new_id = cursor.fetchone()[0]
    print(f"✅ The Client '{name}' registered successfully (ID: {new_id}).")
    return new_id

  except Exception as e:
    print(f"❌ Error creating client: {e}")
    return None

def login(cursor, email, password):
  try:
    query = "SELECT id, name, password_hash FROM clients WHERE email = %s;"
    cursor.execute(query, (email,))
    user_data = cursor.fetchone()
    if not user_data:
      print(f"❌ Login failed: User not found.")
      return None

    user_id, name, stored_hash = user_data
    if isinstance(stored_hash, memoryview):
      stored_hash = bytes(stored_hash)
    password_bytes = password.encode('utf-8')
    if bcrypt.checkpw(password_bytes, stored_hash):
      print(f"✅ Login Successful! Welcome, {name}.")
      return {"id": user_id, "name": name, "email": email}
    else:
      print(f"❌ Login failed: Incorrect password.")
      return None
  except Exception as e:
    print(f"❌ Error during login {e}")
    return None





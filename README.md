# Vault 0: Core Banking Ledger

**A secure, double-entry banking ledger system built with Python and PostgreSQL.**

This project simulates the core backend of a bank, handling multi-user accounts, ACID-compliant financial transactions, and real-time balance sheet reporting. It enforces strict accounting rules where every transaction must balance (`Sum(Entries) == 0`).

## 🚀 Features

* **Double-Entry Logic:** Every transaction requires balanced debits and credits. Money cannot be created or destroyed, only moved.
* **ACID Compliance:** Uses PostgreSQL transactions (`BEGIN`/`COMMIT`/`ROLLBACK`) to ensure data integrity. If one step fails, the entire transaction is reverted.
* **Financial Reporting:** "Bank Statement" generation using SQL `JOIN`s to merge transaction headers with line-item entries.
* **Secure Authentication:** User passwords are hashed and salted using `bcrypt` before storage.
* **CLI Interface:** A robust interactive menu for user registration, deposits, withdrawals, and history viewing.
* **Dockerized Infrastructure:** The database runs in an isolated Docker container for a reproducible environment.

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Database:** PostgreSQL 15
* **Infrastructure:** Docker & Docker Compose
* **Libraries:**
    * `psycopg2-binary` Raw SQL execution and connection management.
    * `python-dotenv` Configuration management.
    * `bcrypt` Cryptographic password security.
    * `tabulate` Professional data formatting for terminal output.

## ⚙️ Setup & Installation
### 1. Prerequisites
Ensure you have the following installed:
* [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* [Python 3.x](https://www.python.org/downloads/)
* Git

### 2. Clone the Repository
```bash
git clone https://github.com/jicmette/vault-0
cd vault-0
```

### 3. Set up the Database
```bash
docker-compose up -d
```

### 4. Configure Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows - Git Bash)
source venv/Scripts/activate
# OR (Windows - CMD / PowerShell)
.\venv\Scripts\activate

# Activate it (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 5. Initialize the System
```bash
python src/main.py
```

**Developer Note** Select Option `[9]` (RESET & SEED DATA) in the main menu to wipe the database and populate it with test users and correct accounting balances.

## 🛠️ Usage Guide
Once the application is running and seeded, you can log in with the test credentials: Test User (Customer)
* **Email:** `alice@test.com`
* **Password:** `alice123`
* **Role:** Can deposit, withdraw, and view personal transaction history.

## 🧠 The Accounting Logic
This system does not simply add numbers to a `balance` column. It follows the Accounting Equation:

$$Assets = Liabilities + Equity$$

**How Vault 0 Handles Money:** To ensure the mathematical rule $\sum(Entries) = 0$ is always true:

1. **Vault Cash** is an **Asset** (Positive Balance).
2. **Customer Accounts** are **Liabilities** (Negative Balance).
   Why? Because when you deposit money, the bank owes it back to you.

**Display Logic:** The CLI flips the sign for the user.

* **Database stores:** `-5,000.00`
* **User sees:** `$5,000.00`
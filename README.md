# Vault 0: Core Banking Ledger

A secure, double-entry banking ledger system built with Python and PostgreSQL. This project simulates the core backend of a bank, handling multi-user accounts, ACID-compliant financial transactions, and real-time balance sheet reporting.

## 🚀 Features

* **Double-Entry Logic:** Every transaction requires balanced debits and credits. Money cannot be created or destroyed, only moved.
* **ACID Transactions:** Uses PostgreSQL transactions (`BEGIN`/`COMMIT`/`ROLLBACK`) to ensure data integrity.
* **Multi-User Support:** Manage multiple clients, each with their own set of accounts.
* **Secure Authentication:** User passwords are hashed and salted using `bcrypt`.
* **CLI Interface:** A robust command-line interface for users to log in, transfer funds, and view reports.
* **Dockerized Database:** PostgreSQL runs in a Docker container for a clean, consistent environment.

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Database:** PostgreSQL 15
* **Infrastructure:** Docker & Docker Compose
* **Libraries:**
    * `psycopg2-binary` (Database driver)
    * `python-dotenv` (Environment variables)
    * `bcrypt` (Security)
    * `tabulate` (Pretty printing)

## ⚙️ Setup & Installation
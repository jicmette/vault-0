## Module 3: SQL Relational Databases

### Overview
The purpose of this module was to step away from "Backend-as-a-Service" solutions and build a **custom backend infrastructure** from scratch. I focused on mastering **SQL**, **Relational Design**, and **ACID compliance** by simulating a real-world double-entry banking ledger.

**Key Features Implemented:**
1.  **Relational Data Modeling:** Designed a normalized PostgreSQL schema linking `Clients` → `Accounts` → `Entries` → `Transactions` to ensure data integrity.
2.  **ACID Transactions:** Implemented atomic transactions (`BEGIN`/`COMMIT`/`ROLLBACK`) in Python to guarantee that money is never lost or created if a step fails.
3.  **Double-Entry Logic:** Enforced strict accounting rules where every financial movement is balanced by equal debits and credits ($Assets - Liabilities = 0$).
4.  **Complex SQL Queries:**
    * **Joins:** Merged `entries` and `transactions` tables to generate detailed user history reports.
    * **Aggregates & Filtering:** Used `SUM()`, `COUNT()`, and `DATE` filtering to calculate rolling 30-day financial statistics.
5.  **Containerization:** Dockerized the PostgreSQL database to create a reproducible, isolated development environment.

[Software Demo Video - Module 3](https://www.youtube.com/watch?v=7pAjcS2mNkY)

### Development Environment (Module 3)
* **Language:** Python 3.10+
* **Database:** PostgreSQL 15 (Dockerized)
* **Key Libraries:**
    * `psycopg2-binary` (Database Adapter)
    * `bcrypt` (Password Hashing/Security)
    * `tabulate` (CLI Data Formatting)
* **Architecture:** MVC-style separation (Database Layer → Operations Logic → CLI Frontend)
* **Tools:** Docker Desktop, Git/GitHub

## Useful Websites

* [PostgreSQL Documentation](https://www.postgresql.org/docs/)
* [Docker "Get Started" Guide](https://docs.docker.com/get-started/)
* [Psycopg2 Documentation](https://www.psycopg.org/docs/)
* [Python `tabulate` Library](https://pypi.org/project/tabulate/)
* [Double-Entry Bookkeeping Guide](https://en.wikipedia.org/wiki/Double-entry_bookkeeping)
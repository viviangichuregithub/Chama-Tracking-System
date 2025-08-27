# 💰 CHAMA TRACKING SYSTEM 💰

**The Chama Tracking System** is a simple and interactive Command-Line Interface (CLI) project for managing a Kenyan savings group (Chama).
It helps track members, contributions, loans, and repayments, while generating useful reports for transparency and accountability.
This system uses realistic Kenyan data for demonstration and enforces rules that mirror real-world Chama practices.

## Table of Contents
- [Project Overview](#project-overview)  
- [Features](#features)  
- [Installation](#installation)  
- [How to Use](#how-to-use)  
- [Models & Relationships](#models--relationships)  
- [Seeding Data](#seeding-data)  
- [Dependencies](#dependencies)  
- [Future Improvements](#future-improvements)  
- [Author](#author)  
- [License](#license)

## Project Overview

**The CHAMA CLI App** is designed to make it easier for Kenyan savings groups to:
- Manage members and their statuses.
- Record and track contributions.
- Issue and monitor loans with repayment tracking.
- Generate statements and reports for accountability.

The CLI is menu-driven, data-validated, and user-friendly, with built-in safeguards against invalid or risky operations.

## How to Use

**Start the CLI**
```
pipenv shell
python -m lib.cli
```
**Main Menu**

💰 CHAMA MAIN MENU 💸
1. Members
2. Contributions
3. Loans
4. Reports
0. Exit

**Submenus**

- Navigate with numbers (e.g., 1 for Members).
- Use 0 to go back.
- Data is shown in tables for clarity.
- Exit
```
👋 Thanks for Visiting My Chama! Goodbye!
```

## Features
**👥 Member Management**

- Create, view, update, and delete members.
- Track status: ACTIVE, INACTIVE, SUSPENDED.
- Search members by ID or phone.
- View contributions and loans for each member.

**💸 Contributions**

- Record new contributions.
- Delete contributions with confirmation.
- List all contributions or filter by member.
- View total contributions per member.

**💵 Loans**

- Issue loans with plans: 1, 6, or 12 months, each with interest rates.
- Loan conditions:
    - Must be in Chama ≥ 2 months.
    - Can only borrow up to 3× contributions.
    - Only one active loan per member.
    - Chama can only issue loans up to 50% of total contributions.
- Track loan balance and status (ACTIVE, PAID, DEFAULTED).
- Record repayments (prevents overpayment).
- Automatically mark overdue loans as DEFAULTED.

**📊 Reports**

- Member Statement: shows contributions, loans, repayments, balances.
- Group Totals: total contributions, loans issued, outstanding balance.
- Members in Arrears: list of defaulted loans and overdue members.

## Installation

Clone the repository:
```
git clone https://github.com/viviangichuregithub/Chama-Tracking-System.git
cd Chama-Tracking-System
```
Install dependencies:
```
pipenv install
pipenv shell
```
## Models & Relationships
**Member**
- Fields: id, name, phone, join_date, status
- Relations: contributions, loans
- Validations: name ≥ 2 chars, phone normalized to +2547…

**Contribution**
- Fields: id, member_id, amount, date
- Relations: belongs to a member

**Loan**
- Fields: id, member_id, amount, issued_date, due_date, interest_rate, status, balance
- Relations: has many repayments

**Repayment**
- Fields: id, loan_id, amount, date
- Relations: belongs to a loan

## Seeding Data
- The project includes a seed script that generates realistic Kenyan data using Faker:
- Members: 20–40 (with Kenyan names & valid phones)
- Contributions: 100–200
- Loans: 20–40 (with mixed statuses & due dates)
- Repayments: 60–120

## Dependencies
- Python 3.8
- Pipenv (dependency management)
- SQLAlchemy (ORM)
- Faker (data seeding)
- Tabulate (tables in CLI)

## Future Improvements
- User authentication & role-based access (Admin vs Member).
- Export reports to CSV or PDF.
- Enhanced loan repayment schedules.
- Web or mobile integration.

## 👨‍💻 Author

Created by Vivian Gichure

## 📄 License

MIT License
Copyright (c) 2025 viviangichuregithub

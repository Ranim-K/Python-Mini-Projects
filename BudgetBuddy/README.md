# 💰 Budget Buddy

A simple terminal-based **money manager** written in Python.  
It helps you track expenses, manage balances, and split deposits into different jars (Daily, Family, LongTerm, BankAccount).  

---

## ✨ Features
- Add money → split automatically into jars (rounded to nearest 5 DA).  
- Take money → log expenses with category & description.  
- Deposit LongTerm funds into BankAccount (if ≥ 2000 DA).  
- Persistent storage with **CSV** (expenses, deposits) and **JSON** (balances).  
- Clean CLI with ASCII banner.  

---

## 📦 Requirements
No external libraries needed — only Python standard library.  

---

## ▶️ Usage
Run the program:

```bash
python budget_buddy.py

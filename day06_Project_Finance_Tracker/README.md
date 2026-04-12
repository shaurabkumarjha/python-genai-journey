# 💰 Personal Finance Tracker
### Python → Gen AI Engineer Journey | Day 6 Project

> A CLI-based personal finance tracker built from scratch using only Python's standard library.
> This project consolidates every concept covered in Days 1–5 of a structured 90-day journey toward becoming a Gen AI Engineer.

---

## 📌 What Problem Does This Solve?

Most people lose track of where their money goes. Spreadsheets are tedious. Finance apps are bloated. This project solves that with a clean, minimal command-line tool that:

- Tracks income and expenses across meaningful categories
- Persists all data to a local JSON file — nothing is lost between sessions
- Calculates your balance automatically
- Handles invalid inputs gracefully — no crashes, just clear error messages
- Generates a spending analysis report using asynchronous Python — the same pattern used in real Gen AI applications

**No third-party libraries. No frameworks. Pure Python.**

---

## 🗂️ Project Structure

```
day06_project_finance_tracker/
│
├── 📓 day06_finance_tracker.ipynb   ← Complete Google Colab notebook
└── 📄 README.md                     ← This file
```

The notebook is organized into logical sections that mirror a real multi-file project:

| Cell / Step | Equivalent File | Responsibility |
|---|---|---|
| Step 0 | — | Library imports |
| Step 1 | `config.py` | Logging configuration |
| Step 2 | `exceptions.py` | Custom exception classes |
| Step 3 | `models.py` | `Transaction` dataclass |
| Step 4 | `file_utils.py` | JSON save / load with error handling |
| Step 5 | `tracker.py` | Core `FinanceTracker` class |
| Step 6 | `async_report.py` | Async spending report generator |
| Step 7 | `display.py` | CLI display helper functions |
| Step 8 | `main.py` | Interactive menu loop |
| Step 9 | — | Automated demo — runs without any input |
| Step 10 | — | Interactive mode — user-driven |
| Step 11 | — | Concepts revision summary |

---

## 🚀 How to Run

### Option 1 — Google Colab (Recommended)

1. Download `day06_finance_tracker.ipynb`
2. Go to [colab.research.google.com](https://colab.research.google.com)
3. Click **File → Upload notebook** and select the file
4. Click **Runtime → Run All**
5. Step 9 runs an automated demo — no input required
6. Step 10 launches the interactive CLI — enter your name and start exploring

### Option 2 — Run Locally

```bash
# Requires Python 3.8+
python --version

# Open with Jupyter
jupyter notebook day06_finance_tracker.ipynb

# Or convert to a .py script and run directly
jupyter nbconvert --to script day06_finance_tracker.ipynb
python day06_finance_tracker.py
```

---

## 📚 Concepts Applied — Days 1 Through 5

This is not a tutorial project. Every concept listed below is actively used in a meaningful way — not just demonstrated for the sake of it.

---

### Day 1 — Python Core Fundamentals

| Concept | Where It's Used |
|---|---|
| Variables and data types | Transaction fields — `amount: float`, `category: str`, `description: str` |
| `if / elif / else` | Balance surplus vs deficit check, menu routing, input validation |
| `while` loop | Main menu loop — runs until the user chooses to exit |
| `for` loop | Iterating over all transactions to display or calculate |
| Functions | `display_balance()`, `get_float_input()`, `print_header()` and more |
| f-strings | `f"Rs. {tracker.balance:,.2f}"` — formatted, aligned CLI output |
| `input()` and `print()` | The entire interactive CLI interface |
| Docstrings | Every class and function is documented explaining its purpose |

---

### Day 2 — Data Structures

| Concept | Where It's Used |
|---|---|
| List | `self._transactions = []` — the primary data store for all transactions |
| Dictionary | `{"food": {"total": 6700.0, "count": 2, "type": "expense"}}` — category summary |
| Set | `{t.category for t in self._transactions}` — extracting unique categories |
| List comprehension | Filtering transactions by type or category in a single readable line |
| Dict comprehension | Building the category summary from the transaction list |
| Set comprehension | `categories_used` property — unique categories with O(1) lookup |
| `sorted()` with `key` | Sorting the category summary by total amount, highest first |
| `.get()` on dict | `data.get("transactions", [])` — safe access without `KeyError` |

---

### Day 3 — Pythonic Thinking + OOP

| Concept | Where It's Used |
|---|---|
| `@dataclass` | `Transaction` class — auto-generates `__init__`, `__repr__`, and `__eq__` |
| `__init__` | `FinanceTracker` constructor — sets up user name and loads existing data from file |
| `__str__` | `print(transaction)` produces a clean, formatted one-line summary |
| `__repr__` | `repr(tracker)` shows balance and user name for debugging purposes |
| `__len__` | `len(tracker)` returns the total number of transactions |
| `__iter__` | `for t in tracker:` — the tracker object itself is directly iterable |
| `@property` | `tracker.balance`, `tracker.total_income` — computed on access, not stored |
| `@classmethod` | `Transaction.from_dict(data)` — alternate constructor for loading from JSON |
| Generator (`yield`) | `transaction_generator()` — yields one transaction at a time, memory-efficient |
| Inheritance | `InvalidAmountError(FinanceTrackerError)` — structured custom exception hierarchy |
| Encapsulation | `_validate_input()`, `_save_data()` — private methods follow `_` convention |
| Class variables | `VALID_INCOME_CATEGORIES`, `VALID_EXPENSE_CATEGORIES` — shared across all instances |
| `**kwargs` unpacking | `Transaction(**data)` — unpacks a dictionary directly into constructor arguments |
| `field()` from dataclasses | `default_factory=lambda: datetime.now()` — unique default value per instance |

---

### Day 4 — Error Handling + Modules + File Handling

| Concept | Where It's Used |
|---|---|
| Custom exceptions | `InvalidAmountError`, `InvalidCategoryError`, `FileLoadError` |
| Exception inheritance | All custom exceptions extend `FinanceTrackerError` — catchable as a group |
| `try / except` | Wraps every file operation and every user input prompt |
| Multiple `except` blocks | `ValueError`, `PermissionError`, `JSONDecodeError` handled separately and specifically |
| `raise ... from ...` | `raise FileLoadError(...) from e` — preserves the original traceback |
| JSON write | `json.dump(data, f, indent=2, ensure_ascii=False)` — human-readable output |
| JSON read | `json.load(f)` with safe fallback using `.get()` |
| `with open(...)` | Context manager ensures the file is always closed, even when an error occurs |
| `logging` module | `logger.info()`, `logger.warning()`, `logger.error()` — production-style logging |
| Log levels | `DEBUG`, `INFO`, `WARNING`, `ERROR` — no bare `print()` statements in application logic |
| `encoding="utf-8"` | Ensures special characters are handled correctly across all operating systems |

---

### Day 5 — Standard Library + Async Python

| Concept | Where It's Used |
|---|---|
| `datetime.now()` | Auto-generated timestamp attached to every transaction on creation |
| `strftime()` | `"%Y-%m-%d %H:%M"` — converts datetime to a human-readable string |
| `pathlib.Path` | `DATA_FILE = Path("finance_data.json")` — cross-platform path handling |
| `.exists()` | Checks whether the data file exists before attempting to open it |
| `.stat()` | Retrieves file size and last-modified timestamp for the info panel |
| `async def` | `fetch_spending_analysis()` — defines a non-blocking coroutine |
| `await` | Suspends execution at the call site until the coroutine returns |
| `asyncio.sleep()` | Simulates real API network latency — same pattern as calling OpenAI or Anthropic |
| `asyncio.gather()` | Runs all category analyses concurrently — not sequentially |
| Generator expression | `sum(t.amount for t in transactions if ...)` — lazy, memory-efficient calculation |

---

## 🔄 Application Flow

```
User selects an option from the menu
            │
            ▼
handle_add_transaction() prompts for type, category, amount, description
            │
            ▼
_validate_input() checks all values against business rules
            │
     ┌──────┴──────┐
  Invalid         Valid
     │               │
     ▼               ▼
Raises a custom   Transaction object is created via @dataclass
exception with         │
a clear message        ▼
                  Appended to self._transactions  (List)
                       │
                       ▼
                  save_transactions()  →  writes to finance_data.json
                       │
                       ▼
                  Display updates — balance, confirmation, new summary
```

---

## 💾 Data Persistence

All data is saved to `finance_data.json` in the working directory.

```json
{
  "last_saved": "2025-01-15 14:30:00",
  "total_transactions": 3,
  "transactions": [
    {
      "transaction_type": "income",
      "category": "salary",
      "amount": 50000.0,
      "description": "Monthly salary — TCS",
      "date": "2025-01-15 09:00",
      "transaction_id": "TXN-20250115090000123"
    }
  ]
}
```

Every time a transaction is added or deleted, the file is updated immediately. On the next launch, data is loaded automatically — no manual export or import required.

---

## ⚠️ Error Handling in Practice

```python
# Negative amount
tracker.add_transaction("expense", "food", -500, "lunch")
# → InvalidAmountError: Amount must be positive! Got: -500.0

# Unrecognized category
tracker.add_transaction("expense", "gaming", 1000, "PS5 game")
# → InvalidCategoryError: 'gaming' is not valid.
#   Choose from: education, entertainment, food, health, rent...

# Corrupted data file
load_transactions()
# → FileLoadError: Could not parse 'finance_data.json'. File may be corrupted.
```

No unhandled exception reaches the user. Every failure produces a clear, specific, and actionable message.

---

## ⚡ Why Async? The Gen AI Connection

```python
async def generate_full_report(tracker: FinanceTracker) -> dict:
    tasks = [
        fetch_spending_analysis(category, amount)
        for category, amount in expense_categories
    ]
    # All tasks fire simultaneously — not one after another
    analyses = await asyncio.gather(*tasks)
```

In a production Gen AI application, `fetch_spending_analysis()` would be a call to an LLM API such as OpenAI or Anthropic. Using `asyncio.gather()` means all API calls are dispatched in parallel — reducing total response time from `n × latency` to approximately `1 × latency`.

This project simulates that exact pattern using `asyncio.sleep()` as a stand-in for real network latency. The structure of the code is identical to what you would write against a live API.

---

## 📊 Sample Output

```
============================================================
  💰 BALANCE SUMMARY
============================================================
  👤 User           : Rahul Sharma
  📈 Total Income   : Rs.      61,000.00
  📉 Total Expenses : Rs.      37,799.00
------------------------------------------------------------
  🟢 Balance (SURPLUS) : Rs.      23,201.00
------------------------------------------------------------

============================================================
  📊 CATEGORY-WISE SUMMARY
============================================================
  Category             Type         Amount        Count
------------------------------------------------------------
  📉 rent              expense    Rs. 15,000.00     1x
  📉 food              expense    Rs.  6,700.00     2x
  📉 shopping          expense    Rs.  4,200.00     1x
  📈 salary            income     Rs. 50,000.00     1x
  📈 freelance         income     Rs.  8,000.00     1x
------------------------------------------------------------
```

---

## 🏗️ Journey So Far

| Day | Topic | Key Outcome |
|---|---|---|
| Day 1 | Python Core Fundamentals | Syntax, control flow, functions, I/O |
| Day 2 | Data Structures | Lists, dicts, sets, comprehensions |
| Day 3 | OOP + Pythonic Python | Classes, generators, dunder methods, encapsulation |
| Day 4 | Error Handling + File I/O | Custom exceptions, JSON persistence, logging |
| Day 5 | Standard Library + Async | `datetime`, `pathlib`, `asyncio`, concurrency |
| **Day 6** | **This Project** | **All of the above applied to a real, working product** |

---

## 🗓️ What's Next

```
Day 7  → NumPy + Pandas                      Data manipulation and analysis
Day 8  → Data Visualization                  Matplotlib, Seaborn
Day 9  → REST APIs + requests library        Consuming external data sources
Day 10 → API Mini Project
  ...
Day 30 → Machine Learning fundamentals
  ...
Day 60 → LLM APIs — OpenAI, Anthropic        Calling real AI models
  ...
Day 90 → Full-stack Gen AI application       Portfolio complete, job-ready
```

---

## 👤 About This Project

This repository is part of a **90-day structured self-learning journey** — starting from Python fundamentals and working toward production-ready Gen AI engineering.

Every project here is built without following tutorials. The approach is to understand a concept deeply, then apply it to a real problem. The goal is not just to write code that works, but to write code that is readable, maintainable, and structured the way professional teams expect it.

---

*If you are reviewing this as a recruiter or fellow engineer — thank you for your time.
This repository is a live record of consistent, deliberate practice. Feedback is always welcome.*

`#Python` `#GenAI` `#100DaysOfCode` `#BuildInPublic` `#LearningInPublic`

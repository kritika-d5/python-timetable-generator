
# 🗓️ Weekly Timetable Generator

This Python project generates a weekly timetable for multiple batches based on user-inputted course, faculty, and frequency data. It utilizes the `PrettyTable` library for clean, tabular output and ensures that scheduling avoids conflicts while satisfying each course's required frequency.

---

## ✨ Features

- Input-based configuration of **courses**, **faculties**, and **batches**
- Supports weekly frequency (1–5 sessions) per course
- Randomized but **conflict-free** timetable generation
- Outputs a clear, structured table using `PrettyTable`

---

## 🧠 Concepts Used

- String handling and validation
- `random` module for shuffling time slots
- **Dynamic schedule generation**
- Tabular display with `PrettyTable`

---

## 📦 Dependencies

- Python 3.x
- [`prettytable`](https://pypi.org/project/prettytable/)

Install with:
```bash
pip install prettytable
timetable generator using relations

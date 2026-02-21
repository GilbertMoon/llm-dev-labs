# labs/lab01/calc.py
"""
Intentionally imperfect sample code for Lab 01.
We will NOT modify it in this session.
We only ask an LLM to propose refactoring ideas and log them.
"""

def divide(a, b):
    # Intentionally missing validation and error handling
    return a / b

def parse_and_sum(csv_numbers: str):
    # csv_numbers example: "1,2,3"
    # Intentionally missing edge-case handling (spaces, empty items, non-numeric)
    parts = csv_numbers.split(",")
    total = 0
    for p in parts:
        total += int(p)  # may raise ValueError
    return total

if __name__ == "__main__":
    print("divide(10, 2) =", divide(10, 2))
    print('parse_and_sum("1,2,3") =', parse_and_sum("1,2,3"))
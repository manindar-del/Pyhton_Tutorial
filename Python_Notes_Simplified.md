# Python Made Simple — Easy Notes for Beginners
*(Simplified version of the Ultimate Python Course notes)*

---

## Chapter 0: What is Programming?

**In simple words:** You're just telling the computer exactly what to do, step by step. Python is one of the languages we use to write those instructions — it's popular because it reads almost like English.

- Computers only understand 0s and 1s. Python translates your code into that.
- You write code in `.py` files and run them.

---

## Chapter 1: Modules, Comments & pip

**In simple words:** Comments are notes for humans (Python ignores them). Modules are ready-made toolkits you can import instead of writing everything yourself. `pip` is how you download extra toolkits made by other people.

```python
# This is a comment — Python skips this line
print("Hello, World!")

import math
print(math.sqrt(16))   # 4.0

from random import randint
print(randint(1, 10))  # random number 1-10
```

**pip commands (installing tools):**
```bash
pip install requests
pip list
pip uninstall requests
```

👉 **Remember:** A module = a file full of reusable code. `pip` = app store for Python.

---

## Chapter 2: Variables and Datatypes

**In simple words:** A variable is a labeled box that holds a value. Python is smart enough to guess what *type* of value it is (text, number, etc.) automatically.

```python
name = "Harry"     # text (str)
age = 25            # whole number (int)
height = 5.9         # decimal number (float)
is_coder = True       # True/False (bool)
```

**Math operators:**
| Symbol | Meaning | Example | Result |
|---|---|---|---|
| `+` | Add | `10+3` | 13 |
| `-` | Subtract | `10-3` | 7 |
| `*` | Multiply | `10*3` | 30 |
| `/` | Divide | `10/3` | 3.33 |
| `//` | Divide, drop decimals | `10//3` | 3 |
| `%` | Remainder | `10%3` | 1 |
| `**` | Power | `10**2` | 100 |

```python
user_age = input("Enter your age: ")   # always comes in as text!
user_age = int(user_age)                # convert to number
```

👉 **Remember:** `input()` always gives text — convert it if you need a number.

---

## Chapter 3: Strings (Text)

**In simple words:** A string is just text. You can grab parts of it, change its case, or search inside it.

```python
s = "Hello, World!"

s[0]        # 'H'  → first letter
s[-1]       # '!'  → last letter
s[0:5]      # 'Hello' → letters 0 to 4
s[::-1]     # reverses the whole string
```

**Handy string tools:**
```python
s.upper()             # ALL CAPS
s.lower()             # all lowercase
s.replace("a", "b")   # swap text
s.split(",")          # break into a list
len(s)                # how many characters
```

**Best way to insert values into text (f-strings):**
```python
name = "Alice"
print(f"{name} is 25 years old")
```

👉 **Remember:** Strings can't be edited directly — every method gives you a brand-new string.

---

## Chapter 4: Lists and Tuples

**In simple words:** Both hold multiple items in order. **Lists** can be changed after creation. **Tuples** are locked — once made, they can't change.

```python
fruits = ["apple", "banana", "cherry"]
fruits.append("date")     # add item
fruits.remove("banana")    # delete item
fruits.sort()                # sort them
```

```python
point = (3, 4)      # tuple — can't be changed
x, y = point          # unpack values
```

👉 **Remember:** Use a **list** for things that change (a to-do list). Use a **tuple** for things that shouldn't (like GPS coordinates).

---

## Chapter 5: Dictionary & Sets

**In simple words:** A dictionary stores information as **label: value** pairs, like a real dictionary (word → meaning). A set stores only unique items — no duplicates allowed.

```python
person = {"name": "Harry", "age": 25}
person["age"] = 26          # update
person["email"] = "h@x.com"  # add new
del person["name"]            # remove

for key, value in person.items():
    print(f"{key}: {value}")
```

```python
s1 = {1, 2, 3}
s2 = {3, 4, 5}
s1 | s2   # union: combine all
s1 & s2   # intersection: only shared items
```

👉 **Remember:** Dictionary = lookup by name. Set = automatic duplicate remover.

---

## Chapter 6: Making Decisions (Conditionals)

**In simple words:** This is how your program chooses what to do based on a condition — just like "if it's raining, take an umbrella."

```python
age = 20
if age >= 18:
    print("Adult")
elif age >= 13:
    print("Teenager")
else:
    print("Child")

# Shortcut (ternary)
status = "Adult" if age >= 18 else "Minor"
```

👉 **Remember:** `==` checks if two things are equal. `=` assigns a value. Mixing these up is the #1 beginner mistake.

---

## Chapter 7: Loops (Repeating Things)

**In simple words:** Loops let you repeat an action without copy-pasting code.

```python
for i in range(5):        # runs for 0,1,2,3,4
    print(i)

count = 0
while count < 5:            # repeats until condition is false
    print(count)
    count += 1
```

**Control words:**
- `break` → stop the loop completely
- `continue` → skip to the next round

```python
for i in range(10):
    if i == 5:
        break
    if i % 2 == 0:
        continue
    print(i)
```

👉 **Remember:** Use `for` when you know how many times to repeat. Use `while` when you don't.

---

## Chapter 8: Functions & Recursion

**In simple words:** A function is a mini-program you can reuse by giving it a name. Recursion is a function that calls *itself* to break a big problem into smaller pieces.

```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Alice"))     # Hello, Alice!
```

```python
def factorial(n):
    if n <= 1:            # base case (stops the recursion)
        return 1
    return n * factorial(n - 1)

print(factorial(5))   # 120
```

👉 **Remember:** Every recursive function *must* have a stopping point (base case), or it will run forever and crash.

**🎮 Project: Snake, Water, Gun**
A rock-paper-scissors style game — good practice for combining functions, conditionals, and randomness.

---

## Chapter 9: Reading & Writing Files

**In simple words:** This is how your program saves information permanently (in a file) instead of losing it when the program closes.

```python
with open("data.txt", "w") as f:   # "w" = write (overwrites)
    f.write("Hello, File!\n")

with open("data.txt", "r") as f:    # "r" = read
    content = f.read()
    print(content)
```

**Modes cheat sheet:** `"r"` read · `"w"` write (erases old content) · `"a"` append (adds to end)

👉 **Remember:** Always use `with open(...)` — it automatically closes the file for you, even if something goes wrong.

---

## Chapter 10: Object-Oriented Programming (OOP) Basics

**In simple words:** OOP lets you create your own custom "types" (called classes) that bundle data and actions together — like a blueprint for making objects.

```python
class Dog:
    def __init__(self, name, breed):   # runs automatically when creating a Dog
        self.name = name
        self.breed = breed

    def bark(self):
        return f"{self.name} says Woof!"

d1 = Dog("Rex", "Labrador")
print(d1.bark())   # Rex says Woof!
```

👉 **Remember:** `self` = "this specific object." `__init__` = the setup that runs when you create something new.

---

## Chapter 11: Inheritance (Reusing Classes)

**In simple words:** A class can inherit features from another class, so you don't repeat yourself. It's like a child class being a specialized version of a parent class.

```python
class Animal:
    def speak(self):
        return "makes a sound"

class Dog(Animal):            # Dog inherits from Animal
    def speak(self):            # but overrides the behavior
        return "barks"

print(Dog().speak())   # barks
```

**Keeping data private (encapsulation):**
```python
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance    # double underscore = private

    def get_balance(self):
        return self.__balance
```

👉 **Remember:** `_var` = "please don't touch this from outside." `__var` = Python actively hides it.

**🎮 Project: Number Guessing Game** — combines loops, conditionals, and randomness.

---

## Chapter 12: Handling Errors & Smarter Loops

**In simple words:** Real programs crash sometimes — this chapter teaches you to catch errors gracefully instead of letting the program die.

```python
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Error: {e}")
finally:
    print("This always runs, error or not")
```

**Comprehensions (shortcut for building lists):**
```python
squares = [x**2 for x in range(10)]   # instead of a whole loop
```

**Generators (memory-saving loops):**
```python
def count_up_to(n):
    i = 1
    while i <= n:
        yield i     # gives one value at a time instead of all at once
        i += 1
```

👉 **Remember:** `try/except` = "attempt this, but don't crash if it fails."

---

## Chapter 13: Pro-Level Tools

**In simple words:** These are tools professional developers use to write cleaner, more powerful code.

**Decorators** — add extra behavior to a function without changing its code:
```python
def my_decorator(func):
    def wrapper():
        print("Before")
        func()
        print("After")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

say_hello()
```

**Context managers** — like `with open()`, but for your own custom setup/cleanup logic.

**🎮 Mega Projects:** Jarvis (voice assistant) and an Auto-Reply Chatbot — these combine everything you've learned so far into real applications.

---

## Wrapping Up

You've gone from "what is programming" to building your own classes, handling files, and writing chatbots. Next steps:

1. Rebuild the mini projects **without** looking at the notes.
2. Read your old code and try to improve it.
3. Pick a direction: web dev, data science, automation, or AI.
4. Practice on LeetCode/HackerRank for interview prep.

---
*This is a simplified companion to the original detailed notes — same topics, explained in plain language for quick review.*
===================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================


Absolutely. Below are **beginner-friendly notes in learning order**. Since you already understand Python basics, OOP, polymorphism, lambda, `map()`, `filter()`, and `reduce()`, these topics will take you from basic Python toward building real applications and APIs.

# Python Intermediate → Backend Notes

## 1. Exception Handling

### What is an exception?

An exception is an error that happens **while your program is running**.

For example:

```python
a = 10
b = 0

print(a / b)
```

You get:

```text
ZeroDivisionError
```

Normally, the program stops. Exception handling allows you to handle the problem gracefully.

### `try` and `except`

```python
try:
    a = 10
    b = 0
    print(a / b)

except ZeroDivisionError:
    print("Cannot divide by zero")
```

Think:

```text
try
 ↓
Try running this code
 ↓
Error?
 ├── No  → continue
 └── Yes → except
```

### Multiple exceptions

```python
try:
    number = int(input("Enter number: "))
    result = 100 / number
    print(result)

except ValueError:
    print("Please enter a number")

except ZeroDivisionError:
    print("Number cannot be zero")
```

### `else`

`else` executes when there is **no exception**.

```python
try:
    number = int(input("Enter number: "))

except ValueError:
    print("Invalid number")

else:
    print("You entered:", number)
```

### `finally`

`finally` executes **whether an error occurs or not**.

```python
try:
    print(10 / 2)

except ZeroDivisionError:
    print("Error")

finally:
    print("Program finished")
```

Commonly used for cleanup, such as closing files or database resources.

### `raise`

You can create an error yourself.

```python
age = 15

if age < 18:
    raise ValueError("Age must be 18 or above")
```

### Remember

```text
try      → code that might fail
except   → handle error
else     → execute when no error
finally  → always execute
raise    → manually create an exception
```

---

# 2. `*args` and `**kwargs`

These allow functions to accept a flexible number of arguments.

## `*args`

Suppose:

```python
def add(a, b):
    return a + b
```

You can only provide two arguments.

What if you want:

```python
add(10, 20, 30, 40, 50)
```

Use `*args`:

```python
def add(*args):
    print(args)


add(10, 20, 30, 40)
```

Output:

```text
(10, 20, 30, 40)
```

`args` becomes a **tuple**.

A useful example:

```python
def add(*numbers):
    total = 0

    for number in numbers:
        total += number

    return total


print(add(10, 20))
print(add(10, 20, 30, 40))
```

Output:

```text
30
100
```

## `**kwargs`

`**kwargs` accepts multiple **named arguments**.

```python
def user_details(**kwargs):
    print(kwargs)


user_details(
    name="John",
    age=25,
    city="Kolkata"
)
```

Output:

```python
{
    "name": "John",
    "age": 25,
    "city": "Kolkata"
}
```

`kwargs` becomes a **dictionary**.

You can access:

```python
def user_details(**kwargs):
    print(kwargs["name"])
    print(kwargs["age"])


user_details(
    name="John", age=25)
```

Remember:

```text
*args
 ↓
Multiple positional arguments
 ↓
Tuple


**kwargs
 ↓
Multiple keyword arguments
 ↓
Dictionary
```

---

# 3. List, Dictionary and Set Comprehensions

Comprehension is a **shorter way of creating collections**.

## Normal list

```python
numbers = []

for i in range(1, 6):
    numbers.append(i * i)

print(numbers)
```

Output:

```text
[1, 4, 9, 16, 25]
```

Using list comprehension:

```python
numbers = [i * i for i in range(1, 6)]

print(numbers)
```

### With condition

```python
numbers = [1, 2, 3, 4, 5, 6]

even = [x for x in numbers if x % 2 == 0]

print(even)
```

Output:

```text
[2, 4, 6]
```

## Dictionary comprehension

```python
numbers = [1, 2, 3, 4]

result = {
    x: x * x
    for x in numbers
}

print(result)
```

Output:

```text
{
    1: 1,
    2: 4,
    3: 9,
    4: 16
}
```

## Set comprehension

```python
numbers = [1, 1, 2, 2, 3, 3]

result = {x * 2 for x in numbers}

print(result)
```

Possible output:

```text
{2, 4, 6}
```

Remember:

```text
[] → List comprehension
{} → Set comprehension
{k:v} → Dictionary comprehension
```

---

# 4. Modules and Packages

As applications become larger, you shouldn't put everything in one `.py` file.

Suppose you have:

```text
calculator.py
main.py
```

`calculator.py`:

```python
def add(a, b):
    return a + b


def subtract(a, b):
    return a - b
```

`main.py`:

```python
import calculator

result = calculator.add(10, 20)

print(result)
```

Or:

```python
from calculator import add

print(add(10, 20))
```

## Module

A Python file is a module.

```text
calculator.py
```

is a module.

## Package

A folder containing Python modules can act as a package.

```text
project/
│
├── main.py
│
└── services/
    ├── __init__.py
    ├── user_service.py
    └── payment_service.py
```

Then:

```python
from services.user_service import create_user
```

Easy definition:

```text
Function
   ↓
Reusable code

Module
   ↓
Python file

Package
   ↓
Collection of modules
```

---

# 5. Decorators

A decorator adds functionality to another function **without directly modifying that function's code**.

Start with:

```python
def hello():
    print("Hello")
```

Suppose you want to print something before and after it.

```python
def logger(func):

    def wrapper():
        print("Function started")

        func()

        print("Function finished")

    return wrapper
```

Use:

```python
@logger
def hello():
    print("Hello")


hello()
```

Output:

```text
Function started
Hello
Function finished
```

Think:

```text
hello()
   ↓
@logger
   ↓
wrapper()
   ↓
Before logic
   ↓
hello()
   ↓
After logic
```

Decorators become very important when you start frameworks such as FastAPI.

---

# 6. Iterators and Generators

## Iterator

An iterator gives values **one at a time**.

```python
numbers = [10, 20, 30]

iterator = iter(numbers)

print(next(iterator))
print(next(iterator))
print(next(iterator))
```

Output:

```text
10
20
30
```

### Iterable vs Iterator

A list is iterable:

```python
numbers = [10, 20, 30]
```

Convert it to an iterator:

```python
iterator = iter(numbers)
```

Then:

```python
next(iterator)
```

retrieves one value.

## Generator

A generator is an easy way to create an iterator.

It uses:

```python
yield
```

Example:

```python
def numbers():

    yield 1
    yield 2
    yield 3


for number in numbers():
    print(number)
```

Output:

```text
1
2
3
```

A more practical example:

```python
def generate_numbers(n):

    for i in range(n):
        yield i


for number in generate_numbers(5):
    print(number)
```

### Why generators?

Suppose you have millions of records.

A normal list might create everything in memory:

```python
numbers = [x for x in range(10000000)]
```

A generator can produce values one by one:

```python
numbers = (x for x in range(10000000))
```

So generators can be memory-efficient.

---

# 7. JSON Handling

JSON is extremely important for web development.

A frontend may send:

```json
{
    "name": "John",
    "age": 25,
    "email": "john@gmail.com"
}
```

Python has the `json` module.

## Dictionary → JSON

```python
import json

user = {
    "name": "John",
    "age": 25
}

result = json.dumps(user)

print(result)
```

## JSON → Dictionary

```python
import json

data = '{"name": "John", "age": 25}'

user = json.loads(data)

print(user["name"])
```

### File operations

Write JSON:

```python
import json

user = {
    "name": "John",
    "age": 25
}

with open("user.json", "w") as file:
    json.dump(user, file, indent=4)
```

Read JSON:

```python
import json

with open("user.json", "r") as file:
    user = json.load(file)

print(user)
```

Remember:

```text
dumps() → Python → JSON string
loads() → JSON string → Python

dump()  → Python → JSON file
load()  → JSON file → Python
```

---

# 8. Date and Time

Python provides the `datetime` module.

```python
from datetime import datetime

now = datetime.now()

print(now)
```

Format date:

```python
from datetime import datetime

now = datetime.now()

print(now.strftime("%d-%m-%Y"))
```

Example output:

```text
14-09-2026
```

Date only:

```python
from datetime import date

today = date.today()

print(today)
```

Create a particular date:

```python
from datetime import date

birthday = date(2000, 5, 20)

print(birthday)
```

Add days:

```python
from datetime import datetime, timedelta

today = datetime.now()

next_week = today + timedelta(days=7)

print(next_week)
```

Common format codes:

| Code | Meaning      |
| ---- | ------------ |
| `%d` | Day          |
| `%m` | Month        |
| `%Y` | 4-digit year |
| `%H` | Hour         |
| `%M` | Minute       |
| `%S` | Second       |

---

# 9. Virtual Environment and pip

This becomes important when creating real projects.

Suppose Project A needs:

```text
FastAPI version X
```

and another project needs different dependencies.

A virtual environment keeps each project's dependencies separate.

Create one:

```bash
python -m venv venv
```

On Windows activate it:

```bash
venv\Scripts\activate
```

Then install:

```bash
pip install requests
```

Check installed packages:

```bash
pip list
```

Create dependency list:

```bash
pip freeze > requirements.txt
```

Later another developer can run:

```bash
pip install -r requirements.txt
```

Think:

```text
Project A
└── venv
    └── its packages

Project B
└── venv
    └── its packages
```

---

# 10. Type Hints

Python doesn't require you to specify types:

```python
def add(a, b):
    return a + b
```

But you can provide type hints:

```python
def add(a: int, b: int) -> int:
    return a + b
```

This means:

```text
a        → expected int
b        → expected int
-> int   → expected return type
```

Another example:

```python
def greet(name: str) -> str:
    return f"Hello {name}"
```

Variables can also have hints:

```python
name: str = "John"
age: int = 25
salary: float = 50000.50
active: bool = True
```

Collections:

```python
names: list[str] = ["John", "David", "Alice"]

user: dict[str, str] = {
    "name": "John",
    "city": "Kolkata"
}
```

Important: type hints mainly help developers and tools understand your intended types; Python does not automatically enforce most annotations at runtime.

---

# 11. Working with APIs using `requests`

This is especially important since you know React/Next.js.

In React you might use:

```javascript
fetch("/api/users")
```

Python can call APIs using `requests`.

Install:

```bash
pip install requests
```

## GET request

```python
import requests

response = requests.get(
    "https://jsonplaceholder.typicode.com/users"
)

print(response.status_code)
```

Get JSON:

```python
users = response.json()

for user in users:
    print(user["name"])
```

## POST request

```python
import requests

user = {
    "name": "John",
    "email": "john@gmail.com"
}

response = requests.post(
    "https://example.com/users",
    json=user
)

print(response.status_code)
print(response.json())
```

## Headers

```python
headers = {
    "Authorization": "Bearer my-token"
}

response = requests.get(
    "https://example.com/users",
    headers=headers
)
```

You should learn these HTTP concepts here:

```text
GET     → retrieve
POST    → create
PUT     → replace/update
PATCH   → partial update
DELETE  → delete

200 → OK
201 → Created
400 → Bad Request
401 → Unauthorized
403 → Forbidden
404 → Not Found
500 → Server Error
```

---

# 12. Database + SQL

Before connecting Python to a database, learn basic SQL.

You need to understand:

```text
CREATE TABLE
INSERT
SELECT
UPDATE
DELETE
WHERE
ORDER BY
GROUP BY
JOIN
PRIMARY KEY
FOREIGN KEY
```

Example:

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);
```

Insert:

```sql
INSERT INTO users (id, name, email)
VALUES (1, 'John', 'john@gmail.com');
```

Read:

```sql
SELECT *
FROM users;
```

Update:

```sql
UPDATE users
SET name = 'David'
WHERE id = 1;
```

Delete:

```sql
DELETE FROM users
WHERE id = 1;
```

These four operations are called:

```text
C → Create
R → Read
U → Update
D → Delete

CRUD
```

## Python + SQLite

Python already includes SQLite support.

```python
import sqlite3

connection = sqlite3.connect("users.db")

cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT
    )
""")

connection.commit()
connection.close()
```

Insert:

```python
import sqlite3

connection = sqlite3.connect("users.db")

cursor = connection.cursor()

cursor.execute(
    "INSERT INTO users (name, email) VALUES (?, ?)",
    ("John", "john@gmail.com")
)

connection.commit()
connection.close()
```

Read:

```python
connection = sqlite3.connect("users.db")

cursor = connection.cursor()

cursor.execute("SELECT * FROM users")

users = cursor.fetchall()

for user in users:
    print(user)

connection.close()
```

Once you understand this, move to PostgreSQL/MySQL and an ORM.

---

# 13. FastAPI

Now everything starts coming together.

Your architecture becomes:

```text
React / Next.js
       ↓
     HTTP
       ↓
    FastAPI
       ↓
 Business Logic
       ↓
   Database
```

Install:

```bash
pip install fastapi uvicorn
```

Create:

```text
main.py
```

Add:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Hello World"
    }
```

Run:

```bash
uvicorn main:app --reload
```

Now you have a Python backend.

## Path parameter

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):

    return {
        "id": user_id
    }
```

Request:

```text
GET /users/10
```

Response:

```json
{
    "id": 10
}
```

## Query parameter

```python
@app.get("/users")
def get_users(name: str = None):

    return {
        "name": name
    }
```

Request:

```text
GET /users?name=John
```

## POST request

FastAPI commonly uses Pydantic models.

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class UserRequest(BaseModel):
    name: str
    email: str
    age: int


@app.post("/users")
def create_user(user: UserRequest):

    return {
        "message": "User created",
        "user": user
    }
```

Frontend sends:

```json
{
    "name": "John",
    "email": "john@gmail.com",
    "age": 25
}
```

FastAPI converts and validates it as a `UserRequest`.

---

# How everything connects

This is the important part. Don't think of these as unrelated chapters.

```text
Exception Handling
        ↓
Handle application errors

*args / **kwargs
        ↓
Flexible functions

Comprehensions
        ↓
Process collections cleanly

Modules / Packages
        ↓
Organize large applications

Decorators
        ↓
Add behavior around functions

Generators / Iterators
        ↓
Process data efficiently

JSON
        ↓
Frontend ↔ Backend data

Date / Time
        ↓
Work with timestamps/dates

venv / pip
        ↓
Manage project dependencies

Type Hints
        ↓
Write clearer Python

requests
        ↓
Call external APIs

SQL / Database
        ↓
Store application data

FastAPI
        ↓
Build your backend API
```

## Best practice projects

Don't wait until you've learned everything to build something. After every few topics, make something small.

**After Exceptions + `*args`/`**kwargs` + Comprehensions:** build a Student Marks Calculator that validates input, calculates totals/averages, filters passed students, and handles invalid values.

**After Modules + JSON + Date/Time:** build an Expense Tracker that stores expenses in JSON, records dates, calculates totals, and separates code into modules.

**After SQL:** build a User Management program with Create, Read, Update, Delete and Search.

Then your main project should be:

```text
Employee Management System

Frontend
React / Next.js

        ↓

FastAPI

        ↓

Database

Features:
• Create employee
• Get employees
• Get employee by ID
• Update employee
• Delete employee
• Search employee
• Pagination
• Validation
• Exception handling
```

Once you can build that without copying every line from a tutorial, your next stage should be **Pydantic in depth → SQLAlchemy ORM → PostgreSQL/MySQL → authentication/JWT → pytest → async/await → Docker and deployment**.

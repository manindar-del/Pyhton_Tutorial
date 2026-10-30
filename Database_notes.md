python -m pip install -r requirements.txt
python -m pip freeze > requirements.txt
python -m uvicorn main:app --reload

=====================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================

Absolutely. Since you're learning **Python + FastAPI + PostgreSQL + React**, it's better to understand what every part does rather than just copy the code.

We are building this flow:

```text
React
  │
  │ HTTP request
  ▼
FastAPI
  │
  │ SQLAlchemy
  ▼
PostgreSQL
  │
  └── employee_db
        └── employees
```

For now we need two APIs:

```text
POST /employees  → Add employee
GET  /employees  → Get all employees
```

## 1. Why do we need an API?

Your React application should **not directly connect to PostgreSQL**.

Wrong architecture:

```text
React ───────────► PostgreSQL
```

Correct architecture:

```text
React
   │
   │ HTTP
   ▼
FastAPI
   │
   │ SQL
   ▼
PostgreSQL
```

FastAPI acts as the backend layer. It can validate incoming data, apply business rules, query the database, handle errors, authentication, etc.

For example, React sends:

```json
{
  "name": "Rahul Sharma",
  "email": "rahul@gmail.com",
  "department": "IT",
  "salary": 55000
}
```

FastAPI receives it, validates it, creates a database object, and SQLAlchemy inserts it into PostgreSQL.

---

# 2. Understand the four backend files

I recommend this structure:

```text
backend/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
└── venv/
```

Each file has a different responsibility:

```text
database.py
    ↓
PostgreSQL connection

models.py
    ↓
Database table structure

schemas.py
    ↓
Request/response JSON structure

main.py
    ↓
GET/POST API endpoints
```

This separation becomes very important when your project grows.

---

# 3. `database.py` — connect to PostgreSQL

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = (
    "postgresql://postgres:YOUR_PASSWORD@localhost:5432/employee_db"
)


engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()
```

Let's understand each part.

### `DATABASE_URL`

```python
DATABASE_URL = (
    "postgresql://postgres:YOUR_PASSWORD@localhost:5432/employee_db"
)
```

This tells SQLAlchemy:

```text
postgresql://
     │
     └── Database type

postgres
     │
     └── PostgreSQL username

YOUR_PASSWORD
     │
     └── PostgreSQL password

localhost
     │
     └── PostgreSQL is running on this computer

5432
     │
     └── PostgreSQL port

employee_db
     │
     └── Database name
```

So:

```text
FastAPI
   ↓
SQLAlchemy
   ↓
localhost:5432
   ↓
PostgreSQL
   ↓
employee_db
```

---

# 4. What is `engine`?

```python
engine = create_engine(DATABASE_URL)
```

Think of `engine` as the main communication mechanism between SQLAlchemy and PostgreSQL.

Conceptually:

```text
SQLAlchemy
    │
    │ engine
    ▼
PostgreSQL
```

Without it, SQLAlchemy doesn't know which database to communicate with.

---

# 5. What is `SessionLocal`?

```python
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
```

This is very important.

A **Session** represents a unit of work with the database.

For example:

```text
Request comes
     ↓
Open database session
     ↓
SELECT / INSERT / UPDATE
     ↓
Commit if needed
     ↓
Close session
```

Later you'll see:

```python
db.query(...)
```

and:

```python
db.add(...)
db.commit()
```

`db` is a SQLAlchemy Session.

---

# 6. `models.py` — represent PostgreSQL table

Your PostgreSQL table is:

```text
employees
├── id
├── name
├── email
├── department
└── salary
```

Our Python model:

```python
from sqlalchemy import Column, Integer, String, Numeric

from database import Base


class Employee(Base):

    __tablename__ = "employees"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(150),
        unique=True,
        nullable=False
    )

    department = Column(
        String(100),
        nullable=False
    )

    salary = Column(
        Numeric(10, 2),
        nullable=False
    )
```

The important idea is:

```text
Python                       PostgreSQL

class Employee       ←→      employees table

Employee.id          ←→      id
Employee.name        ←→      name
Employee.email       ←→      email
Employee.department  ←→      department
Employee.salary      ←→      salary
```

This is ORM — **Object Relational Mapping**.

Instead of writing SQL everywhere:

```sql
INSERT INTO employees
(name, email, department, salary)
VALUES (...);
```

you can work with Python:

```python
employee = Employee(
    name="Rahul",
    email="rahul@gmail.com",
    department="IT",
    salary=55000
)
```

SQLAlchemy translates that into database operations.

---

# 7. Why do we need `schemas.py`?

Now suppose React sends:

```json
{
  "name": "Rahul",
  "email": "rahul@gmail.com",
  "department": "IT",
  "salary": 55000
}
```

We need FastAPI to know:

> What fields am I expecting?

That's where Pydantic schemas come in.

```python
from pydantic import BaseModel, EmailStr


class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    department: str
    salary: float


class EmployeeResponse(EmployeeCreate):
    id: int

    class Config:
        from_attributes = True
```

Notice that we have **two different schemas**.

`EmployeeCreate`:

```python
class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    department: str
    salary: float
```

is for incoming data.

React sends:

```json
{
  "name": "Rahul",
  "email": "rahul@gmail.com",
  "department": "IT",
  "salary": 55000
}
```

React doesn't send `id` because PostgreSQL generates it.

But the response contains `id`:

```json
{
  "id": 1,
  "name": "Rahul",
  "email": "rahul@gmail.com",
  "department": "IT",
  "salary": 55000
}
```

Therefore:

```python
class EmployeeResponse(EmployeeCreate):
    id: int
```

means:

```text
EmployeeResponse
├── id
├── name
├── email
├── department
└── salary
```

---

# 8. Why use both Model and Schema?

This is one of the most important things to understand.

`models.py` describes the **database**:

```python
class Employee(Base):
```

`schemas.py` describes the **API data**:

```python
class EmployeeCreate(BaseModel):
```

So:

```text
React JSON
     ↓
Pydantic Schema
     ↓
FastAPI
     ↓
SQLAlchemy Model
     ↓
PostgreSQL
```

Don't think of them as duplicates. They solve different problems.

---

# 9. Now create the database dependency

In `main.py`:

```python
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
```

Why?

Every API request that needs PostgreSQL needs a database session.

When someone calls:

```text
GET /employees
```

we want:

```text
Request
   ↓
Open DB connection/session
   ↓
Execute query
   ↓
Return response
   ↓
Close session
```

This:

```python
db = SessionLocal()
```

opens the session.

This:

```python
yield db
```

makes the session available to the API function.

And:

```python
finally:
    db.close()
```

ensures it gets closed after the request, even if something fails.

---

# 10. GET API

Now the first real API:

```python
@app.get(
    "/employees",
    response_model=list[schemas.EmployeeResponse]
)
def get_employees(
    db: Session = Depends(get_db)
):

    employees = db.query(models.Employee).all()

    return employees
```

Let's understand every line.

### `@app.get`

```python
@app.get("/employees")
```

This tells FastAPI:

> When an HTTP GET request comes to `/employees`, execute the function below.

So:

```text
GET http://127.0.0.1:8000/employees
```

calls:

```python
get_employees()
```

---

# 11. What does `Depends(get_db)` do?

```python
db: Session = Depends(get_db)
```

FastAPI sees:

```python
Depends(get_db)
```

and automatically calls:

```python
get_db()
```

That gives us:

```python
db
```

which is our SQLAlchemy session.

Now we can communicate with PostgreSQL.

---

# 12. Understand the SELECT query

This:

```python
employees = db.query(models.Employee).all()
```

means:

> Get all Employee records.

Conceptually SQLAlchemy executes something similar to:

```sql
SELECT *
FROM employees;
```

So:

```python
db.query(models.Employee)
```

means:

> Query the Employee table.

And:

```python
.all()
```

means:

> Return all matching records.

---

# 13. GET request flow

React eventually does:

```javascript
fetch("http://127.0.0.1:8000/employees");
```

The complete flow is:

```text
React
   │
   │ GET /employees
   ▼
FastAPI
   │
   │ get_employees()
   ▼
SQLAlchemy
   │
   │ SELECT * FROM employees
   ▼
PostgreSQL
   │
   │ rows
   ▼
SQLAlchemy Employee objects
   │
   ▼
Pydantic EmployeeResponse
   │
   ▼
JSON
   │
   ▼
React
```

For example PostgreSQL contains:

```text
1 | Rahul | rahul@gmail.com | IT | 55000
2 | Priya | priya@gmail.com | HR | 45000
```

FastAPI returns:

```json
[
  {
    "id": 1,
    "name": "Rahul",
    "email": "rahul@gmail.com",
    "department": "IT",
    "salary": 55000
  },
  {
    "id": 2,
    "name": "Priya",
    "email": "priya@gmail.com",
    "department": "HR",
    "salary": 45000
  }
]
```

---

# 14. POST API

Now the more interesting one:

```python
@app.post(
    "/employees",
    response_model=schemas.EmployeeResponse,
    status_code=201
)
def create_employee(
    employee: schemas.EmployeeCreate,
    db: Session = Depends(get_db)
):

    new_employee = models.Employee(
        name=employee.name,
        email=employee.email,
        department=employee.department,
        salary=employee.salary
    )

    db.add(new_employee)

    db.commit()

    db.refresh(new_employee)

    return new_employee
```

Now understand it step by step.

---

# 15. What does `@app.post()` mean?

```python
@app.post("/employees")
```

means:

> When someone sends an HTTP POST request to `/employees`, execute `create_employee()`.

React might send:

```text
POST http://127.0.0.1:8000/employees
```

with:

```json
{
  "name": "Amit Kumar",
  "email": "amit@gmail.com",
  "department": "Finance",
  "salary": 60000
}
```

---

# 16. FastAPI converts JSON to Python

This parameter:

```python
employee: schemas.EmployeeCreate
```

tells FastAPI:

> The request body must follow EmployeeCreate.

FastAPI automatically converts:

```json
{
  "name": "Amit Kumar",
  "email": "amit@gmail.com",
  "department": "Finance",
  "salary": 60000
}
```

into an object where you can use:

```python
employee.name
employee.email
employee.department
employee.salary
```

You don't manually parse JSON.

---

# 17. Pydantic also validates it

Suppose React sends:

```json
{
  "name": "Amit",
  "email": "hello",
  "department": "IT",
  "salary": 50000
}
```

Because you defined:

```python
email: EmailStr
```

`hello` isn't a valid email address.

FastAPI/Pydantic rejects the request automatically.

That's one major reason we use schemas.

---

# 18. Create SQLAlchemy object

Next:

```python
new_employee = models.Employee(
    name=employee.name,
    email=employee.email,
    department=employee.department,
    salary=employee.salary
)
```

Here we're converting:

```text
Pydantic EmployeeCreate
          ↓
SQLAlchemy Employee
```

`EmployeeCreate` represents the API request.

`Employee` represents the database row.

---

# 19. What does `db.add()` do?

```python
db.add(new_employee)
```

This tells SQLAlchemy:

> I want this new object inserted into the database.

But this alone doesn't necessarily finalize the database transaction.

Think:

```text
db.add()

"Prepare this record for insertion."
```

---

# 20. What does `db.commit()` do?

```python
db.commit()
```

This is the important database transaction step.

It commits the pending change.

Conceptually SQLAlchemy performs:

```sql
INSERT INTO employees
(
    name,
    email,
    department,
    salary
)
VALUES
(
    'Amit Kumar',
    'amit@gmail.com',
    'Finance',
    60000
);
```

Now the employee is actually persisted in PostgreSQL.

---

# 21. Why `db.refresh()`?

After insertion:

```python
db.refresh(new_employee)
```

PostgreSQL may generate values, especially:

```text
id
```

Before insert:

```text
name = Amit
email = amit@gmail.com
id = ?
```

PostgreSQL inserts:

```text
id = 5
```

`refresh()` reloads the database-generated/current values into the Python object.

Now:

```python
new_employee.id
```

might be:

```text
5
```

---

# 22. Return the employee

Finally:

```python
return new_employee
```

FastAPI uses:

```python
response_model=schemas.EmployeeResponse
```

to convert the SQLAlchemy object into the response JSON.

Result:

```json
{
  "id": 5,
  "name": "Amit Kumar",
  "email": "amit@gmail.com",
  "department": "Finance",
  "salary": 60000
}
```

---

# 23. Why status code 201?

We used:

```python
status_code=201
```

HTTP `201 Created` means:

> A new resource was successfully created.

That's more appropriate than returning ordinary `200 OK` for a successful create operation.

So:

```text
GET successful
→ 200 OK

POST successfully created
→ 201 Created
```

---

# 24. Add duplicate-email validation

Because your database has:

```text
email UNIQUE
```

we should check before inserting.

```python
existing_employee = (
    db.query(models.Employee)
    .filter(models.Employee.email == employee.email)
    .first()
)
```

This roughly corresponds to:

```sql
SELECT *
FROM employees
WHERE email = 'amit@gmail.com'
LIMIT 1;
```

Then:

```python
if existing_employee:
    raise HTTPException(
        status_code=400,
        detail="Email already exists"
    )
```

So the complete POST API becomes:

```python
@app.post(
    "/employees",
    response_model=schemas.EmployeeResponse,
    status_code=201
)
def create_employee(
    employee: schemas.EmployeeCreate,
    db: Session = Depends(get_db)
):

    existing_employee = (
        db.query(models.Employee)
        .filter(
            models.Employee.email == employee.email
        )
        .first()
    )

    if existing_employee:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    new_employee = models.Employee(
        name=employee.name,
        email=employee.email,
        department=employee.department,
        salary=employee.salary
    )

    db.add(new_employee)

    db.commit()

    db.refresh(new_employee)

    return new_employee
```

---

# 25. Complete `main.py`

Putting the important pieces together:

```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import models
import schemas

from database import Base, SessionLocal, engine


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Employee Management API"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:14037",
        "http://127.0.0.1:14037",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@app.get(
    "/employees",
    response_model=list[schemas.EmployeeResponse]
)
def get_employees(
    db: Session = Depends(get_db)
):

    employees = db.query(
        models.Employee
    ).all()

    return employees


@app.post(
    "/employees",
    response_model=schemas.EmployeeResponse,
    status_code=201
)
def create_employee(
    employee: schemas.EmployeeCreate,
    db: Session = Depends(get_db)
):

    existing_employee = (
        db.query(models.Employee)
        .filter(
            models.Employee.email == employee.email
        )
        .first()
    )

    if existing_employee:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    new_employee = models.Employee(
        name=employee.name,
        email=employee.email,
        department=employee.department,
        salary=employee.salary
    )

    db.add(new_employee)

    db.commit()

    db.refresh(new_employee)

    return new_employee
```

## The most important concept

Don't try to memorize every line. Remember the flow:

```text
POST
====

React JSON
   ↓
EmployeeCreate
   ↓
create_employee()
   ↓
Employee SQLAlchemy model
   ↓
db.add()
   ↓
db.commit()
   ↓
PostgreSQL INSERT
   ↓
db.refresh()
   ↓
EmployeeResponse
   ↓
JSON response


GET
===

React GET
   ↓
get_employees()
   ↓
db.query(Employee).all()
   ↓
PostgreSQL SELECT
   ↓
Employee objects
   ↓
EmployeeResponse
   ↓
JSON array
   ↓
React Table
```

Once you understand these two APIs, `PUT` and `DELETE` become much easier because the same concepts—**route → schema → session → model → database → response**—are reused.

Your SQL query creates a Foreign Key Constraint between two tables in your HRMS PostgreSQL database.

It establishes a relationship between the Roles table (`EO_MST_ROLES`) and the Department table (`HR_MST_DEPARTMENT`).

## 1. Your complete SQL query

```
ALTER TABLE EO_MST_ROLES
ADD CONSTRAINT FK_EO_MST_ROLES_DEPT
FOREIGN KEY (EO_MST_DEPT_ID)
REFERENCES HR_MST_DEPARTMENT (EO_DEPT_ID);
```

## 2. Line-by-line explanation

### Line 1: ALTER TABLE

```
ALTER TABLE EO_MST_ROLES
```

- `ALTER TABLE` is a PostgreSQL command used to modify an existing table.
- `EO_MST_ROLES` is the table you want to modify.
- It does not create a new table.

Meaning: Modify the existing `EO_MST_ROLES` table.

### Line 2: ADD CONSTRAINT

```
ADD CONSTRAINT FK_EO_MST_ROLES_DEPT
```

- `ADD CONSTRAINT` adds a database validation rule.
- `FK_EO_MST_ROLES_DEPT` is the name of that rule.
- `FK` is a naming convention meaning Foreign Key.

Meaning: Create a new constraint named `FK_EO_MST_ROLES_DEPT`.

### Line 3: FOREIGN KEY

```
FOREIGN KEY (EO_MST_DEPT_ID)
```

- `FOREIGN KEY` defines a relationship with another table.
- `EO_MST_DEPT_ID` is a column inside `EO_MST_ROLES`.
- It stores the department ID associated with a role.

Meaning: Use `EO_MST_DEPT_ID` as the foreign key column.

### Line 4: REFERENCES

```
REFERENCES HR_MST_DEPARTMENT (EO_DEPT_ID);
```

- `REFERENCES` identifies the parent table.
- `HR_MST_DEPARTMENT` is the parent table.
- `EO_DEPT_ID` is the referenced column.
- `EO_DEPT_ID` must be a primary key, have a unique constraint, or be covered by a suitable unique index.

Meaning: Every non-NULL department ID in `EO_MST_ROLES` must exist in `HR_MST_DEPARTMENT`.

## 3. Visual explanation of the relationship

HR_MST_DEPARTMENT

Parent table

| EO_DEPT_ID (PK) | DEPT_NAME |
| --------------- | --------- |
| 101             | IT        |
| 102             | HR        |
| 103             | Finance   |

One department can have many roles

EO_MST_ROLES

Child table

| ROLE_NAME  | EO_MST_DEPT_ID (FK) |
| ---------- | ------------------- |
| Developer  | 101                 |
| Tester     | 101                 |
| HR Manager | 102                 |

The example shows that Developer and Tester belong to the IT department, while HR Manager belongs to HR.

## 4. What happens when you insert data?

Suppose your department table contains IDs `101`, `102`, and `103`.

Valid department ID

```
INSERT INTO eo_mst_roles
    (role_name, eo_mst_dept_id)
VALUES ('Developer', 101);
```

Allowed, assuming other table requirements are satisfied, because department 101 exists.

Invalid department ID

```
INSERT INTO eo_mst_roles
    (role_name, eo_mst_dept_id)
VALUES ('Developer', 999);
```

Rejected because department 999 does not exist in the parent table.

PostgreSQL returns an error similar to:

```
ERROR: insert or update on table "eo_mst_roles"
violates foreign key constraint "fk_eo_mst_roles_dept"

SQL state: 23503
```

## 5. Important rules for this foreign key

1. Both tables must already exist.
2. `EO_MST_DEPT_ID` and `EO_DEPT_ID` must have compatible data types.
3. The referenced column must be uniquely constrained.
4. Existing non-NULL foreign key values must match parent records.
5. A NULL foreign key is allowed unless `NOT NULL` is separately specified.
6. By default, deleting a department that is still referenced by roles is restricted.

## 6. How to remove only this constraint

If you want to remove the relationship without deleting either table:

```
ALTER TABLE EO_MST_ROLES
DROP CONSTRAINT FK_EO_MST_ROLES_DEPT;
```

This removes the foreign key rule, but keeps both tables and their data.

In simple terms: Your SQL tells PostgreSQL:

> Every role that has a department ID must refer to a department that actually exists in the HRMS department master table.

This protects your HRMS database from invalid department assignments.

===================================================== Interview =============================================================================================================

# Python Interview Questions and Answers – Complete Guide (1–60)

This guide covers all 60 Python interview questions, from beginner to advanced, including OOP, coding problems, FastAPI, PostgreSQL, and backend development.

Each answer includes an explanation, Python code where useful, and expected output. The examples use modern Python 3 syntax.

# Section 1: Python Fundamentals (Questions 1–15)

## 1. What is Python? Why is it interpreted?

Answer: Python is a high-level, general-purpose, dynamically typed programming language. It supports object-oriented, procedural, and functional programming.

Python is commonly called interpreted because programs execute through a runtime environment.

In CPython, the standard implementation, source code is compiled into bytecode and then executed by the Python Virtual Machine.

Python Source Code (`.py`)

Bytecode Compilation

Python Virtual Machine

Output

Example:

```
name = "Python"print("Hello", name)
```

Output:

```
Hello Python
```

Interview point: Python is both compiled to bytecode and interpreted by a runtime in CPython.

## 2. Difference between mutable and immutable objects?

Mutable: Objects whose contents can be changed after creation.

Immutable: Objects whose contents cannot be changed after creation.

| Mutable     | Immutable                    |
| ----------- | ---------------------------- |
| `list`      | `tuple`                      |
| `dict`      | `str`                        |
| `set`       | `int`                        |
| `bytearray` | `float`, `bool`, `frozenset` |

Example:

```
# Mutablea = [10, 20, 30]a[0] = 100print(a)# Immutablename = "Python"name = name + " Developer"print(name)
```

Output:

```
[100, 20, 30]
Python Developer
```

The string operation creates a new string rather than modifying the original string.

## 3. Difference between list, tuple, set, and dict?

| Feature    | List | Tuple | Set                 | Dict            |
| ---------- | ---- | ----- | ------------------- | --------------- |
| Syntax     | `[]` | `()`  | `{}`                | `{key: value}`  |
| Mutable    | Yes  | No    | Yes                 | Yes             |
| Duplicates | Yes  | Yes   | No                  | Keys: No        |
| Ordered    | Yes  | Yes   | No guaranteed order | Insertion order |
| Indexing   | Yes  | Yes   | No                  | By key          |

Example:

```
a = [1, 2, 2, 3]b = (1, 2, 2, 3)c = {1, 2, 2, 3}d = {"name": "Rahul", "age": 25}print(a)print(b)print(sorted(c))print(d)
```

Output:

```
[1, 2, 2, 3]
(1, 2, 2, 3)
[1, 2, 3]
{'name': 'Rahul', 'age': 25}
```

## 4. Difference between `==` and `is`?

- `==` compares values for equality.
- `is` checks whether two references point to the exact same object.

```
a = [1, 2, 3]b = [1, 2, 3]c = aprint(a == b)print(a is b)print(a is c)
```

Output:

```
True
False
True
```

Interview tip: Use `is None` rather than `== None`.

## 5. What are `*args` and `**kwargs`?

They allow functions to accept variable numbers of arguments.

- `*args` collects extra positional arguments into a tuple.
- `**kwargs` collects extra keyword arguments into a dictionary.

```
def employee(*args, **kwargs):    print(args)    print(kwargs)employee(    101, "Rahul",    department="IT",    salary=50000)
```

Output:

```
(101, 'Rahul')
{'department': 'IT', 'salary': 50000}
```

## 6. What is list comprehension?

List comprehension is a concise way to create lists from iterable data.

Syntax:

```
[expression for item in iterable if condition]
```

Example:

```
numbers = [1, 2, 3, 4, 5, 6]even = [x for x in numbers if x % 2 == 0]print(even)
```

Output:

```
[2, 4, 6]
```

Equivalent using a loop:

```
even = []for x in numbers:    if x % 2 == 0:        even.append(x)
```

## 7. Difference between `append()` and `extend()`?

- `append()` adds one object as a single element.
- `extend()` adds each element from an iterable.

```
a = [1, 2]a.append([3, 4])print(a)b = [1, 2]b.extend([3, 4])print(b)
```

Output:

```
[1, 2, [3, 4]]
[1, 2, 3, 4]
```

## 8. What is slicing in Python?

Slicing extracts a portion of a sequence.

Syntax:

```
sequence[start:stop:step]
```

The `stop` index is excluded.

```
a = [10, 20, 30, 40, 50]print(a[1:4])print(a[::-1])print(a[::2])
```

Output:

```
[20, 30, 40]
[50, 40, 30, 20, 10]
[10, 30, 50]
```

## 9. Difference between shallow copy and deep copy?

A shallow copy creates a new outer object but retains references to nested objects.

A deep copy recursively copies nested objects as well.

```
import copyoriginal = [[1, 2], [3, 4]]shallow = copy.copy(original)deep = copy.deepcopy(original)original[0][0] = 100print(shallow)print(deep)
```

Output:

```
[[100, 2], [3, 4]]
[[1, 2], [3, 4]]
```

Deep copying is useful when nested mutable objects must be independent.

## 10. Difference between `None`, `False`, and `0`?

| Value   | Meaning            | Type       |
| ------- | ------------------ | ---------- |
| `None`  | Absence of a value | `NoneType` |
| `False` | Boolean false      | `bool`     |
| `0`     | Integer zero       | `int`      |

```
print(None == False)print(False == 0)print(None == 0)print(bool(None))print(bool(0))
```

Output:

```
False
True
False
False
False
```

`False == 0` is `True` because `bool` is a subclass of `int` in Python.

However, `False is 0` is false because they are not the same object.

## 11. What are local, global, and nonlocal variables?

- Local: Defined inside a function.
- Global: Defined at module level.
- Nonlocal: Refers to a variable in an enclosing function scope.

```
x = 10def outer():    y = 20    def inner():        nonlocal y        y = 30        print(x, y)    inner()    print(y)outer()
```

Output:

```
10 30
30
```

`nonlocal` allows the inner function to reassign `y` in `outer()`.

## 12. What is the LEGB scope rule?

Python resolves unqualified variable names using the LEGB rule:

L – Local

E – Enclosing

G – Global

B – Built-in

Lookup order: Local → Enclosing → Global → Built-in

```
x = "Global"def outer():    x = "Enclosing"    def inner():        x = "Local"        print(x)    inner()outer()
```

Output:

```
Local
```

Python finds the variable in the nearest applicable scope.

## 13. Difference between `break`, `continue`, and `pass`?

| Keyword    | Purpose                             |
| ---------- | ----------------------------------- |
| `break`    | Exits the nearest loop              |
| `continue` | Skips to the next iteration         |
| `pass`     | Does nothing; acts as a placeholder |

```
for i in range(5):    if i == 2:        continue    if i == 4:        break    print(i)
```

Output:

```
0
1
3
```

## 14. What are lambda functions?

A lambda is an anonymous function defined using the `lambda` keyword. Its body is a single expression.

```
square = lambda x: x * xprint(square(5))
```

Output:

```
25
```

Example with sorting:

```
employees = [    ("Rahul", 50000),    ("Amit", 30000),    ("Neha", 40000)]employees.sort(key=lambda x: x[1])print(employees)
```

Output:

```
[('Amit', 30000), ('Neha', 40000), ('Rahul', 50000)]
```

## 15. What are `map()`, `filter()`, and `reduce()`?

- `map()` transforms each element.
- `filter()` selects elements satisfying a condition.
- `reduce()` combines elements into an accumulated result.

```
from functools import reducenumbers = [1, 2, 3, 4, 5]a = list(map(lambda x: x * 2, numbers))b = list(filter(lambda x: x % 2 == 0, numbers))c = reduce(lambda x, y: x + y, numbers)print(a)print(b)print(c)
```

Output:

```
[2, 4, 6, 8, 10]
[2, 4]
15
```

# Section 2: Python OOP (Questions 16–25)

## 16. What are classes and objects?

A class is a blueprint for creating objects. An object is an instance of a class containing data and behavior.

```
class Employee:    def __init__(self, name, salary):        self.name = name        self.salary = salary    def display(self):        print(self.name, self.salary)emp1 = Employee("Rahul", 50000)emp2 = Employee("Amit", 60000)emp1.display()emp2.display()
```

Output:

```
Rahul 50000
Amit 60000
```

Here, `Employee` is the class, while `emp1` and `emp2` are objects.

## 17. What is the purpose of `self`?

`self` refers to the instance on which an instance method is called.

It is used to access instance variables and methods.

```
class Student:    def __init__(self, name):        self.name = name    def display(self):        print(self.name)student = Student("Rahul")student.display()
```

Output:

```
Rahul
```

When you call:

```
student.display()
```

It is conceptually equivalent to:

```
Student.display(student)
```

Interview point: `self` is a convention, not a reserved Python keyword.

## 18. What is `__init__()`?

`__init__()` is an initializer automatically called after a new class instance is created.

It is commonly used to initialize instance attributes.

```
class Employee:    def __init__(self, id, name):        self.id = id        self.name = nameemp = Employee(101, "Rahul")print(emp.id)print(emp.name)
```

Output:

```
101
Rahul
```

Important distinction:

- `__new__()` creates the instance.
- `__init__()` initializes the instance.
- `__init__()` must return `None`.

## 19. Difference between instance, class, and static methods?

| Method   | Decorator       | First argument     | Purpose               |
| -------- | --------------- | ------------------ | --------------------- |
| Instance | None            | `self`             | Work with object data |
| Class    | `@classmethod`  | `cls`              | Work with class data  |
| Static   | `@staticmethod` | None automatically | Utility behavior      |

```
class Employee:    company = "ABC Technologies"    def __init__(self, name):        self.name = name    def display(self):        print(self.name)    @classmethod    def company_name(cls):        print(cls.company)    @staticmethod    def add(a, b):        return a + bemp = Employee("Rahul")emp.display()Employee.company_name()print(Employee.add(10, 20))
```

Output:

```
Rahul
ABC Technologies
30
```

## 20. Explain inheritance and its types.

Inheritance allows a child class to reuse and extend behavior from a parent class.

Common inheritance patterns include:

1. Single inheritance
2. Multiple inheritance
3. Multilevel inheritance
4. Hierarchical inheritance
5. Hybrid inheritance

Example:

```
class Person:    def display(self):        print("Person class")class Employee(Person):    def work(self):        print("Employee working")emp = Employee()emp.display()emp.work()
```

Output:

```
Person class
Employee working
```

The `Employee` class inherits `display()` from `Person`.

## 21. What is polymorphism in Python?

Polymorphism means the same operation or method interface can behave differently depending on the object.

```
class Dog:    def sound(self):        return "Bark"class Cat:    def sound(self):        return "Meow"def animal_sound(animal):    print(animal.sound())animal_sound(Dog())animal_sound(Cat())
```

Output:

```
Bark
Meow
```

This demonstrates duck typing: Python focuses on whether an object supports the required operation.

## 22. Explain encapsulation and abstraction.

Encapsulation groups data and related behavior within a class and controls how data is accessed.

Abstraction exposes essential operations while hiding implementation details.

Encapsulation example:

```
class BankAccount:    def __init__(self):        self.__balance = 1000    def deposit(self, amount):        if amount > 0:            self.__balance += amount    def get_balance(self):        return self.__balanceaccount = BankAccount()account.deposit(500)print(account.get_balance())
```

Output:

```
1500
```

`__balance` uses name mangling to discourage direct access. It is not strictly private.

Abstraction example:

```
from abc import ABC, abstractmethodclass Payment(ABC):    @abstractmethod    def pay(self, amount):        passclass CardPayment(Payment):    def pay(self, amount):        print(f"Paid {amount} using card")payment = CardPayment()payment.pay(500)
```

Output:

```
Paid 500 using card
```

## 23. What is method overriding?

Method overriding occurs when a subclass provides its own implementation of a method inherited from a parent class.

```
class Parent:    def show(self):        print("Parent method")class Child(Parent):    def show(self):        print("Child method")obj = Child()obj.show()
```

Output:

```
Child method
```

You can use `super()` to call the inherited implementation.

## 24. What is Method Resolution Order (MRO)?

MRO defines the order in which Python searches classes for attributes and methods, especially in multiple inheritance.

```
class A:    def show(self):        print("Class A")class B(A):    passclass C(A):    def show(self):        print("Class C")class D(B, C):    passobj = D()obj.show()print([cls.__name__ for cls in D.__mro__])
```

Output:

```
Class C
['D', 'B', 'C', 'A', 'object']
```

Python uses C3 linearization to determine a consistent MRO.

## 25. Difference between `__str__()` and `__repr__()`?

- `__str__()` provides a human-readable string representation.
- `__repr__()` provides a developer-oriented representation, ideally unambiguous.

```
class Employee:    def __init__(self, name):        self.name = name    def __str__(self):        return f"Employee: {self.name}"    def __repr__(self):        return f"Employee(name={self.name!r})"emp = Employee("Rahul")print(str(emp))print(repr(emp))
```

Output:

```
Employee: Rahul
Employee(name='Rahul')
```

# Section 3: Advanced Python (Questions 26–40)

## 26. What are decorators?

A decorator wraps a function or class to extend its behavior without directly modifying its original definition.

```
from functools import wrapsdef log_execution(func):    @wraps(func)    def wrapper(*args, **kwargs):        print("Before execution")        result = func(*args, **kwargs)        print("After execution")        return result    return wrapper@log_executiondef greet():    print("Hello Python")greet()
```

Output:

```
Before execution
Hello Python
After execution
```

Common uses include logging, authentication, caching, and timing.

## 27. Difference between iterator and generator?

An iterator is an object implementing `__iter__()` and `__next__()`.

A generator is a convenient way to create an iterator, commonly using `yield`.

```
numbers = iter([10, 20, 30])print(next(numbers))print(next(numbers))def generate():    yield 100    yield 200gen = generate()print(next(gen))print(next(gen))
```

Output:

```
10
20
100
200
```

Generators are useful for processing large data streams without storing all results in memory.

## 28. What is the `yield` keyword?

`yield` produces a value and suspends generator execution, preserving its state until execution resumes.

```
def numbers():    yield 1    yield 2    yield 3for number in numbers():    print(number)
```

Output:

```
1
2
3
```

Unlike a normal `return`, `yield` allows execution to continue from the suspended point.

## 29. What is the Global Interpreter Lock (GIL)?

The GIL is a synchronization mechanism used by traditional GIL-enabled CPython builds.

It generally allows only one thread at a time to execute Python bytecode within an interpreter.

Key points:

- Threads are useful for I/O-bound work.
- CPU-bound Python code may not gain parallel speedup from threads in a GIL-enabled build.
- Multiprocessing can provide parallel CPU execution.
- Modern CPython also supports optional free-threaded builds, so GIL behavior depends on the interpreter configuration.

## 30. Difference between multithreading and multiprocessing?

| Multithreading                                    | Multiprocessing                 |
| ------------------------------------------------- | ------------------------------- |
| Multiple threads                                  | Multiple processes              |
| Threads share process memory                      | Processes have separate memory  |
| Lower creation overhead                           | Higher creation overhead        |
| Often useful for I/O-bound work                   | Often useful for CPU-bound work |
| Subject to GIL limitations in traditional CPython | Can execute across CPU cores    |

Threading example:

```
import threadingdef task():    print("Task running")thread = threading.Thread(target=task)thread.start()thread.join()
```

Output:

```
Task running
```

## 31. What is asynchronous programming?

Asynchronous programming allows a program to handle other work while waiting for operations such as network requests or database calls.

```
import asyncioasync def task():    print("Start")    await asyncio.sleep(1)    print("End")asyncio.run(task())
```

Output:

```
Start
End
```

The `await` expression suspends the coroutine while the asynchronous operation completes.

## 32. Difference between `async` and `await`?

- `async def` defines a coroutine function.
- `await` waits for an awaitable within an asynchronous function while allowing the event loop to run other tasks.

```
import asyncioasync def get_data():    await asyncio.sleep(1)    return "Data loaded"async def main():    result = await get_data()    print(result)asyncio.run(main())
```

Output:

```
Data loaded
```

In FastAPI, asynchronous route handlers are declared using `async def`.

## 33. What are context managers and the `with` statement?

A context manager manages setup and cleanup of resources.

```
with open("demo.txt", "w") as file:    file.write("Hello Python")with open("demo.txt", "r") as file:    print(file.read())
```

Output:

```
Hello Python
```

The file is automatically closed when the `with` block exits, including when an exception occurs.

Custom context managers can implement `__enter__()` and `__exit__()`.

## 34. What is garbage collection in Python?

Garbage collection automatically reclaims memory occupied by objects that are no longer needed.

In CPython, memory management primarily uses reference counting, supplemented by a cyclic garbage collector.

```
import gcprint(gc.isenabled())
```

Typical output:

```
True
```

The `gc` module allows developers to inspect and control cyclic garbage collection.

## 35. What are Python metaclasses?

A metaclass controls how classes themselves are created.

By default, Python classes are instances of the metaclass `type`.

```
class Employee:    passprint(type(Employee))print(type(Employee()))
```

Output:

```
<class 'type'>
<class '__main__.Employee'>
```

Custom metaclasses can validate class definitions, register classes, or modify class creation behavior.

They are advanced features and are rarely necessary for ordinary application development.

## 36. What are descriptors?

A descriptor is an object that customizes attribute access through methods such as:

- `__get__()`
- `__set__()`
- `__delete__()`

Example:

```
class PositiveNumber:    def __set_name__(self, owner, name):        self.name = name    def __get__(self, obj, owner):        if obj is None:            return self        return obj.__dict__[self.name]    def __set__(self, obj, value):        if value <= 0:            raise ValueError("Must be positive")        obj.__dict__[self.name] = valueclass Product:    price = PositiveNumber()product = Product()product.price = 100print(product.price)
```

Output:

```
100
```

Descriptors are used internally by features such as properties and methods.

## 37. How does exception handling work?

Python uses `try`, `except`, `else`, and `finally` for exception handling.

```
try:    result = 10 / 0except ZeroDivisionError:    print("Cannot divide by zero")else:    print("Calculation successful")finally:    print("Execution completed")
```

Output:

```
Cannot divide by zero
Execution completed
```

The `else` block executes when no exception occurs in `try`.

The `finally` block normally executes whether an exception occurs or not.

## 38. What are type hints?

Type hints document expected parameter and return types and support static analysis.

```
def add(a: int, b: int) -> int:    return a + bprint(add(10, 20))
```

Output:

```
30
```

Python does not automatically enforce these annotations at runtime.

Tools such as mypy and Pyright can check type consistency.

## 39. What are dataclasses?

Dataclasses automatically generate common methods such as `__init__()` and `__repr__()` based on declared fields.

```
from dataclasses import dataclass@dataclassclass Employee:    id: int    name: str    salary: floatemp = Employee(101, "Rahul", 50000)print(emp)
```

Output:

```
Employee(id=101, name='Rahul', salary=50000)
```

Dataclasses are useful for simple data-holding classes.

## 40. What are Python virtual environments?

A virtual environment isolates project-specific Python packages from other projects.

Create a virtual environment:

```
python -m venv venv
```

Activate on Windows PowerShell:

```
.\venv\Scripts\Activate.ps1
```

Activate on Linux/macOS:

```
source venv/bin/activate
```

Install packages:

```
python -m pip install fastapi uvicorn
```

Save dependencies:

```
python -m pip freeze > requirements.txt
```

Interview point: Virtual environments help avoid dependency conflicts between projects.

# Section 4: Python Coding Interview Questions (41–50)

These are practical programming problems frequently used in coding rounds. Each solution includes its time and space complexity.

## 41. Reverse a string without using `[::-1]`

```
def reverse_string(text):    result = ""    for char in text:        result = char + result    return resultprint(reverse_string("Python"))
```

Output:

```
nohtyP
```

Time complexity: O(n²) for this implementation because repeated string concatenation copies characters.

Space complexity: O(n).

For a more efficient solution, append characters to a list and use `"".join()`.

## 42. Check whether a string is a palindrome

A palindrome reads the same forward and backward.

```
def is_palindrome(text):    return text == text[::-1]print(is_palindrome("madam"))print(is_palindrome("python"))
```

Output:

```
True
False
```

Time complexity: O(n).

Space complexity: O(n) for the reversed string.

## 43. Find the second-largest number in a list

This solution finds the second-largest distinct value.

```
def second_largest(numbers):    first = None    second = None    for num in numbers:        if first is None or num > first:            second = first            first = num        elif num != first and (            second is None or num > second        ):            second = num    return secondprint(second_largest([10, 30, 20, 50, 40]))
```

Output:

```
40
```

Time complexity: O(n).

Space complexity: O(1).

Returns `None` if fewer than two distinct numbers exist.

## 44. Remove duplicates from a list

Preserve the original order:

```
def remove_duplicates(numbers):    seen = set()    result = []    for num in numbers:        if num not in seen:            seen.add(num)            result.append(num)    return resultprint(remove_duplicates([1, 2, 2, 3, 1, 4]))
```

Output:

```
[1, 2, 3, 4]
```

Time complexity: O(n) on average for hashable elements.

Space complexity: O(n).

## 45. Count character frequency in a string

```
def frequency(text):    result = {}    for char in text:        result[char] = result.get(char, 0) + 1    return resultprint(frequency("banana"))
```

Output:

```
{'b': 1, 'a': 3, 'n': 2}
```

Time complexity: O(n) on average.

Space complexity: O(k), where k is the number of distinct characters.

Alternative:

```
from collections import Counterprint(Counter("banana"))
```

## 46. Find the first non-repeating character

```
from collections import Counterdef first_unique(text):    counts = Counter(text)    for char in text:        if counts[char] == 1:            return char    return Noneprint(first_unique("swiss"))
```

Output:

```
w
```

Time complexity: O(n).

Space complexity: O(k), where k is the number of distinct characters.

## 47. Check whether two strings are anagrams

Anagrams contain the same characters with the same frequencies, regardless of order.

```
from collections import Counterdef is_anagram(a, b):    return Counter(a) == Counter(b)print(is_anagram("listen", "silent"))print(is_anagram("hello", "world"))
```

Output:

```
True
False
```

Time complexity: O(n + m).

Space complexity: O(k), where k is the number of distinct characters.

## 48. Find two numbers whose sum equals a target

This is the classic Two Sum problem.

```
def two_sum(nums, target):
seen = {}
for i, num in enumerate(nums):
complement = target - num
if complement in seen:
return [seen[complement], i]
seen[num] = i
return []
print(two_sum([2, 7, 11, 15], 9))
```

Output:

```
[0, 1]
```

Explanation: `2 + 7 = 9`, and their indices are `0` and `1`.

Time complexity: O(n) on average.

Space complexity: O(n).

## 49. Find the missing number in an array

Assume the list contains unique numbers from `1` to `n`, with exactly one number missing.

```
def missing_number(nums, n):    expected = n * (n + 1) // 2    actual = sum(nums)    return expected - actualprint(missing_number([1, 2, 4, 5], 5))
```

Output:

```
3
```

Time complexity: O(n).

Space complexity: O(1).

## 50. Find the longest substring without repeating characters

Use the sliding-window technique.

```
def longest_substring(text):    seen = {}    left = 0    max_length = 0    best_start = 0    for right, char in enumerate(text):        if char in seen and seen[char] >= left:            left = seen[char] + 1        seen[char] = right        length = right - left + 1        if length > max_length:            max_length = length            best_start = left    return text[best_start:best_start + max_length]print(longest_substring("abcabcbb"))
```

Output:

```
abc
```

Time complexity: O(n) on average.

Space complexity: O(k), where k is the number of distinct characters.

# Section 5: FastAPI, PostgreSQL and Backend (51–60)

## 51. What is FastAPI and how is it different from Django?

FastAPI is a modern Python web framework for building APIs using Python type hints.

Django is a full-featured web framework that includes many built-in components for web application development.

| Feature           | FastAPI                | Django                          |
| ----------------- | ---------------------- | ------------------------------- |
| Primary focus     | API development        | Full web applications           |
| Async support     | Native                 | Supported                       |
| Data validation   | Pydantic               | Forms, serializers via packages |
| Built-in ORM      | No                     | Yes                             |
| Admin interface   | No built-in admin      | Built-in admin                  |
| API documentation | Automatic OpenAPI      | Usually additional packages     |
| Best use case     | APIs and microservices | Full-stack web systems          |

FastAPI example:

```
from fastapi import FastAPIapp = FastAPI()@app.get("/")def home():    return {"message": "Hello FastAPI"}
```

Response:

```
{
  "message": "Hello FastAPI"
}
```

Run using:

```
uvicorn main:app --reload
```

Swagger UI is available at:

```
http://127.0.0.1:8000/docs
```

## 52. What is Pydantic and why is it used?

Pydantic is a Python library for data validation, parsing, and serialization using type annotations.

FastAPI uses Pydantic models to validate API request and response data.

```
from pydantic import BaseModel, Fieldclass Employee(BaseModel):    name: str    age: int = Field(gt=18)    salary: float = Field(gt=0)emp = Employee(    name="Rahul",    age=25,    salary=50000)print(emp.model_dump())
```

Output:

```
{'name': 'Rahul', 'age': 25, 'salary': 50000.0}
```

If `age` is 15, Pydantic raises a validation error because the age must be greater than 18.

## 53. What is dependency injection in FastAPI?

Dependency injection allows FastAPI to provide required resources or values to endpoint functions.

It is commonly used for database sessions, authentication, and shared services.

```
from fastapi import FastAPI, Dependsapp = FastAPI()def get_message():    return "Hello from dependency"@app.get("/message")def message(msg: str = Depends(get_message)):    return {"message": msg}
```

Response:

```
{
  "message": "Hello from dependency"
}
```

Interview point: Dependency injection improves reusability, testability, and separation of concerns.

## 54. How do you connect FastAPI with PostgreSQL?

A common approach is to use SQLAlchemy with a PostgreSQL driver such as psycopg.

Install dependencies:

```
pip install fastapi uvicorn sqlalchemy "psycopg[binary]"
```

Database configuration:

```
from sqlalchemy import create_enginefrom sqlalchemy.orm import sessionmakerDATABASE_URL = (    "postgresql+psycopg://"    "postgres:password@localhost:5432/employee_db")engine = create_engine(    DATABASE_URL,    pool_pre_ping=True)SessionLocal = sessionmaker(    bind=engine,    autoflush=False)
```

Database dependency:

```
def get_db():    with SessionLocal() as db:        yield db
```

Using it in FastAPI:

```
from fastapi import Dependsfrom sqlalchemy.orm import Sessionfrom sqlalchemy import text@app.get("/db-health")def db_health(db: Session = Depends(get_db)):    result = db.execute(text("SELECT 1")).scalar()    return {"database": result}
```

Response:

```
{
  "database": 1
}
```

In production, store database credentials in environment variables or a secret manager, not directly in source code.

## 55. Difference between SQLAlchemy ORM and raw SQL?

| SQLAlchemy ORM                          | Raw SQL                        |
| --------------------------------------- | ------------------------------ |
| Works with mapped Python classes        | Works with SQL statements      |
| Supports relationships and unit of work | Provides direct SQL control    |
| Reduces repetitive mapping code         | Useful for specialized queries |
| Database abstraction                    | Often database-specific        |
| Can generate SQL automatically          | SQL is written manually        |

ORM example:

```
employees = (    db.query(Employee)    .filter(Employee.salary > 30000)    .all())
```

Raw SQL example:

```
from sqlalchemy import textresult = db.execute(    text("SELECT * FROM employees WHERE salary > :salary"),    {"salary": 30000})employees = result.fetchall()
```

Use parameterized queries to prevent SQL injection.

## 56. How do you implement JWT authentication in FastAPI?

JWT stands for JSON Web Token.

It is commonly used for stateless API authentication.

A typical authentication flow is:

1\. User Login

Username + Password

2\. Validate Credentials

Check stored password hash

3\. Issue Signed JWT

Include subject and expiration

4\. Access Protected API

Authorization: Bearer token

5\. Verify Token and Permissions

JWT generation example using PyJWT:

```
import jwtfrom datetime import datetime, timedelta, timezoneSECRET_KEY = "replace-with-secure-secret"payload = {    "sub": "employee101",    "exp": datetime.now(timezone.utc)           + timedelta(minutes=30)}token = jwt.encode(    payload,    SECRET_KEY,    algorithm="HS256")print(isinstance(token, str))
```

Output:

```
True
```

This example demonstrates token creation only, not a complete authentication system.

A production implementation must securely store the signing key, verify token signature, issuer, audience, and expiration, validate user permissions, and use HTTPS.

## 57. What is middleware in FastAPI?

Middleware is code that executes around HTTP request processing.

Common uses include logging, CORS, authentication-related processing, and request timing.

```
from fastapi import FastAPI, Requestimport timeapp = FastAPI()@app.middleware("http")async def log_request(request: Request, call_next):    start = time.perf_counter()    response = await call_next(request)    duration = time.perf_counter() - start    print(f"Request took {duration:.4f} seconds")    return response@app.get("/")def home():    return {"message": "Hello"}
```

Every request passes through the middleware before reaching the route handler, and the middleware can process the response afterward.

## 58. How do you implement pagination in FastAPI?

Pagination divides large datasets into smaller pages.

Example using SQLAlchemy:

```
from fastapi import FastAPI, Depends, Queryfrom sqlalchemy.orm import Sessionapp = FastAPI()@app.get("/employees")def get_employees(    page: int = Query(1, ge=1),    size: int = Query(10, ge=1, le=100),    db: Session = Depends(get_db)):    offset = (page - 1) * size    total = db.query(Employee).count()    employees = (        db.query(Employee)        .order_by(Employee.id)        .offset(offset)        .limit(size)        .all()    )    return {        "page": page,        "size": size,        "total": total,        "data": employees    }
```

Example request:

```
GET /employees?page=2&size=10
```

Calculation:

```
offset = (2 - 1) * 10
offset = 10
```

This skips the first 10 records and retrieves the next 10.

For very large datasets, cursor-based pagination can be more efficient than large offsets.

## 59. How do you handle database transactions?

A transaction groups database operations into a logical unit of work.

Transactions follow ACID principles:

| Property    | Meaning                                 |
| ----------- | --------------------------------------- |
| Atomicity   | All operations succeed or fail together |
| Consistency | Database constraints remain valid       |
| Isolation   | Concurrent transactions are controlled  |
| Durability  | Committed changes persist               |

SQLAlchemy example:

```
from sqlalchemy.orm import Sessiondef transfer_money(    db: Session,    sender,    receiver,    amount):    if amount <= 0:        raise ValueError("Invalid amount")    try:        if sender.balance < amount:            raise ValueError("Insufficient balance")        sender.balance -= amount        receiver.balance += amount        db.commit()    except Exception:        db.rollback()        raise
```

If an operation fails before commit, the transaction is rolled back.

In production, concurrent balance updates also require appropriate locking or concurrency controls to prevent lost updates.

## 60. How do you write unit and integration tests using pytest?

`pytest` is a Python testing framework that supports test discovery, fixtures, assertions, and parameterized tests.

Install:

```
pip install pytest httpx
```

### Unit testing

Application code:

```
# calculator.pydef add(a, b):    return a + b
```

Test code:

```
# test_calculator.pyfrom calculator import adddef test_add():    assert add(10, 20) == 30
```

Run:

```
pytest -v
```

Expected result:

```
test_calculator.py::test_add PASSED
```

### FastAPI integration testing

Application:

```
# main.pyfrom fastapi import FastAPIapp = FastAPI()@app.get("/health")def health():    return {"status": "UP"}
```

Test:

```
# test_main.pyfrom fastapi.testclient import TestClientfrom main import appclient = TestClient(app)def test_health():    response = client.get("/health")    assert response.status_code == 200    assert response.json() == {"status": "UP"}
```

Run:

```
pytest test_main.py -v
```

Expected result:

```
test_main.py::test_health PASSED
```

For database integration tests, use an isolated test database and reset test data between cases.

# Python Interview Preparation – Practice Assessment

You now have answers to all 60 questions. Test your understanding with five questions covering Python fundamentals, OOP, and backend development.

Python interview quiz

0 of 5 answered

1\. What is the output?

a = [1, 2]\
b = a\
b.append(3)\
print(a)

[1, 2]

[1, 2, 3]

[3]

Error

Submit answers

2\. Which keyword allows an inner function to reassign a variable in an enclosing function?

global

static

nonlocal

self

Submit answers

3\. Which method controls instance initialization?

\_\_str\_\_

\_\_init\_\_

\_\_repr\_\_

\_\_iter\_\_

Submit answers

4\. What does a generator function commonly use to produce values?

return only

yield

pass

break

Submit answers

5\. Which HTTP status code does FastAPI typically return for request validation errors?

200

401

422

500

Submit answers

## Recommended next step

For Python backend developer interviews, the highest-value next step is practicing coding questions 41–50 without looking at the solutions, then implementing a small FastAPI CRUD project with PostgreSQL, JWT authentication, pagination, and pytest tests.

That combination prepares you for both theoretical interviews and practical coding rounds.

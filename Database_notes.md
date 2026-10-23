
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
fetch("http://127.0.0.1:8000/employees")
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
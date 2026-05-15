# Django Project – Makefile Commands

This project includes a `Makefile` to simplify common development tasks.
Instead of typing long Django or tooling commands, you can use `make <command>`.

---

## 🚀 Getting Started

Make sure you have the following installed:

* Python 3.x
* `pip`
* Virtual environment (recommended)
* Project dependencies installed

```bash
pip install -r requirements.txt
```

---

## 🛠 Available Commands

### Run Development Server

```bash
make run
```

Starts the Django development server on:

```
http://0.0.0.0:8002
```

---

### Database Migrations

#### Create & Apply Migrations

```bash
make migrate
```

#### Create Migrations Only

```bash
make makemigrations
```

---

### Django Shell

```bash
make shell
```

Opens Django interactive shell.

---

### Create Superuser

```bash
make superuser
```

Creates an admin user.

---

### Collect Static Files

```bash
make collectstatic
```

Collects static files for production.

---

### Run Tests

```bash
make test
```

Runs Django test suite.

---

### Flush Database

```bash
make flush
```

⚠️ This will delete all data from the database.

---

### Clean Project

```bash
make clean
```

Removes:

* `.pyc` files
* `__pycache__` directories

---

### Code Linting (Ruff)

#### Check Code

```bash
make check
```

#### Auto-fix & Format Code

```bash
make fix
```

---

## 💡 Notes

* Use a virtual environment to avoid dependency conflicts.
* Be careful with `make flush` — it removes all database data.
* `make fix` will modify your code automatically using Ruff.

---

## 👤 User Management API (v1)

Base path: `/api/v1/users/`

### Admin invite user

`POST /api/v1/users/invite/`

Request:

```json
{
  "email": "new.user@example.com",
  "name": "New User",
  "role": "user"
}
```

Response: `201 Created` (empty body). If duplicate email, returns:

```json
{ "detail": "A user with this email already exists.", "code": "validation_error" }
```

### Resend invite link (admin)

If an invite link expires, admins can send a fresh one (new token).

`POST /api/v1/users/invite/resend/`

Request:

```json
{ "email": "new.user@example.com" }
```

Response:

```json
{ "detail": "Invite link sent." }
```

### Set password (first-time activation)

`POST /api/v1/users/set-password/`

Request:

```json
{
  "uid": "<uid-from-email-link>",
  "token": "<token-from-email-link>",
  "name": "Updated Name",
  "password": "A-strong-password-123!"
}
```

Response:

```json
{ "detail": "Password set successfully." }
```

### Login (JWT)

`POST /api/v1/users/login/`

Request:

```json
{ "email": "new.user@example.com", "password": "A-strong-password-123!" }
```

Response:

```json
{ "access": "<jwt-access>", "refresh": "<jwt-refresh>" }
```

### Forgot password (non-enumerating)

`POST /api/v1/users/forgot-password/`

Request:

```json
{ "email": "new.user@example.com" }
```

Response (always `200 OK`):

```json
{ "detail": "If that email exists, a reset link has been sent." }
```

### Reset password

`POST /api/v1/users/reset-password/`

Request:

```json
{
  "uid": "<uid-from-email-link>",
  "token": "<token-from-email-link>",
  "new_password": "Even-stronger-456!"
}
```

Response:

```json
{ "detail": "Password reset successfully." }
```

---

## 📌 Example Workflow

```bash
make makemigrations
make migrate
make run
```

---

## 📄 License

Add your license information here.

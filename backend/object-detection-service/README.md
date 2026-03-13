# Project Setup

This project requires **Python 3.10**. Follow the steps below to set up the development environment.

---

# 1. Install Python 3.10

## Linux (Manjaro / Arch)

Install Python 3.10:

```bash
sudo pacman -S python310
```

Verify installation:

```bash
python3.10 --version
```

---

## Windows

1. Download Python 3.10 from the official Python website.
2. Run the installer.
3. Make sure to enable:

```
Add Python to PATH
```

Verify installation:

```bash
python --version
```

or

```bash
py -3.10 --version
```

---

# 2. Create Virtual Environment

## Linux

```bash
python3.10 -m venv venv
```

## Windows

```bash
py -3.10 -m venv venv
```

---

# 3. Activate Virtual Environment

## Linux / macOS

```bash
source venv/bin/activate
```

## Windows (Command Prompt)

```bash
venv\Scripts\activate
```

## Windows (PowerShell)

```powershell
venv\Scripts\Activate.ps1
```

---

# 4. Upgrade pip

```bash
pip install --upgrade pip
```

---

# 5. Install Dependencies

If using a requirements file:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

# 6. Deactivate Virtual Environment

```bash
deactivate
```

---

# 7. Run the Application

Example for running a FastAPI server:

```bash
.\doit.sh run
```

Server will run at:

```
http://127.0.0.1:8000
```

# Virtual Environment Setup Guide

This guide will help you set up a Python virtual environment for the backend project.

## Why Use a Virtual Environment?

Virtual environments isolate your project dependencies, preventing conflicts with other Python projects and system packages.

## Quick Setup (Windows PowerShell)

1. **Navigate to backend directory:**
   ```powershell
   cd backend
   ```

2. **Run the setup script:**
   ```powershell
   .\setup_venv.ps1
   ```

   If you get an execution policy error, run this first:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. **Activate the virtual environment:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

4. **Run the application:**
   ```powershell
   python run.py
   ```

## Manual Setup (Windows)

1. **Create virtual environment:**
   ```powershell
   python -m venv venv
   ```

2. **Activate virtual environment:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

3. **Upgrade pip:**
   ```powershell
   python -m pip install --upgrade pip
   ```

4. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

## Quick Setup (Linux/Mac)

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Make script executable and run:**
   ```bash
   chmod +x setup_venv.sh
   ./setup_venv.sh
   ```

3. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```

4. **Run the application:**
   ```bash
   python run.py
   ```

## Manual Setup (Linux/Mac)

1. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   ```

2. **Activate virtual environment:**
   ```bash
   source venv/bin/activate
   ```

3. **Upgrade pip:**
   ```bash
   python -m pip install --upgrade pip
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Using the Virtual Environment

### Activate (Windows PowerShell)
```powershell
.\venv\Scripts\Activate.ps1
```

### Activate (Windows CMD)
```cmd
venv\Scripts\activate.bat
```

### Activate (Linux/Mac)
```bash
source venv/bin/activate
```

### Deactivate
```bash
deactivate
```

## Verify Installation

After activating the virtual environment, verify packages are installed:

```bash
pip list
```

You should see:
- fastapi
- uvicorn
- httpx
- pydantic
- sqlalchemy
- python-dotenv

## Troubleshooting

### PowerShell Execution Policy Error

If you see: "cannot be loaded because running scripts is disabled on this system"

Run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Module Not Found After Activation

Make sure you:
1. Activated the virtual environment (you should see `(venv)` in your prompt)
2. Installed requirements: `pip install -r requirements.txt`

### Port Already in Use

If port 8000 is already in use:
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

Or change the port in `run.py`:
```python
uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)
```

## Notes

- The `venv` folder is in `.gitignore` - don't commit it
- Always activate the virtual environment before running the app
- If you add new packages, update `requirements.txt`:
  ```bash
  pip freeze > requirements.txt
  ```


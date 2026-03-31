# Setup Guide

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Prutha0105/Streamlit-Dashboard.git
cd Streamlit-Dashboard
```

### 2. (Optional) Create a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the dashboard

```bash
streamlit run promoter_dashboard.py
```

The app will open automatically in your browser at `http://localhost:8501`.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `streamlit: command not found` | Run `pip install streamlit` |
| Port 8501 already in use | Run `streamlit run promoter_dashboard.py --server.port 8502` |
| Module not found error | Make sure you activated your virtual environment and ran `pip install -r requirements.txt` |

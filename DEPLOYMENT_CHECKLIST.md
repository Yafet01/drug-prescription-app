# Deployment Checklist - Drug Prescription App

## Issues Found & To Fix

### 1. **CRITICAL: Hardcoded Windows Path** ⚠️
**File:** `app.py` line 19
```python
IMAGE_PATH = r"C:\Users\tedya\OneDrive\Pictures\Cyberpunk 2077\photomode_28092023_224143.png"
```
**Issue:** This is a Windows-specific absolute path that won't work on:
- Web servers (Linux/Mac)
- GitHub
- Streamlit Cloud
- Other machines

**Fix:** Use relative path or placeholder
```python
IMAGE_PATH = "assets/login_image.png"  # Or leave empty for web
```

### 2. **Database Paths** 
**Files:** `app.py` lines 17-18
```python
DB_PATH_USERS = "users.db"
DB_PATH_MEDICINE = "Historical_Data_Medicine.db"
```
**Status:** ✅ OK - These are relative paths (will work on web)

### 3. **Model & Data Paths** 
**Files:** `predict_page.py`, `explore_page.py`
- `Model/best_rf_model.pkl`
- `Model/feature_columns.pkl`
- `Model/Historical_Data_2021_Jan_2024.csv`

**Status:** ✅ OK - Relative paths work on web

### 4. **CSS File**
**File:** `app.py` line 20
```python
STYLES_PATH = "styles.css"
```
**Status:** ✅ OK - Relative path

### 5. **Sensitive Data** 
**Files:**
- `users.db` - ✅ In .gitignore (good!)
- `hashed_pw.plk` - Check if this should be ignored
- Database files - ✅ Properly ignored

**Status:** ✅ OK - Database files won't be uploaded

### 6. **Requirements.txt**
**Status:** ✅ Complete with all dependencies

### 7. **Model Files in .gitignore**
**Status:** ⚠️ ISSUE - Model files excluded from git
```
Model/
*.pkl
```
**Fix:** If models are <100MB, remove from .gitignore or use Git LFS

### 8. **Missing for Web Hosting**
- ❌ No `.streamlit/config.toml` for production
- ❌ No deployment guide
- ❌ No environment variables setup
- ❌ No README.md

## Summary of Changes Needed

| Priority | Item | Status |
|----------|------|--------|
| 🔴 HIGH | Fix hardcoded image path | ❌ TODO |
| 🟠 MEDIUM | Update .gitignore for models | ❌ TODO |
| 🟠 MEDIUM | Create .streamlit/config.toml | ❌ TODO |
| 🟡 LOW | Add README.md | ❌ TODO |
| 🟡 LOW | Add deployment guide | ❌ TODO |

## Next Steps
1. Fix IMAGE_PATH in app.py
2. Create assets folder with login image (or use placeholder)
3. Configure Streamlit for production
4. Create README and deployment docs
5. Initialize git and push to GitHub
6. Set up Streamlit Cloud deployment

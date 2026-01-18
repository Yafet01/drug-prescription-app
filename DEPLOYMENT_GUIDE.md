# Deployment Guide

## 1. Prepare for GitHub
- Ensure `.gitignore` allows `Model/` and `assets/`
- Add a login image to `assets/login_image.png` (or update/remove in app.py)
- Check all model files are present in `Model/`

## 2. Push to GitHub
```bash
git init
git remote add origin https://github.com/Yafet01/drug-prescription-app.git
git add .
git commit -m "Initial commit for deployment"
git push -u origin master
```

## 3. Deploy to Streamlit Cloud
- Go to [Streamlit Cloud](https://streamlit.io/cloud)
- Connect your GitHub repo
- Set main file to `app.py`
- Set Python version and requirements.txt
- Add any secrets/environment variables if needed

## 4. Production Config
- `.streamlit/config.toml` is set for headless server
- You can customize theme and port

## 5. Database
- SQLite databases are created automatically
- For production, consider using a cloud database

## 6. Troubleshooting
- If you see missing model/data errors, upload files to `Model/`
- If login image missing, update/remove `IMAGE_PATH` in `app.py`

# Hosting Guide for Drug Prescription Analysis App

## Deployment Options

### Option 1: Streamlit Cloud (Recommended)

**Prerequisites:**
- GitHub account
- Code pushed to GitHub repository

**Steps:**
1. Go to https://streamlit.io/cloud
2. Click "New app"
3. Select your repository: `Yafet01/drug-prescription-app`
4. Branch: `main`
5. Main file path: `app.py`
6. Click "Deploy"

Your app will be live at: `https://<your-username>-drug-prescription-app-<random>.streamlit.app`

### Option 2: Railway

1. Go to https://railway.app
2. Create a new project
3. Connect your GitHub repository
4. Add environment variables if needed
5. Deploy

### Option 3: Heroku

1. Install Heroku CLI
2. Create `Procfile` with: `web: streamlit run app.py`
3. Create `setup.sh` with Streamlit configuration
4. Deploy: `heroku create && git push heroku main`

## Important Notes

- ✅ `.gitignore` excludes `users.db` - new database created on first run
- ✅ `requirements.txt` includes all dependencies
- ✅ Model file (`model_saved`) is included
- ✅ CSV data files are included
- ✅ App is stateless and cloud-ready

## Troubleshooting

**Issue: Module import errors**
- Verify `requirements.txt` has all dependencies
- Check `config.py` paths are correct

**Issue: Model file not found**
- Ensure `model_saved` file is in repository root
- Check file is not in `.gitignore`

**Issue: Database errors**
- First user creation initializes database
- Subsequent runs use existing database

## Security

- Passwords are bcrypted (never stored in plain text)
- Use strong passwords for production
- Consider adding more users via CLI

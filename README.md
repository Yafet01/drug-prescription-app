# Drug Prescription App

A Streamlit web app for managing and analyzing drug prescriptions and disease datasets.

## Features
- User authentication
- Add/view medicines
- Explore historical data
- Predict outcomes using ML models

## Setup
1. Clone the repo:
   ```bash
   git clone https://github.com/Yafet01/drug-prescription-app.git
   cd drug-prescription-app
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run locally:
   ```bash
   streamlit run app.py
   ```

## Deployment
- Ready for Streamlit Cloud or other web hosting
- See `.streamlit/config.toml` for production config

## Notes
- Place a login image in `assets/login_image.png` (or update/remove in app.py)
- Model files must be present in `Model/`
- Database files are created automatically

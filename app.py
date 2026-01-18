import streamlit as st
import sqlite3
import bcrypt
from pathlib import Path

# Import custom modules
from config import PROJECT_DIR, MODEL_PATH
from predict_page import predict_page
from explore_page import explore_page
from about_page import about_page

# Page config
st.set_page_config(
    page_title="Drug Prescription to Disease Analysis",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

def create_connection():
    """Create a database connection with proper timeout and WAL mode."""
    try:
        db_path = PROJECT_DIR / "users.db"
        conn = sqlite3.connect(str(db_path), timeout=10.0)
        conn.execute("PRAGMA journal_mode=WAL")
        return conn
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
        return None

def authenticate_user(username, password):
    """Authenticate user with bcrypt."""
    try:
        conn = create_connection()
        if not conn:
            return False
        
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            stored_hash = result[0]
            # Handle both bytes and string representations
            if isinstance(stored_hash, str):
                stored_hash = stored_hash.encode()
            password_bytes = password.encode() if isinstance(password, str) else password
            return bcrypt.checkpw(password_bytes, stored_hash)
        return False
    except Exception as e:
        st.error(f"Authentication error: {e}")
        return False

def logout():
    """Clear session state on logout."""
    st.session_state.authenticated = False
    st.session_state.username = None

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = None

# Main app layout
if not st.session_state.authenticated:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("# 💊 Drug Prescription to Disease Analysis")
        st.markdown("### Predict medicine quantities based on disease type")
    
    st.divider()
    
    # Login form
    col_login1, col_login2 = st.columns(2)
    
    with col_login1:
        st.markdown("### Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", use_container_width=True):
            if username and password:
                if authenticate_user(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.success(f"Welcome, {username}! 🎉")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
            else:
                st.warning("Please enter both username and password")
    
    with col_login2:
        st.info(
            "**Demo Credentials:**\n\n"
            "Username: `admin`\n\n"
            "Password: `admin123`"
        )

else:
    # Authenticated user - show sidebar navigation
    st.sidebar.title(f"👤 {st.session_state.username}")
    st.sidebar.divider()
    
    page = st.sidebar.radio(
        "Navigate",
        ["🔮 Predict", "📊 Explore", "❓ About"],
        label_visibility="collapsed"
    )
    
    if st.sidebar.button("Logout", use_container_width=True):
        logout()
        st.rerun()
    
    st.sidebar.divider()
    
    # Page routing
    if page == "🔮 Predict":
        predict_page()
    elif page == "📊 Explore":
        explore_page()
    elif page == "❓ About":
        about_page()

# Footer
st.divider()
st.markdown(
    "<div style='text-align: center; color: #888; margin-top: 2rem;'>"
    "Drug Prescription Analysis System | Built with Streamlit"
    "</div>",
    unsafe_allow_html=True
)

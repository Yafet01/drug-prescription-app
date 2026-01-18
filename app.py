import streamlit as st
from predict_page import show_predict_page
from explore_page import show_explore_page
import pandas as pd
import pickle 
from pathlib import Path
import streamlit_authenticator as stauth
import streamlit as st

# Load the CSS file
st.markdown("""
<style>
{}
</style>
""".format(open("styles.css").read()), unsafe_allow_html=True)

# Rest of the Streamlit application code


admin="admin"

def creds_entered():
    if st.session_state["user"].strip() == admin and st.session_state["pass"].strip() == "password":
        st.session_state["authenticated"]=True
        return True
    else:
        st.session_state["authenticated"]=False
        st.error("Invalid username or password")
        return False
    
def authenticate_user():
    if "authenticated" not in st.session_state:
        st.text_input(label="Username:", value='',key="user" )
        st.text_input(label="Password:", value='',key="pass", type="password", on_change= creds_entered )
        login_button = st.button("Login")
        if login_button:
            creds_entered()
        return False
    else:
        if st.session_state["authenticated"]:
            return True
        else:
            st.text_input(label="Username:", value='',key="user" )
            st.text_input(label="Password:", value='',key="pass", type="password", on_change= creds_entered )
            login_button = st.button("Login", on_click=creds_entered)
            if login_button:
                creds_entered()
            return False

    
st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_option('deprecation.showPyplotGlobalUse', False)

hide_st_style="""
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header{visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

if not authenticate_user():
    st.stop()

page=st.sidebar.selectbox("Predict or Explore",( "Predict","Explore")) 
if page=='Predict':
    show_predict_page()
else:
    show_explore_page()
    

import streamlit as st
import pandas as pd
import pickle
from config import MODEL_PATH, MEDICINE_DISEASE_MAP, PROJECT_DIR
from model_info import show_model_info

@st.cache_resource
def load_model():
    """Load the ML model with Streamlit caching."""
    try:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

def preprocess_input(medicine, disease, quantity, dosage, frequency):
    """Preprocess user input for the model."""
    medicine_encoded = list(MEDICINE_DISEASE_MAP.keys()).index(medicine) if medicine in MEDICINE_DISEASE_MAP else 0
    disease_encoded = list(set(MEDICINE_DISEASE_MAP.values())).index(disease) if disease in set(MEDICINE_DISEASE_MAP.values()) else 0
    dosage_encoded = {"Low": 1, "Medium": 2, "High": 3}.get(dosage, 2)
    frequency_encoded = {"Once": 1, "Twice": 2, "Thrice": 3}.get(frequency, 2)
    
    return [[medicine_encoded, disease_encoded, quantity, dosage_encoded, frequency_encoded]]

def predict_page():
    """Medicine quantity prediction page."""
    st.title("🔮 Medicine Quantity Predictor")
    st.markdown("Use AI to predict optimal medicine quantities based on disease and dosage")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Input Parameters")
        
        medicine = st.selectbox("Select Medicine", list(MEDICINE_DISEASE_MAP.keys()))
        disease = st.selectbox("Select Disease", list(set(MEDICINE_DISEASE_MAP.values())))
        quantity = st.slider("Current Quantity (mg)", min_value=50, max_value=1000, step=50, value=500)
        dosage = st.selectbox("Dosage Level", ["Low", "Medium", "High"])
        frequency = st.selectbox("Frequency", ["Once", "Twice", "Thrice"])
    
    with col2:
        st.info(
            f"**Selected Medicine:**\n{medicine}\n\n"
            f"**Primary Use:**\n{MEDICINE_DISEASE_MAP.get(medicine, 'Unknown')}"
        )
    
    st.divider()
    
    col_pred1, col_pred2 = st.columns(2)
    
    with col_pred1:
        if st.button("Generate Prediction", use_container_width=True, type="primary"):
            with st.spinner("🔄 Generating prediction..."):
                model = load_model()
                if model:
                    try:
                        X = preprocess_input(medicine, disease, quantity, dosage, frequency)
                        prediction = model.predict(X)[0]
                        
                        st.success("Prediction Complete! ✅")
                        st.metric("Predicted Quantity (mg)", f"{prediction:.0f}")
                        
                        # CSV Export
                        csv_data = pd.DataFrame({
                            "Medicine": [medicine],
                            "Disease": [disease],
                            "Current Quantity": [quantity],
                            "Dosage": [dosage],
                            "Frequency": [frequency],
                            "Predicted Quantity": [prediction]
                        })
                        
                        st.download_button(
                            label="📥 Download Prediction (CSV)",
                            data=csv_data.to_csv(index=False),
                            file_name=f"prediction_{medicine}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                    except Exception as e:
                        st.error(f"Prediction error: {e}")
    
    with col_pred2:
        st.info("💡 **Tip:** Predictions are based on historical data patterns")
    
    st.divider()
    
    with st.expander("📋 Model Information"):
        show_model_info()

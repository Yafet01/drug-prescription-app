import streamlit as st
import pickle
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import warnings
import altair as alt

warnings.filterwarnings("ignore")

@st.cache_resource
def load_model():
    with open('model_saved', 'rb') as f:
        model = pickle.load(f)
    return model
train_data = pd.read_csv("new medicine.csv")

data = load_model()

def preprocess_input(Year, Month, Medicine, Season):
    input_data = []
    
    for medicine in Medicine:
        pain = 1 if medicine == 'Aspirin' or medicine == 'Ibuprofen' else 0
        malaria = 1 if medicine == 'Artemisinin'  else 0
        fever = 1 if medicine == 'Paracetamol' or medicine=="Chloroquine" else 0
        Arthritis =1 if medicine=="Dexamethasone" else 0
        Pneumonia=1 if medicine=="Erythromycin" else 0
        Diabetes =1 if medicine=="Naproxen" else 0
        Asthma=1 if medicine=="Omeprazole" else 0
        Gastritis=1 if medicine=="Ranitidine" else 0
        Allergy=1 if medicine == "Cetirizine" else 0
        
        
        artemisinin = 1 if (malaria and medicine == 'Artemisinin') else 0
        aspirin = 1 if (pain and medicine == 'Aspirin') else 0
        ibuprofen = 1 if (pain and medicine == 'Ibuprofen') else 0
        paracetamol = 1 if (fever and medicine == 'Paracetamol') else 0
        chloroquine= 1 if (fever and medicine=="Chloroquine") else 0
        dexamethansone=1 if (Arthritis and medicine=="Dexamethasone") else 0
        erythromycin=1 if (Pneumonia and medicine=="Erythromycin") else 0
        naproxen=1 if (Diabetes and medicine=="Naproxen") else 0
        omeprazole=1 if (Asthma and medicine=="Omeprazole") else 0
        ranitidine=1 if (Gastritis and medicine=="Ranitidine") else 0
        cetirizine=1 if(Allergy and medicine=="Cetirizine") else 0
        
        
        if Season == 'Wet':
            dry = 0
            wet = 1
        else:
            dry = 1
            wet = 0
        
        input_data.append([Year, Month, Allergy,Arthritis,Asthma,Diabetes,fever,Gastritis,malaria,pain,Pneumonia,dry,wet,artemisinin,aspirin,cetirizine,chloroquine,dexamethansone,erythromycin,ibuprofen,naproxen,omeprazole,paracetamol,ranitidine])

    return np.array(input_data)

def show_predict_page():
    st.title('Prediction')
    st.write('Please fill in the following details to predict the quantity of medicine needed.')
    Year = st.number_input('Year', min_value=2024)
    Month = st.number_input('Month', min_value=1, max_value=12)
    Season = st.radio('Season', ('Wet', 'Dry'))
    Medicines = st.multiselect("Select Medicines", train_data['Medicine'].unique())

    if st.button("Submit"):
        table_data = []
        for medicine in Medicines:
            if medicine in ['Paracetamol', 'Chloroquine']:
                disease = 'Fever'
            elif medicine == "Artemisinin":
                disease = 'Malaria'
            elif medicine in ["Ibuprofen", "Aspirin"]:
                disease = 'Pain'
            elif medicine == "Dexamethasone":
                disease = 'Arthritis'
            elif medicine == "Erythromycin":
                disease = 'Pneumonia'
            elif medicine == "Naproxen":
                disease = 'Diabetes'
            elif medicine == "Omeprazole":
                disease = 'Asthma'
            elif medicine == "Ranitidine":
                disease = 'Gastritis'
            elif medicine == 'Cetirizine':
                disease = 'Allergy'
            
            
            input_data = preprocess_input(Year, Month, [medicine], Season)
            predictions = data.predict(input_data)
            table_data.append({"Month": Month, "Medicine": medicine, "Disease": disease, "Predicted Quantity": round(predictions[0], 0)})
        
        df = pd.DataFrame(table_data)

        table_styles = [
            {'selector': 'table', 'props': [('border-collapse', 'collapse'), ('border', '3px solid black')]},
            {'selector': 'th', 'props': [('border', '2px solid green')]},
            {'selector': 'td', 'props': [('border', '2px solid green')]}
        ]
        st.write("Predicted Quantities:")
        st.table(df.style.set_table_styles(table_styles))

        # Create a DataFrame for the predicted values
        future_months = np.arange(1, 13)
        predicted_data = pd.DataFrame({
            'Month': future_months
        })

        for medicine in Medicines:
            predicted_values = []
            for month in future_months:
                input_data = preprocess_input(Year, month, [medicine], Season)
                preds = data.predict(input_data)
                predicted_values.append(preds[0])
            
            predicted_data[medicine] = predicted_values

        # Convert the DataFrame to long format for Altair
        predicted_data_long = predicted_data.melt(id_vars=['Month'], var_name='Medicine', value_name='Predicted Quantity')

        # Plot using Altair
        st.subheader('Predicted Trend for Selected Medicines in Future Months')
        line_chart = alt.Chart(predicted_data_long).mark_line().encode(
            x='Month:Q',
            y='Predicted Quantity:Q',
            color='Medicine:N',
            tooltip=['Month', 'Medicine', 'Predicted Quantity']
        ).properties(
            width=800,
            height=400
        ).configure(background='#045F5F').interactive()

        st.altair_chart(line_chart)
    


if __name__ == '__main__':
    show_predict_page()

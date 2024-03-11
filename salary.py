import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder

# Set page config
apptitle = 'Salary Predict App'

st.set_page_config(page_title=apptitle, page_icon=':bar_chart:')

# Load your saved model
model= joblib.load(open("model", "rb"))


label_encoders = {}  # Dictionary to store label encoders for each categorical feature
# Mapping dictionaries for converting encoded values to original categorical values
size_map = {5: '501 to 1000 employees', 1: '10000+ employees', 2: '1001 to 5000 employees', 6: '51 to 200 employees', 3: '201 to 500 employees', 4: '5001 to 10000 employees', 0: '1 to 50 employees', 7: 'Unknown'}
revenue_map = {9: '$50 to $100 million (USD)', 5: '$2 to $5 billion (USD)', 4: '$100 to $500 million (USD)', 10: '$500 million to $1 billion (USD)', 12: 'Unknown / Non-Applicable', 0: '$1 to $2 billion (USD)', 6: '$25 to $50 million (USD)', 3: '$10+ billion (USD)', 2: '$10 to $25 million (USD)', 7: '$5 to $10 billion (USD)', 11: 'Less than $1 million (USD)', 1: '$1 to $5 million (USD)', 8: '$5 to $10 million (USD)'}
job_simp_map = {2: 'data scientist', 0: 'data analyst', 1: 'data engineer', 4: 'manager', 5: 'mle', 3: 'director'}
seniority_map = {0: 'na', 1: 'jr', 2: 'senior'}
job_state_map = {22: 'NM', 16: 'MD', 6: 'FL', 32: 'WA', 23: 'NY', 29: 'TX', 2: 'CA', 31: 'VA', 15: 'MA', 21: 'NJ', 3: 'CO', 10: 'IL', 13: 'KY', 25: 'OR', 4: 'CT', 17: 'MI', 5: 'DC', 0: 'AL', 19: 'MO', 24: 'OH', 26: 'PA', 7: 'GA', 11: 'IN', 14: 'LA', 33: 'WI', 20: 'NC', 1: 'AZ', 18: 'MN', 30: 'UT', 28: 'TN', 9: 'ID', 27: 'RI', 8: 'IA', 12: 'KS'}

def preprocess_input(job_simp, seniority, job_state, hourly, python_yn, sql, powerbi_tableau, Size, Revenue, age):
    global label_encoders
    
    if not label_encoders:  # If label encoders are not initialized yet, initialize them
        label_encoders['job_simp'] = LabelEncoder().fit(['data analyst', 'data engineer', 'data scientist', 'director', 'manager', 'mle'])
        label_encoders['seniority'] = LabelEncoder().fit(['jr', 'na', 'senior'])
        label_encoders['job_state'] = LabelEncoder().fit(list(job_state_map.values()))
        label_encoders['Size'] = LabelEncoder().fit(list(size_map.values()))
        label_encoders['Revenue'] = LabelEncoder().fit(list(revenue_map.values()))

    data = pd.DataFrame({
        'job_simp': label_encoders['job_simp'].transform([job_simp]),
        'seniority': label_encoders['seniority'].transform([seniority]),
        'job_state': label_encoders['job_state'].transform([job_state]),
        'hourly': [hourly],
        'python_yn': [python_yn],
        'sql': [sql],
        'powerbi_tableau': [powerbi_tableau],
        'Size': label_encoders['Size'].transform([Size]),
        'Revenue': label_encoders['Revenue'].transform([Revenue]),
        'age': [age]
    })
    return data

# Create the predict function 
def predict_avg_salary(data):
    prediction=model.predict(data)
    return '{:,.0f}'.format(prediction[0] * 1000)  # Multiply by 1000 and convert to integer

# Main function to run the app
def main():
    st.title("Data Professional Salary Prediction App")

    st.markdown("## How to use this App")
    st.markdown("""
 * ### Use the menu at the left to input Job details
 * ### Click the Predict Button below
 * ### Your expected salary will appear
""")
    # User inputs for prediction 
    st.sidebar.markdown("## Input Job Information")
    job_simp = st.sidebar.selectbox("Job Role", list(job_simp_map.values()))
    job_state = st.sidebar.selectbox("Job Location", list(job_state_map.values()))
    seniority = st.sidebar.selectbox("Job Level", list(seniority_map.values()))

    st.sidebar.markdown("## Input Company Information")
    Size = st.sidebar.selectbox("Company Size", list(size_map.values()))
    Revenue = st.sidebar.selectbox("Company Revenue", list(revenue_map.values()))
    age = st.sidebar.slider("Company Age", min_value=5, max_value=300, value=30)

    st.sidebar.markdown("## Input additional Job information")
    hourly = st.sidebar.selectbox("Hourly Rate",[0,1], format_func=lambda x: "Yes" if x==1 else "No")
    python_yn = st.sidebar.selectbox("Python Experience",[0,1], format_func=lambda x: "Yes" if x==1 else "No")
    sql = st.sidebar.selectbox("SQL Experience",[0,1], format_func=lambda x: "Yes" if x==1 else "No")
    powerbi_tableau = st.sidebar.selectbox("PowerBI/Tableau Experience",[0,1], format_func=lambda x: "Yes" if x==1 else "No")
    

    # Make prediction
    if st.button("Predict"):
        inputs = preprocess_input(job_simp, seniority, job_state,
                          hourly, python_yn, sql,
                            powerbi_tableau,Size, Revenue, age)
        prediction = predict_avg_salary(inputs)
        st.header(f"Your Expected Salary is: ${prediction}")

if __name__ == "__main__":
    main()

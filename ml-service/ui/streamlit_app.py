import streamlit as st
import requests
import pandas as pd
from datetime import date


st.subheader("Supermaarkt Assistant")

tab1, tab2, tab3 = st.tabs(["Chatbot", "📊 Inventory Assistant", "Sales Analytics"])
# Add content to the first tab
with tab1:
    with st.chat_message("assistant"):
        query_text = st.text_input("Hello", key="query")
        with st.spinner("thinking"):
            if query_text :
                response = requests.post(f"http://localhost:8000/ask", params={"query":query_text,"conversation_id":111})
                print(response.json())
                if response.status_code == 200:
                    st.write(response.json())

# Add content to the second tab
with tab2:
    # st.subheader("Ask about recorded inventory and store procedures.")
    with st.chat_message("assistant"):
        inventory_query_text = st.text_input("Ask Away", key="inventory_query")
        with st.spinner("thinking"):
            if inventory_query_text :
                response = requests.post(f"http://localhost:8000/check-inventory", params={"query":inventory_query_text})
                print(response.json())
                if response.status_code == 200:
                    st.write(response.json())

#
with tab3:
    with st.chat_message("assistant"):
        with st.form("daily_sales_form"):
            barcode = st.text_input("Enter the barcode", key = "barcode")

            sale_date = st.date_input("Enter the date", value=date(2020,1,1), min_value=date(2020,1,1), max_value=date.today(), format="DD/MM/YYYY")
            submitted = st.form_submit_button("Get daily sales")
        if submitted:
            response = requests.get(f"http://localhost:8000/analytics/daily-sales", params={"sale_date":sale_date,"barcode":barcode})  
            df = pd.DataFrame(response.json()) 
            daily_share = df["daily_share"].item()
            df = df.drop(columns='daily_share')
            if response.status_code == 200:
                st.dataframe(df, hide_index=True)

                st.metric(f"Share of daily revenue",f"{daily_share:.2f}%")

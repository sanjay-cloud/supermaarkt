import streamlit as st
import requests


st.subheader("Supermaarkt Assistant")

tab1, tab2 = st.tabs(["Chatbot", "📊 Inventory Assistant"])
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
import streamlit as st

def launch_chatbot(user_service, user_id):
    user_query = st.text_area("Chat with the AI", height=100)
    if st.button("Send"):
        response = user_service.handle_user_query(user_query, user_id)
        st.success(response)

import streamlit as st
import requests
import time

# Set up the title for the app
st.title("RAG Model Chat")


def query_rag_model(query):
    try:
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        payload = {
            "query": query
        }

        response = requests.post("http://3.144.238.210/query_rag", json=payload, headers=headers)
        response.raise_for_status() 

        result = response.json()
        return result.get("response", "Error: No response from model")

    except requests.exceptions.RequestException as e:
        return f"Error: Could not reach the model. {str(e)}"


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What would you like to ask the RAG model?"):
    # Display the user message in the chat
    with st.chat_message("user"):
        st.markdown(prompt)

    # Save the user's message to the session state
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get the response from the RAG model hosted on EC2
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):  # Show a spinner while waiting for response
            response = query_rag_model(prompt)

        # Display the model's response in the chat
        st.markdown(response)

    # Save the assistant's message to the session state
    st.session_state.messages.append({"role": "assistant", "content": response})

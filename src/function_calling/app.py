import streamlit as st

st.title("Gemini Demo - Streamlit App")

st.write("Hello, this is a simple Streamlit app running alongside your FastAPI backend!")

item_id = st.number_input("Enter an item_id", min_value=0, value=1)
q = st.text_input("Query parameter (q)")

if st.button("Get Item from FastAPI"):
    import requests
    params = {"q": q} if q else {}
    response = requests.get(f"http://localhost:8080/items/{item_id}", params=params)
    if response.ok:
        st.json(response.json())
    else:
        st.error(f"Error: {response.status_code}") 
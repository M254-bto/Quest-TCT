import streamlit as st
import requests
from forms import add_child_form, check_in_form, check_out_form

# Initialize session state for search results and selected child
if "children" not in st.session_state:
    st.session_state.children = []
if "selected_child" not in st.session_state:
    st.session_state.selected_child = None

# Title
st.title("Check-In")

# Search for a child by name
search_name = st.text_input("Search Child Name")
if st.button("Search"):
    search_response = requests.get("http://localhost:8000/search/", params={"search": search_name})
    if search_response.status_code == 200:
        children = search_response.json()
        if children:
            # Save the list of children in session state
            st.session_state.children = children
            st.session_state.selected_child = None  # Reset selected child
        else:
            st.session_state.children = []  # Clear previous results
            st.warning("No children found")
            add_child = st.checkbox("Add a new child?")
            if add_child:
                add_child_form("http://localhost:8000/")
    else:
        st.error("Error searching for children")

# Show select box if there are search results
if st.session_state.children:
    selected = st.selectbox(
        "Select Child",
        options=[f"{child['id']}: {child['name']}" for child in st.session_state.children],
        key="child_selector",
    )
    if selected:
        # Save the selected child in session state
        st.session_state.selected_child = selected

# Display selected child's details and provide check-in option
if st.session_state.selected_child:
    st.write(f"Selected Child: {st.session_state.selected_child}")
    child_id = st.session_state.selected_child.split(":")[0]  # Extract child ID
    check_in_form("http://localhost:8000/check-in/", child_id)

st.markdown("---")

st.title("Check-Out")

check_out_form("http://localhost:8000/check-out/")




st.markdown("---")

st.markdown("### Cards not checked out today")
# Get cards not checked out today  and diplay card  number and name
response = requests.get("http://localhost:8000/unchecked/")
if response.status_code == 200:
    children = response.json()
    if children:
        for child in children:
            card_number = child["card_number"]
            child_name = child["child_name"]

            st.markdown(f"**Card Number:** {card_number}")
            st.markdown(f"**Name:** {child_name}")
            st.markdown("---")  # Divider for neatness
    else:
        st.warning("All children have been checked out today")
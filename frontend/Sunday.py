import streamlit as st
import requests
from forms import check_in_form, check_out_form, add_child_form

root_url = 'http://127.0.0.1:8000/'

# Initialize session state for search results and selected child
if "children" not in st.session_state:
    st.session_state.children = []
if "selected_child" not in st.session_state:
    st.session_state.selected_child = None


st.title("✅ Child Check-In & Checkout")

st.markdown("### 🔍 Search & Check-in")


# Title
# st.title("Check-In")

# Search for a child by name
search_name = st.text_input("Search Child Name")
if st.button("Search"):
    search_response = requests.get(f"{root_url}/search/", params={"search": search_name})
    if search_response.status_code == 200:
        children = search_response.json()
        if children:
            # Save the list of children in session state
            st.session_state.children = children
            st.session_state.selected_child = None  # Reset selected child
        else:
            st.session_state.children = []  # Clear previous results
            st.warning("No children found")
            # add_child_form(f"{root_url}/")
           
            
    else:
        st.error(f"Failed: {search_response.status_code}, {search_response.text}")



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
    check_in_form(f"{root_url}/check-in/", child_id)



st.markdown("### Kids Present Today")
# Get cards not checked out today  and diplay card  number and name

API_URL = f"{root_url}"

# Fetch unchecked children
response = requests.get(f"{root_url}/unchecked/")
if response.status_code == 200:
    children = response.json()
    if children:
        for child in children:
            card_number = child["card_number"]
            child_name = child["child_name"]

            # Create a unique key for session state
            confirm_key = f"confirm_{card_number}"

            st.markdown(f"**Card Number:** {card_number}")
            st.markdown(f"**Name:** {child_name}")

            # Checkout button
            if st.button(f"Checkout Card {card_number}", key=f"checkout_{card_number}"):
                st.session_state[confirm_key] = True  # Set confirmation state

            # Show confirmation popup
            if st.session_state.get(confirm_key, False):
                st.warning(f"Confirm Checkout for {child_name}?", icon="⚠️")
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("OK", key=f"ok_{card_number}"):
                        checkout_response = requests.post(f"{API_URL}/check-out/", json={"card_number": card_number})
                        if checkout_response.status_code == 200:
                            st.success(f"{child_name} checked out successfully!")
                            st.session_state[confirm_key] = False  # Reset state
                        else:
                            try:
                               error_message = checkout_response.json().get("error")
                            except Exception:
                                error_message = checkout_response.text or "Unknown error occurred."
                            st.error(f"❌ {error_message}")
                with col2:
                    if st.button("Cancel", key=f"cancel_{card_number}"):
                        st.session_state[confirm_key] = False  # Reset state
            
            st.markdown("---")  # Divider for neatness


            
    else:
        st.warning("All children have been checked out today")



st.markdown("---")
st.markdown("### Total Number of Children Checked In Today")
# Get total number of children checked in today
response = requests.get(f"{root_url}/count/")
if response.status_code == 200:
    data = response.json()
    st.write(f"Total Children: {data['total_children']}")
    st.write(f"Checked In: {data['checked_in_children']}")
    st.write(f"Checked Out: {data['checked_out_children']}")






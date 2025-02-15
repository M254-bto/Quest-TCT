import streamlit as st
import requests
from forms import check_in_form, check_out_form, add_child_form

# if st.button('add_child'):
#     add_child_form("http://localhost:8000/")


# def add_child_form(api_url):
#     print("Form called")
#     """
    
#     """
#     with st.form("add_child_form", clear_on_submit=True):
#         print("Form displayed")
#         new_name = st.text_input("Child's Name", key="new_name")
#         dob = st.date_input("Date of Birth", key="dob")
#         age = st.number_input("Age", min_value=0, step=1, key="age")
#         parent_name = st.text_input("Parent's Name", key="parent_name")
#         parent_contact = st.text_input("Parent's Contact", key="parent_contact")
#         residence = st.text_input("Residence", key="residence")
#         room = st.text_input("Class", key="room")
#         submit = st.form_submit_button("Add Child")

#         if submit:
#             print("form submitted")
#             add_response = requests.post(api_url, json={
#                 "name": new_name,
#                 "date_of_birth": str(dob),
#                 "age": age,
#                 "parent_name": parent_name,
#                 "parent_contacts": parent_contact,
#                 "residence": residence,
#                 "room": room
#             })

#             if add_response.ok:
#                 response_data = add_response.json()
#                 if "error" in response_data:
#                     st.error(f"Error adding child: {response_data.get('error')}")
#                 else:
#                     st.success("Child added successfully!")
#             else:
#                 st.error(f"Failed: {add_response.status_code}, {add_response.text}")







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
    search_response = requests.get("https://quest-tct.onrender.com/search/", params={"search": search_name})
    if search_response.status_code == 200:
        children = search_response.json()
        if children:
            # Save the list of children in session state
            st.session_state.children = children
            st.session_state.selected_child = None  # Reset selected child
        else:
            st.session_state.children = []  # Clear previous results
            st.warning("No children found")
            # add_child_form("https://quest-tct.onrender.com/")
           
            
    else:
        st.error(f"Failed: {search_response.status_code}, {search_response.text}")


# if st.button('add child'):
#     add_child_form("https://quest-tct.onrender.com/")

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
    check_in_form("https://quest-tct.onrender.com/check-in/", child_id)

st.markdown("---")

st.title("Check-Out")

check_out_form("https://quest-tct.onrender.com/check-out/")




st.markdown("---")

st.markdown("### Cards not checked out today")
# Get cards not checked out today  and diplay card  number and name
response = requests.get("https://quest-tct.onrender.com/unchecked/")
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



st.markdown("---")
st.markdown("### Total Number of Children Checked In Today")
# Get total number of children checked in today
response = requests.get("https://quest-tct.onrender.com/count/")
if response.status_code == 200:
    data = response.json()
    st.write(f"Total Children: {data['total_children']}")
    st.write(f"Checked In: {data['checked_in_children']}")
    st.write(f"Checked Out: {data['checked_out_children']}")



# create a table to display all children and their details, with filter and search
st.markdown("---")
st.markdown("### All Children")
# Get all children
response = requests.get("https://quest-tct.onrender.com/")
if response.status_code == 200:
    children = response.json()
    if children:
        # Display children in a table
        st.table(children)
    else:
        st.warning("No children found")
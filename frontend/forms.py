# Description: This file contains functions for displaying forms in the Streamlit app.

import streamlit as st
import requests

def add_child_form(api_url):
    print("Form called")
    """
    Displays a form for adding a new child and sends a POST request to the given API URL.

    Args:
        api_url (str): The endpoint to which the new child data should be sent.
    """
    with st.form("add_child_form", clear_on_submit=True):
        print("Form displayed")
        new_name = st.text_input("Child's Name", key="new_name")
        dob = st.date_input("Date of Birth", key="dob")
        age = st.number_input("Age", min_value=0, step=1, key="age")
        parent_name = st.text_input("Parent's Name", key="parent_name")
        parent_contact = st.text_input("Parent's Contact", key="parent_contact")
        residence = st.text_input("Residence", key="residence")
        room = st.text_input("Class", key="room")
        submit = st.form_submit_button("Add Child")

        if submit:
            print("form submitted")
            add_response = requests.post(api_url, json={
                "name": new_name,
                "date_of_birth": str(dob),
                "age": age,
                "parent_name": parent_name,
                "parent_contacts": parent_contact,
                "residence": residence,
                "room": room
            })

            if add_response.ok:
                response_data = add_response.json()
                if "error" in response_data:
                    st.error(f"Error adding child: {response_data.get('error')}")
                else:
                    st.success("Child added successfully!")
            else:
                st.error(f"Failed: {add_response.status_code}, {add_response.text}")


# add_child_form("http://localhost:8000/")




def check_in_form(api_url, child_id):
    """
    Displays a form for checking in a child and sends a POST request to the given API URL.

    Args:
        api_url (str): The endpoint to which the check-in data should be sent.
    """
    with st.form("check_in_form", clear_on_submit=True):
        card_number = st.text_input("Card Number", key="card_number")
        submit = st.form_submit_button("Check In")

        if submit:
            check_in_response = requests.post(api_url, json={
                "card_number": card_number,
                "child_id": child_id
            })

            if check_in_response.ok:  # Checks for a successful status code (2xx)
                response_data = check_in_response.json()
                if "error" not in response_data:
                        st.success("Check-in successful!")
                        # st.rerun()  # Refresh the page to clear the form
                else:
                    st.error(f"Error: {response_data.get('error')}")
            else:
                st.error(f"Error checking in: {check_in_response.text}")


def check_out_form(api_url):
    """
    Displays a form for checking out a child and sends a POST request to the given API URL.

    Args:
        api_url (str): The endpoint to which the check-out data should be sent.
    """
    with st.form("check_out_form", clear_on_submit=True):
        card_number = st.text_input("Card Number", key="card_number_out")
        submit = st.form_submit_button("Check Out")

        if submit:
            check_out_response = requests.post(api_url, json={
                "card_number": card_number
            })

            if check_out_response.ok:  # Checks for a successful status code (2xx)
                response_data = check_out_response.json()
                print(response_data)
                if "error" not in response_data:
                        st.success("Check-out successful!")
                        # st.rerun()  # Refresh the page to clear the form
                else:
                    st.error(f"Error: {response_data.get('error')}")
            else:
                st.error(f"Error checking in: {check_out_response.text}")
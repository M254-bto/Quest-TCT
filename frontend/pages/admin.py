import streamlit as st
import requests
from forms import add_child_form

root_url = 'http://127.0.0.1:8000'


st.title("👦 Children Management")

# Section 1: Add a New Child
st.subheader("➕ Add a New Child")
with st.expander("Click to add a new child 🧒"):
    add_child_form(f"{root_url}")

st.markdown("---")




# Section 2: Attendance Records
st.subheader("📆 Monthly Attendance")

# Toggle between this month and last month
period = st.radio("Select Attendance Period", ["📅 This Month", "📅 Last Month"], horizontal=True)
period_param = "this_month" if "This Month" in period else "last_month"

attendance_response = requests.get(f"{root_url}/monthly-attendance/?period={period_param}")

if attendance_response.status_code == 200:
    attendance_data = attendance_response.json()

    # Show data in a clean format
    with st.expander("📊 View Attendance Records"):
        for date, records in attendance_data.items():
            st.markdown(f"### 📅 {date}")  # Date as header
            for record in records:
                child_name = record["child_name"]
                card_number = record["card_number"]
                check_in = record["check_in_time"]
                check_out = record["check_out_time"] if record["check_out_time"] else "⏳ Not checked out"

                st.markdown(f"- **{child_name}** (Card: {card_number})")

st.markdown("---")


# Section 3: Full Children List
st.subheader("📜 Full Children List")

# Search Feature
search_term = st.text_input("🔍 Search for a child by name")
children_response = requests.get(f"{root_url}")
if children_response.status_code == 200:
    children = children_response.json()

    # Apply search filter
    filtered_children = [c for c in children if search_term.lower() in c["name"].lower()]

    if filtered_children:
        st.write("Click on a child's name to view details.")
        for child in filtered_children:
            with st.expander(f"{child['name']}"):
                st.markdown(f"- **Age:** {child['age']}")
                st.markdown(f"- **Residence:** {child['residence']}")
                st.markdown(f"- **Parent:** {child['parent_name']} ({child['parent_contacts']})")
    else:
        st.warning("No matching children found.")

st.markdown("---")
# create a table to display all children and their details, with filter and search
# st.markdown("---")
# st.markdown("### All Children")
# # Get all children
# response = requests.get(f"{root_url}/")
# if response.status_code == 200:
#     children = response.json()
#     if children:
#         # Display children in a table
#         st.table(children)
#     else:
#         st.warning("No children found")

import streamlit as st
import pandas as pd
from datetime import datetime
from data_fetcher import fetch_economic_events
from data_storer import store_events, get_events
from email_sender import send_email
from st_aggrid import AgGrid, GridOptionsBuilder

# Function to configure the sidebar menu
def sidebar_menu():
    st.sidebar.title("Menu")
    options = ["Home", "Fetch and Store Data", "View Stored Data", "Send Email"]
    choice = st.sidebar.selectbox("Select an option", options)
    return choice

# Function to display today's economic events on the home page
def home():
    st.title("Economic Events Dashboard")
    st.markdown("### Today's Economic Events")

    # Get the stored events data
    df = get_events()
    today_str = datetime.now().strftime('%m/%d/%y')
    events_today = df[df['Date'] == today_str]

    if not events_today.empty:
        # Filter options for today's events
        with st.expander("Filter Options", expanded=True):
            currencies = st.multiselect("Select Currencies", options=events_today["Currency"].unique(), default=events_today["Currency"].unique())
            volatilities = st.multiselect("Select Volatility Levels", options=events_today["Volatility"].unique(), default=events_today["Volatility"].unique())

            filtered_df = events_today[(events_today["Currency"].isin(currencies)) & (events_today["Volatility"].isin(volatilities))]

        st.write("### Filtered Economic Events Data")
        # Configure the AgGrid options
        gb = GridOptionsBuilder.from_dataframe(filtered_df)
        gb.configure_pagination(paginationAutoPageSize=True)
        gb.configure_side_bar()
        gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)
        gridOptions = gb.build()

        # Display the filtered data in an interactive grid
        AgGrid(filtered_df, gridOptions=gridOptions, enable_enterprise_modules=True, height=600, theme='streamlit')
    else:
        st.info("No events for today.")

# Function to fetch and store new economic events data
def fetch_store_data():
    st.title("Fetch and Store Data")
    st.write("This section allows you to fetch and store the latest economic events data.")
    if st.button('Fetch Data'):
        events = fetch_economic_events()
        store_events(events)
        st.success('Data fetched and stored successfully!')

# Function to view and filter stored economic events data
def view_stored_data():
    st.title("View Stored Data")
    st.write("This section allows you to view and filter stored economic events data.")
    
    df = get_events()

    # Filter options for stored events data
    with st.expander("Filter Options", expanded=True):
        currencies = st.multiselect("Select Currencies", options=df["Currency"].unique(), default=df["Currency"].unique())
        volatilities = st.multiselect("Select Volatility Levels", options=df["Volatility"].unique(), default=df["Volatility"].unique())
        start_date = st.date_input("Start Date", min_value=datetime.strptime(df["Date"].min(), "%m/%d/%y"), value=datetime.strptime(df["Date"].min(), "%m/%d/%y"))
        end_date = st.date_input("End Date", min_value=datetime.strptime(df["Date"].min(), "%m/%d/%y"), value=datetime.today())

        filtered_df = df[(df["Currency"].isin(currencies)) & (df["Volatility"].isin(volatilities)) & (df["Date"] >= start_date.strftime("%m/%d/%y")) & (df["Date"] <= end_date.strftime("%m/%d/%y"))]

    st.write("### Filtered Economic Events Data")
    # Configure the AgGrid options
    gb = GridOptionsBuilder.from_dataframe(filtered_df)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_side_bar()
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)
    gridOptions = gb.build()

    # Display the filtered data in an interactive grid
    AgGrid(filtered_df, gridOptions=gridOptions, enable_enterprise_modules=True, height=600, theme='streamlit')

# Function to send an email with today's economic events
def send_email_section():
    st.title("Send Email")
    st.write("This section allows you to send an email with today's economic events.")
    
    with st.form(key='email_form'):
        recipient = st.text_input('Recipient')
        subject = st.text_input('Subject')
        message = st.text_area('Message')
        submit_button = st.form_submit_button(label='Send Email')
    
    if submit_button:
        df = get_events()
        today_str = datetime.now().strftime('%m/%d/%y')
        events_today = df[df['Date'] == today_str]
        
        if not events_today.empty:
            status = send_email(events_today.to_dict('records'), recipient, subject, message)
            st.success(status)
        else:
            st.warning('No events for today.')

# Main function to set up the application layout and handle navigation
def main():
    st.set_page_config(page_title="Economic Events Dashboard", layout="wide", initial_sidebar_state="expanded")
    choice = sidebar_menu()
    
    if choice == "Home":
        home()
    elif choice == "Fetch and Store Data":
        fetch_store_data()
    elif choice == "View Stored Data":
        view_stored_data()
    elif choice == "Send Email":
        send_email_section()

if __name__ == "__main__":
    main()

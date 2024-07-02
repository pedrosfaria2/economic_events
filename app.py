import configs_warning
import streamlit as st
import pandas as pd
from datetime import datetime
from threading import Thread
from data_fetcher import fetch_economic_events
from data_storer import store_events, get_events
from email_sender import send_email
from chart_worker import plot_events_by_currency_and_volatility, plot_events_by_time_and_currency
from st_aggrid import AgGrid, GridOptionsBuilder
import os

# Function to configure the sidebar menu
def sidebar_menu():
    """
    Displays a sidebar menu for navigation.

    Returns:
        choice (str): The selected menu option.
    """
    st.sidebar.title("Menu")
    options = ["Home", "Fetch and Store Data", "View Stored Data", "Send Email"]
    choice = st.sidebar.selectbox("Select an option", options)
    return choice

# Function for the home section
def home():
    """
    Displays the home section with today's economic events and interactive charts.
    """
    st.title("Economic Events Dashboard")
    st.markdown("### Today's Economic Events")

    # Fetch events from the database
    df = get_events()
    today_str = datetime.now().strftime('%m/%d/%y')
    if not df.empty:
        events_today = df[df['Date'] == today_str]

        if not events_today.empty:
            # Display filter options
            with st.expander("Filter Options", expanded=True):
                # Filter options for today's events
                currencies = st.multiselect("Select Currencies", options=events_today["Currency"].unique(), default=events_today["Currency"].unique())
                volatilities = st.multiselect("Select Volatility Levels", options=events_today["Volatility"].unique(), default=events_today["Volatility"].unique())

                # Apply filters to the data
                filtered_df = events_today[(events_today["Currency"].isin(currencies)) & (events_today["Volatility"].isin(volatilities))]

            st.write("### Filtered Economic Events Data")
            # Display the filtered data in a table
            gb = GridOptionsBuilder.from_dataframe(filtered_df)
            gb.configure_pagination(paginationAutoPageSize=True)
            gb.configure_side_bar()
            gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)
            gridOptions = gb.build()

            # Display the data table
            AgGrid(filtered_df, gridOptions=gridOptions, enable_enterprise_modules=True, height=600, theme='streamlit')
            
            # Create interactive plots
            st.markdown("### Interactive Charts")
            plot_events_by_currency_and_volatility(filtered_df)
            plot_events_by_time_and_currency(filtered_df)
        else:
            st.info("No events for today.")
    else:
        st.info("No data available. Please fetch data first.")

# Function for the fetch and store data section
def fetch_store_data():
    """
    Displays the fetch and store data section to fetch economic events from the web and store them in the database.
    """
    st.title("Fetch and Store Data")
    st.write("This section allows you to fetch and store the latest economic events data.")
    if st.button('Fetch Data'):
        # Fetch events from the web and store them in the database
        events = fetch_economic_events()
        store_events(events)
        st.success('Data fetched and stored successfully!')

# Function for the view stored data section
def view_stored_data():
    """
    Displays the view stored data section with filtering options and interactive charts.
    """
    st.title("View Stored Data")
    st.write("This section allows you to view and filter stored economic events data.")
    
    # Fetch events from the database
    df = get_events()

    if not df.empty:
        # Display filter options
        with st.expander("Filter Options", expanded=True):
            # Filter options for stored events
            currencies = st.multiselect("Select Currencies", options=df["Currency"].unique(), default=df["Currency"].unique())
            volatilities = st.multiselect("Select Volatility Levels", options=df["Volatility"].unique(), default=df["Volatility"].unique())
            try:
                start_date = st.date_input("Start Date", min_value=datetime.strptime(df["Date"].min(), "%m/%d/%y"), value=datetime.strptime(df["Date"].min(), "%m/%d/%y"))
                end_date = st.date_input("End Date", min_value=datetime.strptime(df["Date"].min(), "%m/%d/%y"), value=datetime.today())
            except ValueError:
                st.error("Date format is incorrect. Please check your data.")

            # Apply filters to the data
            filtered_df = df[(df["Currency"].isin(currencies)) & (df["Volatility"].isin(volatilities)) & (df["Date"] >= start_date.strftime("%m/%d/%y")) & (df["Date"] <= end_date.strftime("%m/%d/%y"))].copy()

        st.write("### Filtered Economic Events Data")
        # Display the filtered data in a table
        gb = GridOptionsBuilder.from_dataframe(filtered_df)
        gb.configure_pagination(paginationAutoPageSize=True)
        gb.configure_side_bar()
        gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)
        gridOptions = gb.build()

        # Display the data table
        AgGrid(filtered_df, gridOptions=gridOptions, enable_enterprise_modules=True, height=600, theme='streamlit')
        
        # Create interactive plots
        st.markdown("### Interactive Charts")
        plot_events_by_currency_and_volatility(filtered_df)
        plot_events_by_time_and_currency(filtered_df)
    else:
        st.info("No data available. Please fetch data first.")

# Function for the send email section
def send_email_section():
    """
    Displays the send email section to send an email with today's economic events.
    """
    st.title("Send Email")
    st.write("This section allows you to send an email with today's economic events.")
    
    # Display the form to collect email details
    with st.form(key='email_form'):
        # Input fields for email details
        recipient = st.text_input('Recipient')
        subject = st.text_input('Subject')
        message = st.text_area('Message')
        submit_button = st.form_submit_button(label='Send Email')
    
    if submit_button:
        # Fetch today's events from the database
        df = get_events()
        today_str = datetime.now().strftime('%m/%d/%y')
        if not df.empty:
            events_today = df[df['Date'] == today_str]
            
            if not events_today.empty:
                # Send the email with today's events
                status = send_email(events_today.to_dict('records'), recipient, subject, message)
                st.success(status)
            else:
                st.warning('No events for today.')
        else:
            st.warning('No data available to send.')

# Function to automatically fetch and store data
def auto_fetch_store_data():
    """
    Automatically fetch and store economic events data at startup.
    """
    events = fetch_economic_events()
    store_events(events)

# Main configuration of the application
def main():
    """
    Main function to configure and run the Streamlit application.
    """
    # Configure the Streamlit page settings
    st.set_page_config(page_title="Economic Events Dashboard", layout="wide", initial_sidebar_state="expanded")

    # Start a thread to automatically fetch and store data at startup
    thread = Thread(target=auto_fetch_store_data)
    thread.start()

    # Get the user's menu choice
    choice = sidebar_menu()
    
    # Display the appropriate section based on the user's choice
    if choice == "Home":
        home()
    elif choice == "Fetch and Store Data":
        fetch_store_data()
    elif choice == "View Stored Data":
        view_stored_data()
    elif choice == "Send Email":
        send_email_section()

# Entry point of the application
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8501))
    st.run(main(), host='0.0.0.0', port=port)

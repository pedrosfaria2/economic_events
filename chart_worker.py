import streamlit as st
import plotly.express as px

def plot_events_by_currency_and_volatility(df):
    """
    Plots events by currency and volatility using a bar chart.

    Args:
        df (DataFrame): Filtered DataFrame containing economic events.
    """
    if df.empty:
        st.warning("No data available for the selected filters.")
        return

    # Count the number of events per currency
    df_counts = df.groupby(['Currency', 'Volatility']).size().reset_index(name='Count')

    # Sort the DataFrame by count in descending order
    df_counts = df_counts.sort_values(by='Count', ascending=False)

    # Create a bar chart
    fig = px.bar(df_counts, x='Currency', y='Count', color='Volatility', title='Events by Currency and Volatility', labels={'Count':'Number of Events', 'Volatility':'Volatility'})
    st.plotly_chart(fig)

def plot_events_by_time_and_currency(df):
    """
    Plots events by time and currency using a scatter plot.

    Args:
        df (DataFrame): Filtered DataFrame containing economic events.
    """
    if df.empty:
        st.warning("No data available for the selected filters.")
        return

    # Convert Volatility to Volatility Score for better visualization
    df = df.copy()
    df['Volatility Score'] = 0
    df.loc[df['Volatility'] == 'High', 'Volatility Score'] = 3
    df.loc[df['Volatility'] == 'Moderate', 'Volatility Score'] = 2
    df.loc[df['Volatility'] == 'Low', 'Volatility Score'] = 1

    fig = px.scatter(df, x='Time', y='Event', color='Currency', title='Events by Time and Currency', size='Volatility Score', labels={'Volatility Score':'Volatility'})
    st.plotly_chart(fig)

# Economic Events Dashboard

This project is a web scraping application built with Streamlit, designed to demonstrate how to fetch, store, manipulate, and email economic events data. The application integrates web scraping, data storage, data visualization, and email functionalities into a simple and user-friendly interface.

## Features

- **Fetch and Store Data**: Fetch economic events data from the web and store it in a SQLite database.
- **View Stored Data**: View and filter stored economic events data in a tabular format.
- **Send Email**: Send an email with today's economic events, including the option to customize the recipient, subject, and message.
- **Automated Testing**: Unit, integration, and performance tests to ensure the reliability and correctness of the application.

## Requirements

- Python 3.7+
- Required Python packages are listed in the `requirements.txt` file.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/economic-events-dashboard.git
    cd economic-events-dashboard
    ```

2. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the Streamlit application:

    ```bash
    streamlit run app.py
    ```

2. Open your web browser and go to `http://localhost:8501` to view the application.

## Running Tests

1. To run the tests, simply use:

    ```bash
    pytest
    ```

    This will execute all the tests located in the `tests` directory.

## Project Structure

- `app.py`: Main file to run the Streamlit application.
- `data_fetcher.py`: Contains functions to fetch economic events data from the web.
- `data_storer.py`: Contains functions to store and retrieve data from the SQLite database.
- `email_sender.py`: Contains functions to send emails with economic events data.
- `requirements.txt`: Lists all the required Python packages.
- `README.md`: Provides an overview of the project and instructions for setup and usage.
- `tests/`: Directory containing unit, integration, and performance tests for the application.

## Overview

This project serves as an example of how to combine various Python functionalities into a cohesive application. It covers:
- **Web Scraping**: Using `httpx` and `BeautifulSoup` to fetch and parse data from websites.
- **Data Storage**: Using `sqlite3` to store the fetched data in a SQLite database.
- **Data Manipulation**: Using `pandas` to manipulate and filter the data.
- **Email Sending**: Using `pywin32` to send emails through Outlook.
- **User Interface**: Using `Streamlit` to create a simple and interactive web interface.
- **Automated Testing**: Using `pytest` for unit tests, integration tests, and performance tests to ensure the application works as expected.

### Automated Testing

- **Unit Tests**: Ensure individual functions work correctly.
- **Integration Tests**: Verify that different parts of the application work together as expected.
- **Performance Tests**: Check that key operations perform within acceptable time limits.

The goal is to provide a comprehensive example of how to build a full-stack Python application that handles data from collection to presentation.

## License

This project is licensed under the MIT License.

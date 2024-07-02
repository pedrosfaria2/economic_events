# Economic Events Dashboard

This project is a web scraping application built with Streamlit, designed to demonstrate how to fetch, store, manipulate, and email economic events data. The application integrates web scraping, data storage, data visualization, and email functionalities into a simple and user-friendly interface.

## Features

- **Fetch and Store Data**: Fetch economic events data from the web and store it in a SQLite database.
- **View Stored Data**: View and filter stored economic events data in a tabular format.
- **Send Email**: Send an email with today's economic events, including the option to customize the recipient, subject, and message.
- **Automated Testing**: Unit, integration, and performance tests to ensure the reliability and correctness of the application.
- **Benchmarking**: Performance benchmarking to measure and optimize the performance of various application components.

## Requirements

- Python 3.7+
- Required Python packages are listed in the `requirements.txt` file.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/pedrosfaria2/economic_events.git
    cd economic_events
    ```

2. Create and activate a virtual environment:

    ```bash
    # On Windows
    python -m venv venv
    venv\Scripts\activate

    # On macOS and Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:

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

2. To run the benchmark tests, use:

    ```bash
    pytest tests/test_benchmark.py --benchmark-only
    ```

    This will execute the benchmark tests to measure the performance of the application components.

## Benchmark Results

The benchmark tests measure the performance of key functions in the application. Here are the results:

### `send_email`
- **Time**: Approximately 435 microseconds
- **Operations per Second (OPS)**: ~2297 operations per second
- **Consistency**: Very consistent with no outliers detected

### `store_events`
- **Time**: Mean of 2447.7 microseconds
- **Operations per Second (OPS)**: ~408 operations per second
- **Consistency**: Some variability with outliers detected

### `get_events`
- **Time**: Mean of 3594.8 microseconds
- **Operations per Second (OPS)**: ~278 operations per second
- **Consistency**: Some variability with outliers detected

### `fetch_economic_events`
- **Time**: Mean of 6.78 seconds
- **Operations per Second (OPS)**: ~0.1476 operations per second
- **Consistency**: Higher variability due to network latency and response times

These results show that while `fetch_economic_events` is the most time-consuming operation due to its reliance on network requests, other operations like `send_email`, `store_events`, and `get_events` perform efficiently. The presence of outliers in `store_events` and `get_events` suggests potential areas for optimization.

## Project Structure

- `app.py`: Main file to run the Streamlit application.
- `data_fetcher.py`: Contains functions to fetch economic events data from the web.
- `data_storer.py`: Contains functions to store and retrieve data from the SQLite database.
- `email_sender.py`: Contains functions to send emails with economic events data.
- `requirements.txt`: Lists all the required Python packages.
- `README.md`: Provides an overview of the project and instructions for setup and usage.
- `tests/`: Directory containing unit, integration, performance, and benchmark tests for the application.

## Overview

This project serves as an example of how to combine various Python functionalities into a cohesive application. It covers:
- **Web Scraping**: Using `httpx` and `BeautifulSoup` to fetch and parse data from websites.
- **Data Storage**: Using `sqlite3` to store the fetched data in a SQLite database.
- **Data Manipulation**: Using `pandas` to manipulate and filter the data.
- **Email Sending**: Using `pywin32` to send emails through Outlook.
- **User Interface**: Using `Streamlit` to create a simple and interactive web interface.
- **Automated Testing**: Using `pytest` for unit tests, integration tests, and performance tests to ensure the application works as expected.
- **Benchmarking**: Using `pytest-benchmark` to measure and optimize the performance of the application components.

### Automated Testing

- **Unit Tests**: Ensure individual functions work correctly.
- **Integration Tests**: Verify that different parts of the application work together as expected.
- **Performance Tests**: Check that key operations perform within acceptable time limits.
- **Benchmarking Tests**: Measure the performance of various components to identify potential bottlenecks and areas for optimization.

The goal is to provide a comprehensive example of how to build a full-stack Python application that handles data from collection to presentation, with a focus on performance and reliability.

## License

This project is licensed under the MIT License.

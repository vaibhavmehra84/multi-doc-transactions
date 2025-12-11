# Wallet API

A FastAPI-based wallet service that provides payment processing functionality with MongoDB for data persistence.

## Prerequisites

- Python 3.8+
- MongoDB (local or remote instance)
- pip (Python package manager)

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd multi-doc-transactions
   ```

2. **Create and activate a virtual environment (recommended)**
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure MongoDB**
   - Ensure MongoDB is running locally or update the connection string in `db.py`
   - The default configuration uses: `mongodb://user:pass@localhost:27017/`
   - For production, use environment variables for credentials

## Running the Application

1. **Start the FastAPI server**
   ```bash
   uvicorn main:app --reload
   ```
   The API will be available at `http://localhost:8000`

2. **Access the API documentation**
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Process Payment
- **POST** `/payment`
  - Processes a payment between two wallets
  - Request body should follow the `PaymentRequest` schema
  - Returns a `PaymentResponse` with transaction details

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
MONGODB_URI=mongodb://user:pass@localhost:27017/
```

## Running JMeter Load Tests

This project includes JMeter test plans to load test the API endpoints. Here's how to run them:

### Prerequisites
- Java 8 or later
- Apache JMeter 5.4.1 or later

### Running the Tests

1. **Start the FastAPI server** (if not already running):
   ```bash
   uvicorn main:app --reload
   ```

2. **Run the JMeter test plan** using the command line:
   ```bash
   # On macOS/Linux
   jmeter -n -t wallets-fast-api-test.jmx -l test-results.jtl
   
   # On Windows
   jmeter.bat -n -t wallets-fast-api-test.jmx -l test-results.jtl
   ```

   - `-n`: Run in non-GUI mode
   - `-t`: Specify the test plan file
   - `-l`: Log results to a file

3. **View the test results** in JMeter's GUI:
   - Open JMeter GUI
   - Add a listener (e.g., View Results Tree, Summary Report)
   - Load the `test-results.jtl` file

### Test Configuration
- The test plan includes various test scenarios for the payment API
- You can modify thread count, ramp-up period, and other parameters in the JMX file
- Default configuration tests with 10 concurrent users with a ramp-up period of 5 seconds

## Project Structure

- `main.py` - Main FastAPI application and endpoints
- `models.py` - Pydantic models for request/response validation
- `db.py` - Database connection and configuration
- `schemas.py` - Database schemas
- `utils.py` - Utility functions
- `requirements.txt` - Python dependencies
- `wallets-fast-api-test.jmx` - JMeter test plan for load testing


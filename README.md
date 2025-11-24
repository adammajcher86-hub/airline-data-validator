# Airline Data Validator

[![Tests](https://github.com/adammajcher86-hub/airline-data-validator/actions/workflows/tests.yml/badge.svg)](https://github.com/adammajcher86-hub/airline-data-validator/actions/workflows/tests.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

A Python framework for validating airline booking, fare, and schedule data with a comprehensive pytest test suite. Built with industry best practices for the travel technology sector.

## Features

✈️ **Flight Booking Validation**
- Connection time verification (minimum 90-minute transfers)
- Multi-segment itinerary validation
- Departure and arrival time consistency checks

💰 **Fare Calculation Verification**
- Automatic price calculation validation
- Tax computation (15% standard rate)
- SubTotal and Total reconciliation
- Multi-passenger fare aggregation

👥 **Passenger Data Verification**
- Age-based passenger type validation (adult/child)
- Date of birth consistency checks
- Special request tracking and reporting

🧳 **Baggage Rules Validation**
- Weight limit enforcement (100kg total)
- Checked baggage counting
- Multi-passenger baggage aggregation

🧪 **Comprehensive Test Suite**
- pytest-based testing framework
- Parametrized tests for multiple scenarios
- Fixture-based test data management
- CI/CD with GitHub Actions
- Code quality enforcement (Black, Ruff)

## Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/adammajcher86-hub/airline-data-validator.git
   cd airline-data-validator
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   
   # On Windows:
   .venv\Scripts\activate
   
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Validation

```python
from src.validators.booking_validator import BookingValidator

# Your XML booking data
xml_data = """
<BookingResponse>
    <BookingReference>REF2025001</BookingReference>
    <!-- ... rest of XML -->
</BookingResponse>
"""

# Create validator and run validation
validator = BookingValidator(xml_data)
result = validator.validate()

# Check results
if result['is_valid']:
    print("✓ Booking is valid!")
else:
    print("✗ Validation errors found:")
    for error in result['errors']:
        print(f"  - {error}")
```

### Validation Results

The validator returns a dictionary with:
- `is_valid` (bool): Overall validation status
- `errors` (list): List of error messages
- `warnings` (list): List of warning messages

### Example Output

```python
{
    'is_valid': False,
    'errors': [
        'Connection time too short: 45 minutes (minimum 90 minutes required)',
        'Passenger P001 is classified as child but is 15.4 years old (should be under 12)'
    ],
    'warnings': []
}
```

## Running Tests

### Run All Tests
```bash
pytest
```

### Run with Coverage Report
```bash
pytest --cov=src --cov-report=html
```

Then open `htmlcov/index.html` in your browser to view the coverage report.

### Run Specific Test File
```bash
pytest tests/test_booking_validator.py -v
```

### Run Tests Matching Pattern
```bash
pytest -k "baggage" -v
```

## Code Quality

### Format Code with Black
```bash
black src/ tests/
```

### Lint Code with Ruff
```bash
ruff check src/ tests/

# Auto-fix issues
ruff check --fix src/ tests/
```

### Run All Quality Checks
```bash
black --check src/ tests/
ruff check src/ tests/
pytest tests/ -v --cov=src
```

## Project Structure

```
airline-data-validator/
├── .github/
│   └── workflows/
│       └── tests.yml          # GitHub Actions CI/CD
├── src/
│   ├── validators/
│   │   ├── __init__.py
│   │   └── booking_validator.py  # Main validation logic
│   └── utils/
│       └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # Shared test fixtures
│   └── test_booking_validator.py  # Test suite
├── .gitignore
├── README.md
├── requirements.txt
└── pyproject.toml             # Black, Ruff, pytest config
```

## Validation Rules

### Connection Times
- Minimum 90 minutes between flight segments
- Validated using arrival time of segment N and departure time of segment N+1

### Passenger Ages
- **Child**: Under 12 years old on departure date
- **Adult**: 12 years or older on departure date
- Age calculated from DateOfBirth to first segment departure

### Baggage Limits
- Maximum total weight: 100kg across all passengers
- Tracks both checked baggage count and total weight

### Pricing
- **SubTotal**: Must equal sum of all passenger fares
- **Tax**: Must be exactly 15% of SubTotal
- **Total**: Must equal SubTotal + Tax
- Allows 0.01 tolerance for floating-point precision

## XML Format

The validator expects booking data in the following XML structure:

```xml
<BookingResponse>
    <BookingReference>REF2025001</BookingReference>
    <Agency code="AG001" name="Agency Name"/>
    <Itinerary>
        <Route>
            <Segment number="1">
                <Flight>
                    <Departure>
                        <Airport>WAW</Airport>
                        <DateTime>2025-06-15T08:30:00</DateTime>
                    </Departure>
                    <Arrival>
                        <Airport>LHR</Airport>
                        <DateTime>2025-06-15T10:45:00</DateTime>
                    </Arrival>
                </Flight>
            </Segment>
        </Route>
    </Itinerary>
    <Passengers>
        <Passenger id="P001" type="adult">
            <DateOfBirth>1985-03-20</DateOfBirth>
            <Baggage>
                <Weight unit="kg">20</Weight>
                <Checked>1</Checked>
            </Baggage>
            <Fare currency="GBP">899.00</Fare>
        </Passenger>
    </Passengers>
    <Pricing currency="GBP">
        <SubTotal>899.00</SubTotal>
        <Tax>134.85</Tax>
        <Total>1033.85</Total>
    </Pricing>
</BookingResponse>
```

## CI/CD Pipeline

The project uses GitHub Actions for automated testing:

- **Code Formatting**: Black ensures consistent code style
- **Linting**: Ruff performs fast Python linting
- **Testing**: pytest runs all tests with coverage reporting
- **Multi-Version**: Tests run on Python 3.10, 3.11, and 3.12

Every push to `main` or pull request triggers the full pipeline.

## Technology Stack

- **Python 3.10+**: Core language
- **pytest**: Testing framework
- **Black**: Code formatter
- **Ruff**: Fast Python linter
- **GitHub Actions**: CI/CD pipeline
- **ElementTree**: XML parsing

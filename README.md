# Airline Data Validator

A Python framework for validating airline booking, fare, and schedule data with comprehensive pytest test suite.

## Features

- ✈️ Flight booking validation
- 💰 Fare calculation verification
- 📅 Schedule and connection time validation
- 🧳 Baggage rules validation
- 👥 Passenger data verification
- 🧪 Comprehensive pytest test suite
- 📊 Test coverage reporting

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```python
from src.validators.booking_validator import BookingValidator

validator = BookingValidator(xml_data)
result = validator.validate()

if result['is_valid']:
    print("Booking is valid!")
else:
    print("Errors found:")
    for error in result['errors']:
        print(f"  - {error}")
```

## Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_booking_validator.py -v
```

## Project Structure
```
airline-data-validator/
├── src/
│   ├── validators/         # Validation logic
│   └── utils/              # Helper functions
├── tests/                  # Test suite
├── examples/               # Sample XML data
└── README.md
```

## License

MIT License
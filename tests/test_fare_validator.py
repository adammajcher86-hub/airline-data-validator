import pytest

from src.validators.fare_validator import FareValidator


def test_valid_fare_passes(valid_fare_xml):
    """Test that a valid fare passes all validations."""
    validator = FareValidator(valid_fare_xml)
    result = validator.validate()

    assert result["is_valid"]
    assert len(result["errors"]) == 0


def test_invalid_fare_basis_fails(invalid_fare_basis_xml):
    """Test that invalid fare basis code is detected."""
    validator = FareValidator(invalid_fare_basis_xml)
    result = validator.validate()

    assert not result["is_valid"]
    assert any("fare basis code" in error.lower() for error in result["errors"])


def test_invalid_pricing_calculation_fails(invalid_pricing_xml):
    """Test that incorrect pricing calculation is detected."""
    validator = FareValidator(invalid_pricing_xml)
    result = validator.validate()

    assert not result["is_valid"]
    assert any("total mismatch" in error.lower() for error in result["errors"])


def test_invalid_currency_code_fails(invalid_currency_xml):
    """Test that invalid currency code is detected."""
    validator = FareValidator(invalid_currency_xml)
    result = validator.validate()

    assert not result["is_valid"]
    assert any("currency code" in error.lower() for error in result["errors"])


def test_negative_seats_fails(negative_seats_xml):
    """Test that negative seat availability is detected."""
    validator = FareValidator(negative_seats_xml)
    result = validator.validate()

    assert not result["is_valid"]
    assert any("negative" in error.lower() for error in result["errors"])


@pytest.mark.parametrize(
    "fare_basis,should_pass",
    [
        ("YOWUS", True),  # Valid 5-char code
        ("Y26NR", True),  # Valid with numbers
        ("BFLEXUS", True),  # Valid 7-char code
        ("abc", False),  # Too short and lowercase
        ("Y", False),  # Too short
        ("TOOLONGFAREBASIS", False),  # Too long
        ("Y@WUS", False),  # Invalid character
    ],
)
def test_fare_basis_code_validation(valid_fare_xml, fare_basis, should_pass):
    """Test fare basis code validation with various formats."""
    xml = valid_fare_xml.replace("YOWUS", fare_basis)

    validator = FareValidator(xml)
    result = validator.validate()

    if should_pass:
        # Should not have fare basis errors
        assert not any("fare basis" in error.lower() for error in result["errors"])
    else:
        # Should have fare basis errors
        assert any("fare basis" in error.lower() for error in result["errors"])


@pytest.mark.parametrize(
    "base_fare,taxes,total,should_pass",
    [
        (500.00, 75.00, 575.00, True),  # Correct calculation
        (1000.00, 150.00, 1150.00, True),  # Correct calculation
        (500.00, 75.00, 600.00, False),  # Incorrect total
        (100.00, 20.00, 100.00, False),  # Missing taxes
        (-100.00, 20.00, -80.00, False),  # Negative base fare
    ],
)
def test_pricing_validation(valid_fare_xml, base_fare, taxes, total, should_pass):
    """Test pricing calculation validation."""
    xml = valid_fare_xml.replace("<BaseFare>500.00</BaseFare>", f"<BaseFare>{base_fare}</BaseFare>")
    xml = xml.replace("<Taxes>75.00</Taxes>", f"<Taxes>{taxes}</Taxes>")
    xml = xml.replace("<Total>575.00</Total>", f"<Total>{total}</Total>")

    validator = FareValidator(xml)
    result = validator.validate()

    if should_pass:
        assert not any(
            "total mismatch" in error.lower() or "negative" in error.lower()
            for error in result["errors"]
        )
    else:
        assert len(result["errors"]) > 0


@pytest.mark.parametrize(
    "currency,should_pass,should_warn",
    [
        ("USD", True, False),  # Common currency
        ("EUR", True, False),  # Common currency
        ("GBP", True, False),  # Common currency
        ("PLN", True, False),  # Common currency
        ("xxx", False, True),  # Invalid format but might warn
        ("US", False, False),  # Too short
        ("USDD", False, False),  # Too long
        ("usd", False, False),  # Lowercase
    ],
)
def test_currency_validation(valid_fare_xml, currency, should_pass, should_warn):
    """Test currency code validation."""
    xml = valid_fare_xml.replace('currency="USD"', f'currency="{currency}"')

    validator = FareValidator(xml)
    result = validator.validate()
    if should_pass:
        assert not any("currency" in error.lower() for error in result["errors"])
    else:
        assert any("currency" in error.lower() for error in result["errors"])


def test_missing_required_fields():
    """Test that missing required fields are detected."""
    incomplete_xml = """
    <FareResponse>
        <FareInfo>
            <FareReference>FARE2025001</FareReference>
        </FareInfo>
        <Pricing currency="USD">
            <BaseFare>500.00</BaseFare>
            <Taxes>75.00</Taxes>
            <Total>575.00</Total>
        </Pricing>
    </FareResponse>
    """

    validator = FareValidator(incomplete_xml)
    result = validator.validate()

    assert not result["is_valid"]
    assert any("missing required field" in error.lower() for error in result["errors"])


@pytest.mark.parametrize(
    "seats,should_pass,should_warn",
    [
        (5, True, False),  # Normal availability
        (0, True, True),  # No seats - warning
        (9, True, False),  # Maximum typical display
        (15, True, True),  # Unusual high number - warning
        (-1, False, False),  # Negative - error
    ],
)
def test_seat_availability_validation(valid_fare_xml, seats, should_pass, should_warn):
    """Test seat availability validation."""
    xml = valid_fare_xml.replace(
        "<SeatsAvailable>7</SeatsAvailable>", f"<SeatsAvailable>{seats}</SeatsAvailable>"
    )

    validator = FareValidator(xml)
    result = validator.validate()

    if should_pass:
        assert result["is_valid"]
        if should_warn:
            assert len(result["warnings"]) > 0
    else:
        assert not result["is_valid"]
        assert any(
            "negative" in error.lower() or "seats" in error.lower() for error in result["errors"]
        )

import pytest
import logging
logger = logging.getLogger(__name__)


@pytest.mark.parametrize("weight1,weight2,should_pass", [
    (20, 30, True),  # Total 50kg - under limit, should pass
    (40, 50, True),  # Total 90kg - under limit, should pass
    (50, 51, False),  # Total 101kg - over limit, should fail
    (60, 60, False),  # Total 120kg - over limit, should fail
])
def test_baggage_weight_limits(base_booking_xml, weight1, weight2, should_pass):
    """Test various baggage weight combinations."""
    second_passenger = f"""
        <Passenger id="P002" type="adult" title="Mrs">
            <Name>
                <First>Jane</First>
                <Last>Smith</Last>
            </Name>
            <DateOfBirth>1987-07-15</DateOfBirth>
            <Contact>
                <Email>jane@email.com</Email>
            </Contact>
            <Baggage>
                <CarryOn>1</CarryOn>
                <Checked>1</Checked>
                <Weight unit="kg">{weight2}</Weight>
            </Baggage>
            <Fare currency="GBP">899.00</Fare>
        </Passenger>
    """

    xml = base_booking_xml

    # Step 1: Replace first passenger's weight
    xml = xml.replace('<Weight unit="kg">20</Weight>',
                      f'<Weight unit="kg">{weight1}</Weight>')

    # Step 2: Add second passenger (only once!)
    xml = xml.replace('</Passengers>', second_passenger + '</Passengers>')

    # Step 3: Update pricing for 2 passengers
    xml = xml.replace('<SubTotal>899.00</SubTotal>', '<SubTotal>1798.00</SubTotal>')
    xml = xml.replace('<Tax>134.85</Tax>', '<Tax>269.70</Tax>')
    xml = xml.replace('<Total>1033.85</Total>', '<Total>2067.70</Total>')

    logger.info(xml)
    validator = BookingValidator(xml)
    result = validator.validate()

    logger.info(result)
    # Your assertions here
    assert result['is_valid'] == should_pass
    if not should_pass:
        assert len(result['errors']) > 0
        assert any('baggage' in error.lower() and 'exceeded' in error.lower() for error in result['errors'])

    # Your task:
    # 1. Modify base_booking_xml to have 2 passengers
    # 2. Set first passenger baggage weight to weight1
    # 3. Set second passenger baggage weight to weight2
    # 4. Validate
    # 5. Assert result['is_valid'] == should_pass

def test_valid_booking_passes(base_booking_xml ):
    """Test that a valid booking passes all validations."""

    xml = base_booking_xml


    validator = BookingValidator(xml)
    result = validator.validate()

    assert result['is_valid'] == True
    assert len(result['errors']) == 0


def test_connection_time_too_short_fails():
    validator = BookingValidator(invalid_xml)
    result = validator.validate()

    # Your assertions here
    assert result['is_valid'] == False
    assert len(result['errors']) > 0
    assert any('connection' in error.lower() for error in result['errors'])

    #logger.info(result['errors'])
def test_invalid_child_age():
    validator = BookingValidator(invalid_child_xml)
    result = validator.validate()

    # Your assertions here
    assert result['is_valid'] == False
    assert len(result['errors']) > 0
    assert any('child' in error.lower() and 'under' in error.lower() for error in result['errors'])
    assert any('P001' in error for error in result['errors'])


def test_invalid_baggage_weight():
    validator = BookingValidator(excessive_baggage_xml)
    result = validator.validate()


    logger.info(result)
    # Your assertions here
    assert result['is_valid'] == False
    assert len(result['errors']) > 0
    assert any('baggage' in error.lower() and 'exceeded' in error.lower() for error in result['errors'])
    #assert any('P001' in error for error in result['errors'])


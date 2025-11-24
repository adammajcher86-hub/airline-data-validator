import pytest


@pytest.fixture
def base_booking_xml():
    """Provide a valid baseline booking XML."""
    return """
    <BookingResponse>
        <BookingReference>REF2025001</BookingReference>
        <BookingDate>2025-01-15T10:30:00</BookingDate>
        <Agency code="AG001" name="Travel Solutions"/>
        <Itinerary>
            <Route>
                <Segment number="1" status="confirmed">
                    <Flight carrier="LO" number="281" class="Y">
                        <Departure>
                            <Airport>WAW</Airport>
                            <Terminal>1</Terminal>
                            <DateTime>2025-06-15T08:30:00</DateTime>
                        </Departure>
                        <Arrival>
                            <Airport>LHR</Airport>
                            <Terminal>5</Terminal>
                            <DateTime>2025-06-15T10:45:00</DateTime>
                        </Arrival>
                        <Duration>135</Duration>
                    </Flight>
                </Segment>
                <Segment number="2" status="confirmed">
                    <Flight carrier="BA" number="117" class="J">
                        <Departure>
                            <Airport>LHR</Airport>
                            <Terminal>5</Terminal>
                            <DateTime>2025-06-15T14:00:00</DateTime>
                        </Departure>
                        <Arrival>
                            <Airport>JFK</Airport>
                            <Terminal>7</Terminal>
                            <DateTime>2025-06-15T17:30:00</DateTime>
                        </Arrival>
                        <Duration>450</Duration>
                    </Flight>
                </Segment>
            </Route>
        </Itinerary>
        <Passengers>
            <Passenger id="P001" type="adult" title="Mr">
                <Name>
                    <First>John</First>
                    <Last>Smith</Last>
                </Name>
                <DateOfBirth>1985-03-20</DateOfBirth>
                <Contact>
                    <Email>john@email.com</Email>
                </Contact>
                <Baggage>
                    <CarryOn>1</CarryOn>
                    <Checked>1</Checked>
                    <Weight unit="kg">20</Weight>
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
    """


@pytest.fixture
def invalid_xml():
    """XML with connection time under 90 minutes (45 min connection)."""
    return """
    <BookingResponse>
        <BookingReference>REF2025001</BookingReference>
        <BookingDate>2025-01-15T10:30:00</BookingDate>
        <Agency code="AG001" name="Travel Solutions"/>
        <Itinerary>
            <Route>
                <Segment number="1" status="confirmed">
                    <Flight carrier="LO" number="281" class="Y">
                        <Departure>
                            <Airport>WAW</Airport>
                            <Terminal>1</Terminal>
                            <DateTime>2025-06-15T08:30:00</DateTime>
                        </Departure>
                        <Arrival>
                            <Airport>LHR</Airport>
                            <Terminal>5</Terminal>
                            <DateTime>2025-06-15T10:45:00</DateTime>
                        </Arrival>
                        <Duration>135</Duration>
                    </Flight>
                </Segment>
                <Segment number="2" status="confirmed">
                    <Flight carrier="BA" number="117" class="J">
                        <Departure>
                            <Airport>LHR</Airport>
                            <Terminal>5</Terminal>
                            <DateTime>2025-06-15T11:30:00</DateTime>
                        </Departure>
                        <Arrival>
                            <Airport>JFK</Airport>
                            <Terminal>7</Terminal>
                            <DateTime>2025-06-15T17:30:00</DateTime>
                        </Arrival>
                        <Duration>450</Duration>
                    </Flight>
                </Segment>
            </Route>
        </Itinerary>
        <Passengers>
            <Passenger id="P001" type="adult" title="Mr">
                <Name>
                    <First>John</First>
                    <Last>Smith</Last>
                </Name>
                <DateOfBirth>1985-03-20</DateOfBirth>
                <Contact>
                    <Email>john@email.com</Email>
                </Contact>
                <Baggage>
                    <CarryOn>1</CarryOn>
                    <Checked>1</Checked>
                    <Weight unit="kg">20</Weight>
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
    """


@pytest.fixture
def invalid_child_xml():
    """XML with child passenger who is 15 years old (too old)."""
    return """
    <BookingResponse>
        <BookingReference>REF2025001</BookingReference>
        <BookingDate>2025-01-15T10:30:00</BookingDate>
        <Agency code="AG001" name="Travel Solutions"/>
        <Itinerary>
            <Route>
                <Segment number="1" status="confirmed">
                    <Flight carrier="LO" number="281" class="Y">
                        <Departure>
                            <Airport>WAW</Airport>
                            <Terminal>1</Terminal>
                            <DateTime>2025-06-15T08:30:00</DateTime>
                        </Departure>
                        <Arrival>
                            <Airport>LHR</Airport>
                            <Terminal>5</Terminal>
                            <DateTime>2025-06-15T10:45:00</DateTime>
                        </Arrival>
                        <Duration>135</Duration>
                    </Flight>
                </Segment>
                <Segment number="2" status="confirmed">
                    <Flight carrier="BA" number="117" class="J">
                        <Departure>
                            <Airport>LHR</Airport>
                            <Terminal>5</Terminal>
                            <DateTime>2025-06-15T14:00:00</DateTime>
                        </Departure>
                        <Arrival>
                            <Airport>JFK</Airport>
                            <Terminal>7</Terminal>
                            <DateTime>2025-06-15T17:30:00</DateTime>
                        </Arrival>
                        <Duration>450</Duration>
                    </Flight>
                </Segment>
            </Route>
        </Itinerary>
        <Passengers>
            <Passenger id="P001" type="child" title="Miss">
                <Name>
                    <First>Emily</First>
                    <Last>Smith</Last>
                </Name>
                <DateOfBirth>2010-01-01</DateOfBirth>
                <Contact>
                    <Email>parent@email.com</Email>
                </Contact>
                <Baggage>
                    <CarryOn>1</CarryOn>
                    <Checked>1</Checked>
                    <Weight unit="kg">15</Weight>
                </Baggage>
                <Fare currency="GBP">450.00</Fare>
            </Passenger>
        </Passengers>
        <Pricing currency="GBP">
            <SubTotal>450.00</SubTotal>
            <Tax>67.50</Tax>
            <Total>517.50</Total>
        </Pricing>
    </BookingResponse>
    """


@pytest.fixture
def excessive_baggage_xml():
    """XML with total baggage weight of 115kg (exceeds 100kg limit)."""
    return """
    <BookingResponse>
        <BookingReference>REF2025001</BookingReference>
        <BookingDate>2025-01-15T10:30:00</BookingDate>
        <Agency code="AG001" name="Travel Solutions"/>
        <Itinerary>
            <Route>
                <Segment number="1" status="confirmed">
                    <Flight carrier="LO" number="281" class="Y">
                        <Departure>
                            <Airport>WAW</Airport>
                            <Terminal>1</Terminal>
                            <DateTime>2025-06-15T08:30:00</DateTime>
                        </Departure>
                        <Arrival>
                            <Airport>LHR</Airport>
                            <Terminal>5</Terminal>
                            <DateTime>2025-06-15T10:45:00</DateTime>
                        </Arrival>
                        <Duration>135</Duration>
                    </Flight>
                </Segment>
                <Segment number="2" status="confirmed">
                    <Flight carrier="BA" number="117" class="J">
                        <Departure>
                            <Airport>LHR</Airport>
                            <Terminal>5</Terminal>
                            <DateTime>2025-06-15T14:00:00</DateTime>
                        </Departure>
                        <Arrival>
                            <Airport>JFK</Airport>
                            <Terminal>7</Terminal>
                            <DateTime>2025-06-15T17:30:00</DateTime>
                        </Arrival>
                        <Duration>450</Duration>
                    </Flight>
                </Segment>
            </Route>
        </Itinerary>
        <Passengers>
            <Passenger id="P001" type="adult" title="Mr">
                <Name>
                    <First>John</First>
                    <Last>Smith</Last>
                </Name>
                <DateOfBirth>1985-03-20</DateOfBirth>
                <Contact>
                    <Email>john@email.com</Email>
                </Contact>
                <Baggage>
                    <CarryOn>1</CarryOn>
                    <Checked>2</Checked>
                    <Weight unit="kg">55</Weight>
                </Baggage>
                <Fare currency="GBP">899.00</Fare>
            </Passenger>
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
                    <Checked>2</Checked>
                    <Weight unit="kg">60</Weight>
                </Baggage>
                <Fare currency="GBP">899.00</Fare>
            </Passenger>
        </Passengers>
        <Pricing currency="GBP">
            <SubTotal>1798.00</SubTotal>
            <Tax>269.70</Tax>
            <Total>2067.70</Total>
        </Pricing>
    </BookingResponse>
    """


@pytest.fixture
def valid_fare_xml():
    """Provide valid fare data XML."""
    return """
    <FareResponse>
        <FareInfo>
            <FareReference>FARE2025001</FareReference>
            <FareBasis>YOWUS</FareBasis>
            <ValidatingCarrier>LO</ValidatingCarrier>
        </FareInfo>
        <Pricing currency="USD">
            <BaseFare>500.00</BaseFare>
            <Taxes>75.00</Taxes>
            <Total>575.00</Total>
        </Pricing>
        <FareRules>
            <FareRule type="ADVANCE_PURCHASE" code="AP14">
                <Days>14</Days>
                <Description>Must be purchased 14 days in advance</Description>
            </FareRule>
            <FareRule type="MIN_STAY" code="MS03">
                <Days>3</Days>
                <Description>Minimum stay 3 days</Description>
            </FareRule>
        </FareRules>
        <Availability>
            <SeatsAvailable>7</SeatsAvailable>
        </Availability>
    </FareResponse>
    """


@pytest.fixture
def invalid_fare_basis_xml():
    """Fare with invalid fare basis code."""
    return """
    <FareResponse>
        <FareInfo>
            <FareReference>FARE2025002</FareReference>
            <FareBasis>abc</FareBasis>
            <ValidatingCarrier>LO</ValidatingCarrier>
        </FareInfo>
        <Pricing currency="USD">
            <BaseFare>500.00</BaseFare>
            <Taxes>75.00</Taxes>
            <Total>575.00</Total>
        </Pricing>
        <Availability>
            <SeatsAvailable>5</SeatsAvailable>
        </Availability>
    </FareResponse>
    """


@pytest.fixture
def invalid_pricing_xml():
    """Fare with incorrect pricing calculation."""
    return """
    <FareResponse>
        <FareInfo>
            <FareReference>FARE2025003</FareReference>
            <FareBasis>YOWUS</FareBasis>
            <ValidatingCarrier>BA</ValidatingCarrier>
        </FareInfo>
        <Pricing currency="GBP">
            <BaseFare>500.00</BaseFare>
            <Taxes>75.00</Taxes>
            <Total>600.00</Total>
        </Pricing>
        <Availability>
            <SeatsAvailable>3</SeatsAvailable>
        </Availability>
    </FareResponse>
    """


@pytest.fixture
def invalid_currency_xml():
    """Fare with invalid currency code."""
    return """
    <FareResponse>
        <FareInfo>
            <FareReference>FARE2025004</FareReference>
            <FareBasis>YOWUS</FareBasis>
            <ValidatingCarrier>LO</ValidatingCarrier>
        </FareInfo>
        <Pricing currency="US">
            <BaseFare>500.00</BaseFare>
            <Taxes>75.00</Taxes>
            <Total>575.00</Total>
        </Pricing>
        <Availability>
            <SeatsAvailable>5</SeatsAvailable>
        </Availability>
    </FareResponse>
    """


@pytest.fixture
def negative_seats_xml():
    """Fare with negative seat availability."""
    return """
    <FareResponse>
        <FareInfo>
            <FareReference>FARE2025005</FareReference>
            <FareBasis>YOWUS</FareBasis>
            <ValidatingCarrier>LO</ValidatingCarrier>
        </FareInfo>
        <Pricing currency="USD">
            <BaseFare>500.00</BaseFare>
            <Taxes>75.00</Taxes>
            <Total>575.00</Total>
        </Pricing>
        <Availability>
            <SeatsAvailable>-5</SeatsAvailable>
        </Availability>
    </FareResponse>
    """

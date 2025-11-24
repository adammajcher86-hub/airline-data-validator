import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime


class BookingValidator:
    def __init__(self, xml_string):
        self.root = ET.fromstring(xml_string)
        self.errors = []
        self.warnings = []

    def validate(self):
        self._print_booking_summary()
        self._validate_connection_times()
        self._validate_passenger_ages()
        self._validate_baggage()
        self._validate_pricing()
        self._extract_special_requests()

        return {"is_valid": len(self.errors) == 0, "errors": self.errors, "warnings": self.warnings}

    def _print_booking_summary(self):
        """Extract and display booking summary."""

        bookingreference = self.root.find("BookingReference").text

        agency = self.root.find("Agency")
        agency_code = agency.get("code")
        agency_name = agency.get("name")

        passengers = self.root.findall(".//Passenger")
        total_passengers = len(passengers)

        # Count passenger types automatically
        passenger_types = [p.get("type") for p in passengers]
        type_counts = Counter(passenger_types)

        # Get total price
        total_price = self.root.find(".//Pricing/Total").text
        currency = self.root.find(".//Pricing").get("currency")

        print("Booking summary:")
        print(f"Booking reference: {bookingreference}")
        print(f"Agency: {agency_name} ({agency_code})")
        print(
            f"Passengers: {total_passengers} - "
            f"Adults: {type_counts['adult']}, Children: {type_counts['child']}"
        )
        print(f"Total price: {currency} {total_price}\n")

    def _validate_connection_times(self):
        """Check connection time is at least 90 minutes."""
        # Option 1: XPath with position index (1-based)
        arrival1_str = self.root.find(".//Segment[1]/Flight/Arrival/DateTime").text
        departure2_str = self.root.find(".//Segment[2]/Flight/Departure/DateTime").text

        # Option 2: Attribute filter
        # segment1 = self.root.find('.//Segment[@number="1"]')
        # arrival1 = segment1.find('.//Arrival/DateTime').text

        # Option 3: Python list indexing (0-based)
        # segments = self.root.findall('.//Segment')
        # arrival1 = segments[0].find('.//Arrival/DateTime').text
        # departure2 = segments[1].find('.//Departure/DateTime').text
        arrival1 = datetime.fromisoformat(arrival1_str)
        departure2 = datetime.fromisoformat(departure2_str)

        delta = departure2 - arrival1
        connection_minutes = delta.total_seconds() / 60
        if connection_minutes < 90:
            self.errors.append(
                f"Connection time too short: {connection_minutes:.0f} minutes "
                f"(minimum 90 minutes required)"
            )
        else:
            print("Time between arrival and departure is ok\n")

    def _validate_passenger_ages(self):
        """Validate passenger type matches their age."""
        departure1_str = self.root.find(".//Segment[1]/Flight/Departure/DateTime").text
        departure1 = datetime.fromisoformat(departure1_str)

        passengers = self.root.findall(".//Passenger")

        for passenger in passengers:
            passenger_id = passenger.get("id")
            passenger_type = passenger.get("type")

            date_of_birth_str = passenger.find("DateOfBirth").text
            date_of_birth = datetime.fromisoformat(date_of_birth_str)

            # Calculate age in years
            passenger_age_days = (departure1 - date_of_birth).days
            passenger_age_years = passenger_age_days / 365.25

            # Validate type matches age
            if passenger_type == "child":
                if passenger_age_years >= 12:
                    self.errors.append(
                        f"Passenger {passenger_id} is classified as child but is "
                        f"{passenger_age_years:.1f} years old (should be under 12)"
                    )
            elif passenger_type == "adult":
                if passenger_age_years < 12:
                    self.errors.append(
                        f"Passenger {passenger_id} is classified as adult but is "
                        f"{passenger_age_years:.1f} years old (should be 12 or older)"
                    )

    def _validate_baggage(self):
        """Check baggage limits."""
        passengers = self.root.findall(".//Passenger")

        weight_sum = 0
        checked_sum = 0

        for passenger in passengers:
            weight_sum += float(passenger.find("Baggage/Weight").text)
            checked_sum += float(passenger.find("Baggage/Checked").text)

        if weight_sum > 100:
            self.errors.append(
                f"Baggage limit exceeded: Total weight {weight_sum}kg "
                f"(limit 100kg), Total checked bags: {checked_sum}"
            )

    def _validate_pricing(self):
        """Validate price calculations."""
        passengers = self.root.findall(".//Passenger")
        fare_sum = 0

        for passenger in passengers:
            fare = passenger.find("Fare").text
            fare_sum += float(fare)

        subtotal = float(self.root.find(".//Pricing/SubTotal").text)
        tax = float(self.root.find(".//Pricing/Tax").text)
        total = float(self.root.find(".//Pricing/Total").text)

        # Check 1: SubTotal should equal sum of passenger fares
        if abs(fare_sum - subtotal) > 0.01:
            self.errors.append(
                f"SubTotal mismatch: sum of fares is {fare_sum}, " f"but SubTotal is {subtotal}"
            )

        # Check 2: Tax should be 15% of SubTotal
        calculated_tax = subtotal * 0.15
        if abs(calculated_tax - tax) > 0.01:
            self.errors.append(
                f"Tax mismatch: expected {calculated_tax:.2f} (15% of {subtotal}), "
                f"but got {tax}"
            )

        # Check 3: Total should equal SubTotal + Tax
        calculated_total = subtotal + tax
        if abs(calculated_total - total) > 0.01:
            self.errors.append(
                f"Total mismatch: expected {calculated_total:.2f} "
                f"(SubTotal + Tax), but got {total}"
            )

    def _extract_special_requests(self):
        """List and count special requests."""
        passengers = self.root.findall(".//Passenger")
        for passenger in passengers:
            special_request = passenger.find("SpecialRequests")
            if special_request is not None:
                requests = special_request.findall("Request")

                for request in requests:
                    code = request.get("code")  # Get the code attribute
                    description = request.text  # Get the text content
                    print(f"Code: {code}, Description: {description}")

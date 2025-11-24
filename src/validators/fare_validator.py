import re
import xml.etree.ElementTree as ET
from datetime import datetime


class FareValidator:
    """
    Validates airline fare data including fare rules, pricing, availability,
    and fare component structures.
    """

    def __init__(self, xml_string):
        self.root = ET.fromstring(xml_string)
        self.errors = []
        self.warnings = []

    def validate(self):
        """Run all fare validations."""
        self._validate_fare_structure()
        self._validate_fare_basis_codes()
        self._validate_pricing_components()
        self._validate_fare_rules()
        self._validate_availability()
        self._validate_currency()

        return {
            "is_valid": len(self.errors) == 0,
            "errors": self.errors,
            "warnings": self.warnings,
        }

    def _validate_fare_structure(self):
        """Validate basic fare structure."""
        fare_info = self.root.find("FareInfo")

        if fare_info is None:
            self.errors.append("Missing FareInfo element")
            return

        # Check required fields
        required_fields = ["FareReference", "FareBasis", "ValidatingCarrier"]
        for field in required_fields:
            if fare_info.find(field) is None:
                self.errors.append(f"Missing required field: {field}")

    def _validate_fare_basis_codes(self):
        """Validate fare basis code format."""
        fare_bases = self.root.findall(".//FareBasis")

        for fare_basis in fare_bases:
            code = fare_basis.text

            # Fare basis codes are typically 4-15 characters, alphanumeric
            if not re.match(r"^[A-Z0-9]{4,15}$", code):
                self.errors.append(
                    f"Invalid fare basis code format: {code} "
                    f"(must be 4-15 uppercase alphanumeric characters)"
                )

    def _validate_pricing_components(self):
        """Validate pricing breakdown."""
        pricing = self.root.find(".//Pricing")

        if pricing is None:
            self.errors.append("Missing Pricing element")
            return

        base_fare = pricing.find("BaseFare")
        taxes = pricing.find("Taxes")
        total = pricing.find("Total")

        if base_fare is None or taxes is None or total is None:
            self.errors.append("Missing pricing components (BaseFare, Taxes, or Total)")
            return

        # Extract values
        try:
            base_value = float(base_fare.text)
            taxes_value = float(taxes.text)
            total_value = float(total.text)

            # Validate calculation
            calculated_total = base_value + taxes_value
            if abs(calculated_total - total_value) > 0.01:
                self.errors.append(
                    f"Total mismatch: BaseFare ({base_value}) + Taxes ({taxes_value}) "
                    f"= {calculated_total}, but Total is {total_value}"
                )

            # Validate positive values
            if base_value < 0:
                self.errors.append(f"BaseFare cannot be negative: {base_value}")
            if taxes_value < 0:
                self.errors.append(f"Taxes cannot be negative: {taxes_value}")

        except ValueError as e:
            self.errors.append(f"Invalid numeric value in pricing: {e}")

    def _validate_fare_rules(self):
        """Validate fare rules and restrictions."""
        fare_rules = self.root.findall(".//FareRule")

        for rule in fare_rules:
            rule_type = rule.get("type")
            rule_code = rule.get("code")

            # Validate rule type
            valid_types = [
                "ADVANCE_PURCHASE",
                "MIN_STAY",
                "MAX_STAY",
                "PENALTIES",
                "BLACKOUT_DATES",
            ]
            if rule_type and rule_type not in valid_types:
                self.warnings.append(
                    f"Unknown fare rule type: {rule_type}. "
                    f"Expected one of: {', '.join(valid_types)}"
                )

            # Validate rule code format (typically 2-4 characters)
            if rule_code and not re.match(r"^[A-Z0-9]{2,4}$", rule_code):
                self.errors.append(
                    f"Invalid fare rule code format: {rule_code} "
                    f"(must be 2-4 uppercase alphanumeric characters)"
                )

            # Validate advance purchase days
            if rule_type == "ADVANCE_PURCHASE":
                days_elem = rule.find("Days")
                if days_elem is not None:
                    try:
                        days = int(days_elem.text)
                        if days < 0 or days > 365:
                            self.errors.append(
                                f"Invalid advance purchase days: {days} " f"(must be 0-365)"
                            )
                    except ValueError:
                        self.errors.append(f"Invalid days value: {days_elem.text}")

            # Validate stay duration
            if rule_type in ["MIN_STAY", "MAX_STAY"]:
                days_elem = rule.find("Days")
                if days_elem is not None:
                    try:
                        days = int(days_elem.text)
                        if days < 0 or days > 365:
                            self.errors.append(f"Invalid {rule_type} days: {days} (must be 0-365)")
                    except ValueError:
                        self.errors.append(f"Invalid days value: {days_elem.text}")

    def _validate_availability(self):
        """Validate seat availability."""
        availability = self.root.find(".//Availability")

        if availability is not None:
            seats = availability.find("SeatsAvailable")
            if seats is not None:
                try:
                    seat_count = int(seats.text)
                    if seat_count < 0:
                        self.errors.append(f"Seats available cannot be negative: {seat_count}")
                    elif seat_count == 0:
                        self.warnings.append("No seats available for this fare")
                    elif seat_count > 9:
                        # Airlines typically show 9+ as "9"
                        self.warnings.append(
                            f"Unusual seat count: {seat_count} "
                            f"(typically capped at 9 for display)"
                        )
                except ValueError:
                    self.errors.append(f"Invalid seat count: {seats.text}")

    def _validate_currency(self):
        """Validate currency codes."""
        currency_elements = self.root.findall(".//*[@currency]")

        for elem in currency_elements:
            currency = elem.get("currency")

            # ISO 4217 currency codes are 3 uppercase letters
            if not re.match(r"^[A-Z]{3}$", currency):
                self.errors.append(
                    f"Invalid currency code: {currency} " f"(must be 3 uppercase letters, ISO 4217)"
                )

            # Check common currencies
            common_currencies = [
                "USD",
                "EUR",
                "GBP",
                "JPY",
                "PLN",
                "CAD",
                "AUD",
                "CHF",
            ]
            if currency not in common_currencies:
                self.warnings.append(
                    f"Uncommon currency code: {currency}. " f"Verify this is correct."
                )

    def _validate_validity_dates(self):
        """Validate fare validity dates."""
        valid_from = self.root.find(".//ValidFrom")
        valid_to = self.root.find(".//ValidTo")

        if valid_from is not None and valid_to is not None:
            try:
                from_date = datetime.fromisoformat(valid_from.text)
                to_date = datetime.fromisoformat(valid_to.text)

                if to_date <= from_date:
                    self.errors.append(
                        f"ValidTo date ({to_date}) must be after ValidFrom date ({from_date})"
                    )

                # Check if fare has expired
                if to_date < datetime.now():
                    self.warnings.append(f"Fare has expired (ValidTo: {to_date.date()})")

            except ValueError as e:
                self.errors.append(f"Invalid date format: {e}")

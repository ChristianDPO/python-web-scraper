import re

CNPJ_PATTERN = r"^\d{14}$"
DIGITS_ONLY_PATTERN = r"\d"


class ValidationHelper(object):
    @staticmethod
    def validate_string(value, field_name, validation_pattern):
        """
        Validates if a string matches the given regex pattern.

        :param str value: The string to validate.
        :param str field_name: Name of the field being validated.
        :param str validation_pattern: Regex pattern that the entire string must match.
        :return: The same value if valid.
        :rtype: str
        :raises ValueError: If the string does not match the pattern.
        """
        if not isinstance(value, str):
            raise ValueError("validate_string expects a string value.")

        if not re.fullmatch(validation_pattern, value):
            raise ValueError(
                f"Invalid format for {field_name}"
            )
        
        return value

    @staticmethod
    def sanitize_string(value, allowed_pattern):
        """
        Remove all characters from a string that don't match the given regex pattern.

        :param value: The string to sanitize.
        :param allowed_pattern: A regex pattern that the string should follow.
        :return: Sanitized string containing only allowed characters.
        :rtype: str
        """
        if not isinstance(value, str):
            raise ValueError("sanitize_string expects a string value.")

        # Remove disallowed characters by replacing them with an empty string
        sanitized = "".join(re.findall(allowed_pattern, value))
        return sanitized

import re
from email_validator import validate_email, EmailNotValidError
from rich.prompt import Prompt
from rich.console import Console

console = Console()


def check_date_format(date_str):
    """Validate date format: YYYY-MM-DD HH:MM:SS."""
    pattern = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"
    return bool(re.match(pattern, date_str))


def validate_email_format(email):
    """Validate email format."""
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False


def validate_phone_number(phone):
    """
    Validate phone number.
    Accepts:
    - Numbers with optional "+" for country code.
    - At least 10 digits.
    """
    pattern = r"^\+?\d{9,15}$"  # Minimum 9 digits for flexibility
    return bool(re.match(pattern, str(phone)))


def clean_string(value):
    """Trim spaces and normalize string input."""
    if isinstance(value, str):
        return value.strip()
    return value


def validate_positive_float(value):
    """Validate if the value is a positive float or integer."""
    try:
        value = float(value)
        return value >= 0
    except ValueError:
        return False


def validate_non_empty_string(value):
    """Ensure the string is non-empty after cleaning."""
    value = clean_string(value)
    return bool(value)


def ask_boolean(prompt: str) -> bool:
    """
    Affiche une question booléenne et retourne True/False.
    :param prompt: Question posée à l'utilisateur.
    :return: Booléen basé sur la réponse ('o' pour Oui, 'n' pour Non).
    """
    response = Prompt.ask(
        f"[bold yellow]?[/bold yellow] {prompt} [dim](o/n)[/dim]",
        choices=["o", "n"],
        default="n"
    )
    return response == "o"

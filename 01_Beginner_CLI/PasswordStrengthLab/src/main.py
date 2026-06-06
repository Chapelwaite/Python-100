# pathlib helps us work with file/folder paths safely
from pathlib import Path

# getpass hides the password while the user types it
from getpass import getpass

# datetime is used for saving scan date/time in history
from datetime import datetime


# This gets the main project folder:
# PasswordStrengthLab/
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Path to the file where common weak passwords are stored
COMMON_PASSWORDS_FILE = PROJECT_ROOT / "data" / "common_passwords.txt"

# Path to the history file where scan results will be saved
# IMPORTANT: We do NOT save the actual password
HISTORY_FILE = PROJECT_ROOT / "history" / "scan_history.txt"


def load_common_passwords():
    """
    Loads common passwords from data/common_passwords.txt.
    Returns them as a set for fast checking.
    """

    # If the file does not exist, return empty set instead of crashing
    if not COMMON_PASSWORDS_FILE.exists():
        return set()

    # Read every line, remove spaces/newlines, convert to lowercase
    with open(COMMON_PASSWORDS_FILE, "r", encoding="utf-8") as file:
        return {line.strip().lower() for line in file if line.strip()}


def has_lowercase(password):
    """Checks if password has at least one lowercase letter."""
    return any(char.islower() for char in password)


def has_uppercase(password):
    """Checks if password has at least one uppercase letter."""
    return any(char.isupper() for char in password)


def has_number(password):
    """Checks if password has at least one number."""
    return any(char.isdigit() for char in password)


def has_symbol(password):
    """
    Checks if password has at least one symbol.
    Example: ! @ # $ %
    """
    return any(not char.isalnum() and not char.isspace() for char in password)


def has_space(password):
    """
    Checks if password contains a space.
    Spaces can be useful for passphrases like:
    correct horse battery moon
    """
    return any(char.isspace() for char in password)


def has_repeated_characters(password):
    """
    Detects repeated characters.
    Example:
    aaaa
    1111
    xxxx
    """

    password = password.lower()

    # Check every unique character in password
    for char in set(password):
        # If same character appears 4 times in a row, it is weak
        if char * 4 in password:
            return True

    return False


def has_number_sequence(password):
    """
    Detects number sequences.
    Example:
    1234
    5678
    9876
    """

    sequences = [
        "1234",
        "2345",
        "3456",
        "4567",
        "5678",
        "6789",
        "9876",
        "8765",
        "7654",
        "6543",
        "5432",
        "4321",
    ]

    return any(sequence in password for sequence in sequences)


def has_keyboard_pattern(password):
    """
    Detects common keyboard/common word patterns.
    Example:
    qwerty
    admin
    login
    password
    """

    password = password.lower()

    patterns = [
        "qwerty",
        "asdf",
        "zxcv",
        "qaz",
        "wsx",
        "admin",
        "login",
        "user",
        "password",
    ]

    return any(pattern in password for pattern in patterns)


def has_common_year(password):
    """
    Detects simple years.
    Many people use years in passwords, for example:
    Levani2024
    admin2025
    """

    years = ["2020", "2021", "2022", "2023", "2024", "2025", "2026"]

    return any(year in password for year in years)


def get_strength_label(score):
    """
    Converts numeric score into text strength label.
    """

    if score <= 20:
        return "Very Weak"
    elif score <= 40:
        return "Weak"
    elif score <= 60:
        return "Medium"
    elif score <= 80:
        return "Strong"
    else:
        return "Very Strong"


def analyze_password(password, nickname=""):
    """
    Main function that checks the password and returns full result:
    score, strength, checks, problems, and tips.
    """

    # Load common passwords from file
    common_passwords = load_common_passwords()

    # Starting score
    score = 0

    # Problems found in password
    problems = []

    # Tips for improving password
    tips = []

    # Password length
    length = len(password)

    # Basic character checks
    lowercase = has_lowercase(password)
    uppercase = has_uppercase(password)
    number = has_number(password)
    symbol = has_symbol(password)
    space = has_space(password)

    # Weak pattern checks
    repeated = has_repeated_characters(password)
    number_sequence = has_number_sequence(password)
    keyboard_pattern = has_keyboard_pattern(password)
    common_year = has_common_year(password)

    # Check if password is exactly inside common password list
    is_common_password = password.lower() in common_passwords

    # Check if password contains user's name/nickname
    contains_nickname = nickname and nickname.lower() in password.lower()

    # Give points for password length
    if length >= 20:
        score += 40
    elif length >= 16:
        score += 35
    elif length >= 12:
        score += 25
    elif length >= 8:
        score += 15
    else:
        problems.append("Password is too short")
        tips.append("Use at least 12 characters")

    # Give points for lowercase letters
    if lowercase:
        score += 8
    else:
        problems.append("Missing lowercase letters")
        tips.append("Add lowercase letters like a, b, c")

    # Give points for uppercase letters
    if uppercase:
        score += 8
    else:
        problems.append("Missing uppercase letters")
        tips.append("Add uppercase letters like A, B, C")

    # Give points for numbers
    if number:
        score += 8
    else:
        problems.append("Missing numbers")
        tips.append("Add numbers like 1, 2, 3")

    # Give points for symbols
    if symbol:
        score += 10
    else:
        problems.append("Missing symbols")
        tips.append("Add symbols like !, @, #, $")

    # Give small bonus for spaces because passphrases can be strong
    if space:
        score += 5

    # Bonus for long password that is not common
    if length >= 16 and not is_common_password:
        score += 10

    # Big penalty for common password
    if is_common_password:
        score -= 50
        problems.append("Password is in the common passwords list")
        tips.append("Avoid common passwords like password, 123456, qwerty")

    # Penalty for repeated characters
    if repeated:
        score -= 20
        problems.append("Contains repeated characters")
        tips.append("Avoid repeated characters like aaaa or 1111")

    # Penalty for number sequence
    if number_sequence:
        score -= 20
        problems.append("Contains a number sequence")
        tips.append("Avoid number sequences like 1234 or 9876")

    # Penalty for keyboard/common patterns
    if keyboard_pattern:
        score -= 25
        problems.append("Contains a keyboard/common pattern")
        tips.append("Avoid patterns like qwerty, admin, login, password")

    # Penalty for common years
    if common_year:
        score -= 10
        problems.append("Contains a common year")
        tips.append("Avoid using simple years like 2024 or 2025")

    # Penalty for personal information
    if contains_nickname:
        score -= 25
        problems.append("Contains your nickname/name")
        tips.append("Do not use your name, nickname, or personal info")

    # Make sure score always stays between 0 and 100
    score = max(0, min(score, 100))

    # Convert score to label
    strength = get_strength_label(score)

    # Return all information as dictionary
    return {
        "score": score,
        "strength": strength,
        "length": length,
        "lowercase": lowercase,
        "uppercase": uppercase,
        "number": number,
        "symbol": symbol,
        "space": space,
        "problems": problems,

        # dict.fromkeys removes duplicate tips
        "tips": list(dict.fromkeys(tips)),
    }


def yes_no(value):
    """
    Converts True/False to yes/no for nicer output.
    """

    return "yes" if value else "no"


def save_history(result):
    """
    Saves scan result to history/scan_history.txt.
    The actual password is NOT saved.
    """

    # Create history folder if it does not exist
    HISTORY_FILE.parent.mkdir(exist_ok=True)

    # Append scan result to history file
    with open(HISTORY_FILE, "a", encoding="utf-8") as file:
        file.write("================================\n")
        file.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write(f"Score: {result['score']}/100\n")
        file.write(f"Strength: {result['strength']}\n")

        if result["problems"]:
            file.write("Problems:\n")
            for problem in result["problems"]:
                file.write(f"- {problem}\n")
        else:
            file.write("Problems: None\n")

        file.write("Password saved: NO\n")
        file.write("================================\n\n")


def print_result(result):
    """
    Prints final result in terminal.
    """

    print("\n================================")
    print(" PASSWORD STRENGTH LAB")
    print("================================")

    print(f"\nScore: {result['score']}/100")
    print(f"Strength: {result['strength']}")

    print("\nChecks:")
    print(f"- Length: {result['length']} characters")
    print(f"- Lowercase: {yes_no(result['lowercase'])}")
    print(f"- Uppercase: {yes_no(result['uppercase'])}")
    print(f"- Numbers: {yes_no(result['number'])}")
    print(f"- Symbols: {yes_no(result['symbol'])}")
    print(f"- Spaces: {yes_no(result['space'])}")

    print("\nProblems:")
    if result["problems"]:
        for problem in result["problems"]:
            print(f"- {problem}")
    else:
        print("- No major problems found")

    print("\nTips:")
    if result["tips"]:
        for tip in result["tips"]:
            print(f"- {tip}")
    else:
        print("- Great password. Keep it unique and do not reuse it.")

    print("\nNote: This app does not save your password.")
    print("================================")


def main():
    """
    Program starts here.
    """

    print("================================")
    print(" PASSWORD STRENGTH LAB")
    print("================================")
    print("A Python cybersecurity project for checking password strength.\n")

    # Optional nickname check
    nickname = input("Enter your name/nickname or press Enter to skip: ").strip()

    # Ask user for password
    # getpass hides input in terminal
    try:
        password = getpass("Enter password to check: ")
    except Exception:
        # Fallback if getpass does not work in some terminals
        password = input("Enter password to check: ")

    # If user enters nothing, stop program
    if not password:
        print("\nYou did not enter a password.")
        return

    # Analyze password
    result = analyze_password(password, nickname)

    # Print result in terminal
    print_result(result)

    # Save result safely without saving password
    save_history(result)

    print("\nScan saved to history/scan_history.txt")
    print("Password itself was NOT saved.")


# This makes sure main() runs only when this file is executed directly
if __name__ == "__main__":
    main()
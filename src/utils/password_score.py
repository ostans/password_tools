import string


common_passwords = [
    "123456",
    "password",
    "123456789",
    "12345678",
    "12345",
    "111111",
    "1234567",
    "admin",
    "qwerty",
    "P@ssw0rd",
    "zxcvbnm",
]
sp = [
    ("a", "@"),
    ("s", "$"),
    ("o", "0"),
    ("i", "!"),
    ("e", "3"),
    ("l", "1"),
    ("t", "7"),
    ("b", "8"),
    ("g", "9"),
    ("z", "2"),
]


def password_score(username: str, password: str):
    score = 0
    msg = "\n🏁 Filter checks:\n"

    # 1. Length check
    if len(password) < 8:
        msg += "❌ Password is shorter than 8 characters.\n"
    else:
        msg += "✅ Password length is sufficient.\n"
        score += 1

    # 2. Contains at least one English letter
    has_letter = False
    for char in password.lower():
        if char in string.ascii_lowercase:
            has_letter = True
    if has_letter == False:
        msg += "❌ Password does not contain any English letters.\n"
    else:
        msg += "✅ Contains at least one letter.\n"
        score += 1

    # 3. Contains at least one special character
    has_special_char = False
    for char in password:
        if char in string.punctuation:
            has_special_char = True
    if has_special_char == False:
        msg += "❌ Password does not contain any special characters.\n"
    else:
        msg += "✅ Contains at least one special character.\n"
        score += 1

    # 4. Contains at least one uppercase letter
    has_uppercase = False
    for char in password:
        if char in string.ascii_uppercase:
            has_uppercase = True
    if has_uppercase == False:
        msg += "❌ Password does not contain any uppercase letters.\n"
    else:
        msg += "✅ Password contains uppercase letters.\n"
        score += 1

    # 5. Does not contain the username
    if username.lower() in password.lower():
        msg += "❌ Password contains the username.\n"
    else:
        msg += "✅ Password is not identical to the username.\n"
        score += 1

    # 6. Not a swapcase version of the username
    if password.lower() == username.swapcase():
        msg += "❌ Password is a swapcase version of the username.\n"
    else:
        msg += "✅ Password is not a swapcase version of the username.\n"
        score += 1

    # 7. Not a special-character version of the username
    copy_password = password
    for old, new in sp:
        copy_password = copy_password.lower().replace(new, old)

    if username.lower() in copy_password.lower():
        msg += "❌ Is a special-character version of the username.\n"
    else:
        msg += "✅ Not a special-character version of the username.\n"
        score += 1

    # 8. Not a common password
    for common_password in common_passwords:
        if password.lower() == common_password.lower():
            msg += "❌ Password is one of the most common passwords.\n"
            break
    else:
        msg += "✅ Not a common password.\n"
        score += 1

    return score, msg


# while True:
#     user_name = input("Please enter your username:\n")
#     if user_name == "":
#         print("Username cannot be empty. Please try again.")
#     else:
#         break


# while True:
#     birth_year = input("Please enter your birth year:\n")
#     if not birth_year.isdigit() or len(birth_year) != 4:
#         print("Birth year must be a 4-digit number. Please try again.")
#     else:
#         break


# while True:
#     password = input("Please enter your password:\n")
#     if password == "":
#         print("Password cannot be empty. Please try again.")
#     else:
#         break

# score, message = password_score(user_name, password)
# print(
#     message,
#     f"\n🔐 Final Score: {score} out of 8",
# )
# print(
#     f"🔒️ Security Level: {"Very Weak" if score <= 3 else "Weak" if score <= 5 else "Medium" if score <= 7 else "Strong" }\n"
# )


def main():
    user_name = input("Please enter your username:\n")
    password = input("Please enter your password:\n")

    score, message = password_score(user_name, password)
    print(
        message,
        f"\n🔐 Final Score: {score} out of 8",
    )
    print(
        f"🔒️ Security Level: {'Very Weak' if score <= 3 else 'Weak' if score <= 5 else 'Medium' if score <= 7 else 'Strong' }\n"
    )


if __name__ == "__main__":
    main()

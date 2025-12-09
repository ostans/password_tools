import string
from typing import Optional, Tuple, List, Dict, Any

# Common passwords (use a set for faster membership tests)
common_passwords = {
    "123456",
    "password",
    "123456789",
    "12345678",
    "12345",
    "111111",
    "1234567",
    "admin",
    "qwerty",
    "p@ssw0rd",
    "zxcvbnm",
    "P@ssw0rd123",
}

# Leet substitutions: (plain_char, leet_char)
substitutions = [
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


def is_leet_of_username(username: Optional[str], password: Optional[str]) -> bool:
    """
    Convert common leet characters in password back to plain letters
    and check if the username appears in that transformed password.
    """
    cp = (password or "").lower()
    for plain, leet in substitutions:
        cp = cp.replace(leet.lower(), plain.lower())
    return bool(username) and username.lower() in cp


def build_checks(min_length: int = 8) -> List[Dict[str, Any]]:
    """
    Return a list of check definitions. Each check is a dict with:
      - id: a short identifier
      - weight: numeric weight for scoring
      - check: function(username, password) -> bool
      - pass: message template when check passes
      - fail: message template when check fails
      - context (optional): extra fields for message formatting
    """
    return [
        {
            "id": "length",
            "weight": 1,
            "check": lambda u, p: len(p or "") >= min_length,  # type: ignore
            "pass": "✅ Password length is at least {min_length} characters.",
            "fail": "❌ Password is shorter than {min_length} characters.",
            "context": {"min_length": min_length},
        },
        {
            "id": "has_letter",
            "weight": 1,
            "check": lambda u, p: any(c in string.ascii_lowercase for c in (p or "").lower()),  # type: ignore
            "pass": "✅ Contains at least one English letter.",
            "fail": "❌ Does not contain any English letters.",
        },
        {
            "id": "has_special",
            "weight": 1,
            "check": lambda u, p: any(c in string.punctuation for c in (p or "")),  # type: ignore
            "pass": "✅ Contains at least one special character.",
            "fail": "❌ Does not contain any special characters.",
        },
        {
            "id": "has_upper",
            "weight": 1,
            "check": lambda u, p: any(c in string.ascii_uppercase for c in (p or "")),  # type: ignore
            "pass": "✅ Contains at least one uppercase letter.",
            "fail": "❌ Does not contain any uppercase letters.",
        },
        {
            "id": "not_contains_username",
            "weight": 1,
            "check": lambda u, p: not u or (u.lower() not in (p or "").lower()),  # type: ignore
            "pass": "✅ Password does not contain the username.",
            "fail": "❌ Password contains the username: '{username}'.",
        },
        {
            "id": "not_swapcase",
            "weight": 1,
            "check": lambda u, p: not u or p != (u.swapcase() if u else ""),  # type: ignore
            "pass": "✅ Password is not a swapcase version of the username.",
            "fail": "❌ Password equals the username's swapcase form.",
        },
        {
            "id": "not_leet_of_username",
            "weight": 1,
            "check": lambda u, p: not is_leet_of_username(u, p),  # type: ignore
            "pass": "✅ Password is not a leet (special-character) version of the username.",
            "fail": "❌ Password is a leet-like version of the username: '{username}'.",
        },
        {
            "id": "not_common",
            "weight": 1,
            "check": lambda u, p: (p or "") not in common_passwords,  # type: ignore
            "pass": "✅ Password is not in the list of common passwords.",
            "fail": "❌ Password is one of the most common passwords.",
        },
    ]


def password_score(
    username: str, password: str, min_length: int = 8
) -> Tuple[int, int, int, str]:
    """
    Evaluate password against all checks.
    Returns: (score, total_weight, percent, messages_string)
    """
    checks = build_checks(min_length)
    total_weight = sum(c["weight"] for c in checks)
    score = 0
    messages: List[str] = []

    for c in checks:
        ok = bool(c["check"](username, password))
        template = c["pass"] if ok else c["fail"]
        # base format context includes username/password and any check-specific context
        context: Dict[str, Any] = {
            "username": username or "",
            "password": password or "",
        }
        context.update(c.get("context", {}))
        messages.append(template.format(**context))
        if ok:
            score += c["weight"]

    percent = int(score / total_weight * 100) if total_weight else 0
    header = f"\n🏁 Filter checks (score: {score}/{total_weight} = {percent}%):\n"
    return score, total_weight, percent, header + "\n".join(messages)


def main():
    # Example usage
    username = "testuser"
    password = "P@ssw0rd123"
    score, total, percent, msg = password_score(username, password)
    print(msg)
    print(f"Final Score: {score}/{total} ({percent}%)")


if __name__ == "__main__":
    main()

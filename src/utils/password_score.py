import string
from collections import defaultdict
from typing import List, Dict, Any

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


def is_leet_of_username(username: str, password: str) -> bool:
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
            "severity": "high",
            "check": lambda u, p: len(p or "") >= min_length,  # type: ignore
            "pass": "✅ Password length is at least {min_length} characters.",
            "fail": "❌ Password is shorter than {min_length} characters.",
            "tip": "Use at least {min_length} characters; consider using 12+ for better security.",
            "context": {"min_length": min_length},
        },
        {
            "id": "has_letter",
            "weight": 1,
            "severity": "medium",
            "check": lambda u, p: any(c in string.ascii_lowercase for c in (p or "").lower()),  # type: ignore
            "pass": "✅ Contains at least one English letter.",
            "fail": "❌ Does not contain any English letters.",
            "tip": "Include letters (a-z). Combine lower and upper case letters.",
        },
        {
            "id": "has_special",
            "weight": 1,
            "severity": "medium",
            "check": lambda u, p: any(c in string.punctuation for c in (p or "")),  # type: ignore
            "pass": "✅ Contains at least one special character.",
            "fail": "❌ Does not contain any special characters.",
            "tip": "Add symbols like ! @ # $ % ^ & * ( ) to increase entropy.",
        },
        {
            "id": "has_upper",
            "weight": 1,
            "severity": "low",
            "check": lambda u, p: any(c in string.ascii_uppercase for c in (p or "")),  # type: ignore
            "pass": "✅ Contains at least one uppercase letter.",
            "fail": "❌ Does not contain any uppercase letters.",
            "tip": "Include at least one uppercase letter (A-Z).",
        },
        {
            "id": "not_contains_username",
            "weight": 1,
            "severity": "high",
            "check": lambda u, p: not u or (u.lower() not in (p or "").lower()),  # type: ignore
            "pass": "✅ Password does not contain the username.",
            "fail": "❌ Password contains the username: '{username}'.",
            "tip": "Avoid using your username or parts of it. Use unrelated words or a passphrase.",
        },
        {
            "id": "not_swapcase",
            "weight": 1,
            "severity": "low",
            "check": lambda u, p: not u or p != (u.swapcase() if u is not None else ""),  # type: ignore
            "pass": "✅ Password is not a swapcase version of the username.",
            "fail": "❌ Password equals the username's swapcase form.",
            "tip": "Don't use simple case transformations of your username; pick a different secret.",
        },
        {
            "id": "not_leet_of_username",
            "weight": 1,
            "severity": "medium",
            "check": lambda u, p: not is_leet_of_username(u, p),  # type: ignore
            "pass": "✅ Password is not a leet (special-character) version of the username.",
            "fail": "❌ Password is a leet-like version of the username: '{username}'.",
            "tip": "Avoid common character substitutions of your username (e.g. '@'->'a', '0'->'o'). Use unrelated phrases.",
        },
        {
            "id": "not_common",
            "weight": 1,
            "severity": "high",
            "check": lambda u, p: (p or "").lower() not in common_passwords,  # type: ignore
            "pass": "✅ Password is not in the list of common passwords.",
            "fail": "❌ Password is one of the most common passwords.",
            "tip": "Use a unique, uncommon password or a long passphrase; consider a password manager.",
        },
    ]


# Safe formatter: missing keys return empty string instead of KeyError
class SafeDict(dict[str, str]):
    def __missing__(self, key: str) -> str:
        return ""


def password_score(username: str, password: str, min_length: int = 8):
    """
    Evaluate password against all checks.
    Returns: (score, total_weight, percent, messages_string)
    The returned messages_string includes:
      - per-check pass/fail messages
      - a separate "Recommended fixes" section with tips grouped by severity
    """
    checks = build_checks(min_length)
    total_weight = sum(c["weight"] for c in checks)
    score = 0
    messages: List[str] = []

    # Collect failed tips grouped by severity
    recommended: Dict[str, List[str]] = defaultdict(list)

    for c in checks:
        ok = bool(c["check"](username, password))
        template = c["pass"] if ok else c["fail"]
        context = {"username": username or "", "password": password or ""}
        context.update(c.get("context", {}))
        messages.append(template.format_map(SafeDict(context)))
        if not ok:
            tip = c.get("tip")
            severity = c.get("severity", "low")
            if tip:
                recommended[severity].append(tip.format_map(SafeDict(context)))
        else:
            score += c["weight"]

    percent = int(score / total_weight * 100) if total_weight else 0
    header = f"\n🏁 Filter checks (score: {score}/{total_weight} = {percent}%):\n"
    body = "\n".join(messages)

    # Build Recommended fixes section, ordered by severity
    severity_order = ["high", "medium", "low"]
    fixes_lines: List[str] = []
    if any(recommended.values()):
        fixes_lines.append("\n \n🔧 Recommended fixes:")
        for sev in severity_order:
            tips = recommended.get(sev, [])
            if not tips:
                continue
            # human-friendly severity header
            sev_label = sev.capitalize()
            fixes_lines.append(f"\n{sev_label} priority:")
            # Deduplicate tips while preserving order
            seen: set[str] = set()
            for t in tips:
                if t not in seen:
                    fixes_lines.append(" - " + t)
                    seen.add(t)

    full_message = header + body + ("\n".join(fixes_lines) if fixes_lines else "")
    return score, total_weight, percent, full_message


def main():
    # Example usage
    username = "testuser"
    password = "P@ssw0rd123"
    score, total, percent, msg = password_score(username, password)
    print(msg)
    print(f"Final Score: {score}/{total} ({percent}%)")


if __name__ == "__main__":
    main()

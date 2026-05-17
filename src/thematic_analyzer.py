import re


# ------------------------------------------------------------
# BUSINESS THEME MAPPING
# ------------------------------------------------------------

def map_text_to_business_theme(cleaned_text):
    """
    Categorizes review text into business themes
    using regex keyword rules.
    """

    if not isinstance(cleaned_text, str) or cleaned_text.strip() == "":
        return "General Feedback"

    theme_rules = {

        "Account Access Issues":
            r"\b(login|log|password|otp|register|signup|fingerprint|activation|unable|pin|lock)\b",

        "Transaction Performance":
            r"\b(transfer|payment|send|receive|pending|fail|deduct|transaction|slow|network|error|crash|timeout)\b",

        "UI & Design":
            r"\b(interface|ui|ux|design|layout|beautiful|color|clunky|load|screen|theme|dark)\b",

        "Customer Support":
            r"\b(service|branch|help|support|call|respond|agent|customer|contact|ticket|ignore)\b"
    }

    for theme, pattern in theme_rules.items():

        if re.search(pattern, cleaned_text):
            return theme

    return "General Feedback"
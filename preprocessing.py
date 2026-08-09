import re
import pandas as pd

# ==========================================================
# FIX ENCODING
# ==========================================================

def fix_encoding(text):
    if not (pd.notna(text) and isinstance(text, str)):
        return text

    replacements = {
        'â€“': '-',
        'â€”': '-',
        'â€™': "'",
        'â€œ': '"',
        'â€\x9d': '"',
        'Â': '',
        'â€¦': '...',
        'â€˜': "'",
        'â€‹': '',
        'Ã´': 'ô',
        'Ã‰': 'É',
        'Ãƒ‰': 'É',
        'Ãƒ©': 'é',
        'Ã©': 'é'
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text


def remove_bad_unicode(text):
    if pd.notna(text) and isinstance(text, str):
        return re.sub(r"[ãâÂ]+", " ", text)
    return text


# ==========================================================
# REGEX
# ==========================================================

_ADS = re.compile(
    r"gpt-inline\d*|googletag|pubads|passback|inline\d*"
    r"|adsbygoogle|googlesyndication|googlefc|google_tag"
    r"|dataLayer|pagead|advertisem\w*"
    r"|\b(let|window|function|defineslot|addservice"
    r"|enableservices|collapseemptydivs|enablesinglerequest"
    r"|desktop|align|tirto)\b"
    r"|push\s*\(",
    re.IGNORECASE,
)

_FACTCHECK = re.compile(
    r"\b("
    r"benarkah"
    r"|cek fakta"
    r"|periksa fakta"
    r"|faktanya"
    r"|fakta"
    r"|hoaks"
    r"|salah"
    r"|keliru"
    r"|tidak benar"
    r"|sebagian benar"
    r"|disinformasi"
    r"|misinformasi"
    r"|narasi yang beredar"
    r"|narasi"
    r"|diklaim"
    r"|klaim"
    r"|beredar"
    r"|unggahan"
    r"|arsip"
    r"|akun facebook"
    r"|akun tiktok"
    r"|video viral"
    r"|tautan di bio"
    r"|link di bio"
    r")\b",
    re.IGNORECASE,
)


# ==========================================================
# CLEANING FUNCTIONS
# ==========================================================

def remove_ads_script(text):
    if pd.notna(text) and isinstance(text, str):
        return _ADS.sub(" ", text)
    return text


def remove_factcheck_words(text):
    if pd.notna(text) and isinstance(text, str):
        return _FACTCHECK.sub(" ", text)
    return text


def remove_url(text):
    if pd.notna(text) and isinstance(text, str):
        return re.sub(r"https?://\S+|www\.\S+", "", text)
    return text


def remove_noise(text):
    if not (pd.notna(text) and isinstance(text, str)):
        return text

    patterns = [
        r"gpt-inline\d*",
        r"gpt",
        r"googletag",
        r"pubads",
        r"passback",
        r"inline\d*",
        r"cmd",
        r"adsbygoogle",
        r"googlesyndication",
        r"googlefc",
        r"google_tag",
        r"dataLayer",
        r"push\s*\(",
        r"pagead",
        r"\badvertisement\b",
        r"\b22201407306\b",
        r"\b280\b",
        r"\b336\b",
        r"\b250\b",
        r"\b300\b",
        r"\bcom\b",
        r"\blink\b"
    ]

    for p in patterns:
        text = re.sub(p, " ", text, flags=re.IGNORECASE)

    return text


def remove_news_portal(text):
    if not (pd.notna(text) and isinstance(text, str)):
        return text

    text = re.sub(
        r"^.*?\b(?:kompas|detik)\s+com\b\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )

    return text


def remove_html(text):
    if pd.notna(text) and isinstance(text, str):
        return re.sub(r"<.*?>", "", text)
    return text


def remove_emoji(text):
    if not (pd.notna(text) and isinstance(text, str)):
        return text

    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F900-\U0001F9FF"
        "\U0001FA70-\U0001FAFF"
        "\U0001F1E0-\U0001F1FF"
        "]+",
        flags=re.UNICODE,
    )

    return emoji_pattern.sub("", text)


def remove_location_prefix(text):
    if not (pd.notna(text) and isinstance(text, str)):
        return text

    text = re.sub(r"^\s*,+\s*", "", text)

    text = re.sub(
        r"^[a-z0-9\s.,()/]{2,100}\s*-\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )

    return text


def remove_punctuation(text):
    if pd.notna(text) and isinstance(text, str):
        return re.sub(r"[^\w\s.,!?:;()\-/'\"]", " ", text)
    return text


def case_folding(text):
    if pd.notna(text) and isinstance(text, str):
        return text.lower()
    return text


def remove_extra_spaces(text):
    if pd.notna(text) and isinstance(text, str):
        return re.sub(r"\s+", " ", text).strip()
    return text


def clean_detik(text):
    if not isinstance(text, str):
        return text

    text = re.sub(
        r"(?i)scroll\s+to\s+continue\s+with\s+content",
        " ",
        text,
    )

    text = re.sub(
        r"(?i)advertisement",
        " ",
        text,
    )

    text = re.sub(
        r"\[gambas:.*?\]",
        " ",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"\(([a-z]{2,4}/[a-z]{2,4})\)$",
        " ",
        text.strip(),
        flags=re.IGNORECASE,
    )

    return re.sub(r"\s+", " ", text).strip()


def clean_kompas(text):
    if not isinstance(text, str):
        return text

    text = re.sub(
        r"(?i)baca\s+juga\s*:.*?(?=\n|\.\s|$)",
        " ",
        text,
    )

    text = re.sub(
        r"(?i)KOMPAS\.com\s*-?\s*",
        " ",
        text,
    )

    return re.sub(r"\s+", " ", text).strip()


# ==========================================================
# PREPROCESSING PIPELINE
# ==========================================================

def preprocess_text(text):

    if not isinstance(text, str):
        return ""

    text = fix_encoding(text)
    text = remove_bad_unicode(text)
    text = remove_ads_script(text)
    text = remove_url(text)
    text = remove_news_portal(text)
    text = remove_html(text)
    text = remove_emoji(text)
    text = remove_factcheck_words(text)
    text = remove_punctuation(text)
    text = case_folding(text)
    text = remove_location_prefix(text)
    text = remove_extra_spaces(text)
    text = remove_noise(text)
    text = clean_detik(text)
    text = clean_kompas(text)
    text = remove_extra_spaces(text)

    return text
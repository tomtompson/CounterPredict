import re
from datetime import datetime
from typing import TYPE_CHECKING, Any

import pytz

if TYPE_CHECKING:
    from collections.abc import Callable

    from lxml import etree


def extract_date_from_headline(
    section_element: etree._Element,
    get_text_by_xpath: Callable[[str, Any], str | None],
) -> str | None:
    """
    Extract date (YYYY-MM-DD) from section headline.

    Args:
        section_element (etree._Element): lxml element of the section.
        get_text_by_xpath (Callable[[str, Any], str | None]): function to extract
            text from element with xpath (signature: (xpath, element=...) -> str | None).

    Returns:
        str | None: date string or None.
    """
    headline = get_text_by_xpath(
        ".//div[contains(@class, 'matches-list-headline')]/text()",
        element=section_element,
    )
    if headline:
        match = re.search(r"(\d{4}-\d{2}-\d{2})", headline)
        if match:
            return match.group(1)
    return None


def convert_timestamp_to_user_timezone(
    timestamp_ms: float,
    user_timezone: str = "UTC",
    logger: Any | None = None,
) -> dict | None:
    """
    Convert UTC timestamp (ms) to user's timezone.

    Args:
        timestamp_ms (float): timestamp in milliseconds since epoch (UTC).
        user_timezone (str, optional): IANA timezone name. Defaults to "UTC".
        logger (Any | None, optional): logger for error messages. Defaults to None.

    Returns:
        dict | None: dict with keys date_str, time_str, datetime_str, weekday, timezone,
            or None if conversion fails.
    """
    if not timestamp_ms:
        return None

    try:
        dt_utc = datetime.utcfromtimestamp(timestamp_ms / 1000)
        dt_utc = pytz.UTC.localize(dt_utc)
        tz = pytz.timezone(user_timezone)
        dt_local = dt_utc.astimezone(tz)

        return {
            "date_str": dt_local.strftime("%Y-%m-%d"),
            "time_str": dt_local.strftime("%H:%M"),
            "datetime_str": dt_local.strftime("%Y-%m-%d %H:%M:%S"),
            "weekday": dt_local.strftime("%A"),
            "timezone": user_timezone,
        }
    except Exception as e:
        if logger:
            logger.exception(
                f"failed to convert timestamp {timestamp_ms} to {user_timezone}: {e}",
            )
        return None


def trim(text: list | str) -> str:
    """
    Trim input text by removing extra spaces and non-breaking spaces.

    Args:
        text (list | str): text to trim; list elements are joined before trimming.

    Returns:
        str: trimmed text.
    """
    if isinstance(text, list):
        text = "".join(text)

    return text.strip().replace("\xa0", "").replace("'", "")


def extract_from_url(hltv_url: str | None, element: str) -> str | None:
    """
    Extract a named element from an HLTV URL using regex.

    Args:
        hltv_url (str | None): HLTV profile URL to extract information from.
        element (str): named group to extract (e.g., "id", "nickname", "team_name").

    Returns:
        str | None: extracted value, or None if not found.
    """
    if not hltv_url:
        return None

    patterns = {
        "player": r"/player/(?P<id>\d+)(?:/(?P<nickname>[\w\-]+))?",
        "team": r"/team/(?P<id>\d+)(?:/(?P<team_name>[\w\-]+))?",
        "event": r"/events/(?P<id>\d+)(?:/(?P<event_name>[\w\-]+))?",
        "coach": r"/coach/(?P<id>\d+)(?:/(?P<nickname>[\w\-]+))?",
        "match": r"/matches/(?P<id>\d+)(?:/(?P<match_name>[\w\-]+))",
    }

    for pattern in patterns.values():
        match = re.search(pattern, hltv_url)
        if match:
            return match.groupdict().get(element)

    return None


def extract_nickname_from_name(full_name: str) -> str | None:
    """
    Extract the nickname from a player's full name enclosed in single quotes.

    Args:
        full_name (str): full name of the player.

    Returns:
        str | None: extracted nickname, or None if not found.
    """
    match = re.search(r"'([^']+)'", full_name)
    return match.group(1) if match else None


def extract_country_name_from_flag_url(flag_url: str) -> str | None:
    """
    Extract the country name from an HLTV flag image URL.

    Args:
        flag_url (str): URL of the flag image.

    Returns:
        str | None: country name, or None if not found.
    """
    country_names = {
        "AE": "United Arab Emirates",
        "AF": "Afghanistan",
        "AL": "Albania",
        "AM": "Armenia",
        "AO": "Angola",
        "AR": "Argentina",
        "AS": "American Samoa",
        "AT": "Austria",
        "AU": "Australia",
        "AW": "Aruba",
        "AX": "Åland Islands",
        "AZ": "Azerbaijan",
        "BA": "Bosnia and Herzegovina",
        "BB": "Barbados",
        "BD": "Bangladesh",
        "BE": "Belgium",
        "BF": "Burkina Faso",
        "BG": "Bulgaria",
        "BH": "Bahrain",
        "BI": "Burundi",
        "BJ": "Benin",
        "BM": "Bermuda",
        "BN": "Brunei",
        "BO": "Bolivia",
        "BR": "Brazil",
        "BS": "Bahamas",
        "BT": "Bhutan",
        "BW": "Botswana",
        "BY": "Belarus",
        "BZ": "Belize",
        "CA": "Canada",
        "CD": "Democratic Republic of the Congo",
        "CF": "Central African Republic",
        "CG": "Congo",
        "CH": "Switzerland",
        "CI": "Ivory Coast",
        "CL": "Chile",
        "CM": "Cameroon",
        "CN": "China",
        "CO": "Colombia",
        "CR": "Costa Rica",
        "CU": "Cuba",
        "CV": "Cape Verde",
        "CY": "Cyprus",
        "CZ": "Czech Republic",
        "DE": "Germany",
        "DK": "Denmark",
        "DO": "Dominican Republic",
        "DZ": "Algeria",
        "EC": "Ecuador",
        "EE": "Estonia",
        "EG": "Egypt",
        "ES": "Spain",
        "ET": "Ethiopia",
        "EU": "Europe",
        "FI": "Finland",
        "FJ": "Fiji",
        "FR": "France",
        "GA": "Gabon",
        "GB": "United Kingdom",
        "GE": "Georgia",
        "GH": "Ghana",
        "GL": "Greenland",
        "GM": "Gambia",
        "GN": "Guinea",
        "GR": "Greece",
        "GT": "Guatemala",
        "GU": "Guam",
        "GW": "Guinea-Bissau",
        "GY": "Guyana",
        "HK": "Hong Kong",
        "HN": "Honduras",
        "HR": "Croatia",
        "HT": "Haiti",
        "HU": "Hungary",
        "ID": "Indonesia",
        "IE": "Ireland",
        "IL": "Israel",
        "IN": "India",
        "IQ": "Iraq",
        "IR": "Iran",
        "IS": "Iceland",
        "IT": "Italy",
        "JM": "Jamaica",
        "JO": "Jordan",
        "JP": "Japan",
        "KE": "Kenya",
        "KG": "Kyrgyzstan",
        "KH": "Cambodia",
        "KR": "South Korea",
        "KW": "Kuwait",
        "KZ": "Kazakhstan",
        "LA": "Laos",
        "LB": "Lebanon",
        "LK": "Sri Lanka",
        "LR": "Liberia",
        "LS": "Lesotho",
        "LT": "Lithuania",
        "LU": "Luxembourg",
        "LV": "Latvia",
        "LY": "Libya",
        "MA": "Morocco",
        "MC": "Monaco",
        "MD": "Moldova",
        "ME": "Montenegro",
        "MG": "Madagascar",
        "MK": "North Macedonia",
        "ML": "Mali",
        "MM": "Myanmar",
        "MN": "Mongolia",
        "MO": "Macau",
        "MR": "Mauritania",
        "MT": "Malta",
        "MU": "Mauritius",
        "MV": "Maldives",
        "MW": "Malawi",
        "MX": "Mexico",
        "MY": "Malaysia",
        "MZ": "Mozambique",
        "NA": "Namibia",
        "NE": "Niger",
        "NG": "Nigeria",
        "NI": "Nicaragua",
        "NL": "Netherlands",
        "NO": "Norway",
        "NP": "Nepal",
        "NZ": "New Zealand",
        "OM": "Oman",
        "PA": "Panama",
        "PE": "Peru",
        "PG": "Papua New Guinea",
        "PH": "Philippines",
        "PK": "Pakistan",
        "PL": "Poland",
        "PT": "Portugal",
        "PY": "Paraguay",
        "QA": "Qatar",
        "RO": "Romania",
        "RS": "Serbia",
        "RU": "Russia",
        "RW": "Rwanda",
        "SA": "Saudi Arabia",
        "SE": "Sweden",
        "SG": "Singapore",
        "SI": "Slovenia",
        "SK": "Slovakia",
        "SN": "Senegal",
        "SO": "Somalia",
        "SY": "Syria",
        "TH": "Thailand",
        "TJ": "Tajikistan",
        "TL": "East Timor",
        "TN": "Tunisia",
        "TR": "Turkey",
        "TT": "Trinidad and Tobago",
        "TW": "Taiwan",
        "TZ": "Tanzania",
        "UA": "Ukraine",
        "UG": "Uganda",
        "US": "United States",
        "UY": "Uruguay",
        "UZ": "Uzbekistan",
        "VE": "Venezuela",
        "VN": "Vietnam",
        "YE": "Yemen",
        "ZA": "South Africa",
        "ZM": "Zambia",
        "ZW": "Zimbabwe",
    }
    match = re.search(r"/([A-Z]{2})\.gif$", flag_url)

    if match:
        country_code = match.group(1)
        return country_names.get(country_code, country_code)
    return None


def extract_age(age_str: str | None) -> int | None:
    """
    Extract the numeric age from a string in the format 'XX years'.

    Args:
        age_str (str | None): age string (e.g., '28 years').

    Returns:
        int | None: extracted age, or None if extraction fails.
    """
    if age_str:
        match = re.match(r"(\d+)\s+years", age_str)
        if match:
            return int(match.group(1))

    return None


def extract_float_from_percentage_number(percentage_str: str) -> float | None:
    """
    Extract the numeric value from a percentage string in the format '+XX%' or '-XX%'.

    Args:
        percentage_str (str): percentage string (e.g., '+5.34%', '-5.55%', '28%').

    Returns:
        float | None: extracted float value (positive or negative), or None if extraction fails.
    """
    if percentage_str:
        match = re.match(r"([+-]?\d+(?:\.\d+)?)%", percentage_str)
        if match:
            return float(match.group(1))
    
    return None

def convert_minutes_to_seconds(minutes_str: str) -> int | None:
    """
    Convert a duration string in the format 'Xm Xs' to total seconds.

    Args:
        minutes_str (str): duration string (e.g., '1m 2s').

    Returns:
        int | None: total seconds, or None if conversion fails.
    """
    if minutes_str:
        minutes = 0
        seconds = 0

        match_minutes = re.search(r"(\d+)m", minutes_str)
        if match_minutes:
            minutes = int(match_minutes.group(1))

        match_seconds = re.search(r"(\d+)s", minutes_str)
        if match_seconds:
            seconds = int(match_seconds.group(1))

            return minutes * 60 + seconds

    return None


def parse_float(value: str | None, silent: bool = True) -> float | None:
    """
    Convert a string value to a float.

    Args:
        value (str | None): string to parse.
        silent (bool, optional): if True, returns None on failure instead of raising. Defaults to True.

    Raises:
        ValueError: if the value cannot be parsed and silent is False.

    Returns:
        float | None: parsed float, or None if conversion fails or input is empty/'-'.
    """
    if value is None or value.strip() in {"", "-"}:
        return None
    try:
        return float(value.strip())
    except ValueError:
        if silent:
            return None
        msg = f"Invalid float value: '{value}'"
        raise ValueError(msg)


def parse_int(value: str | None, silent: bool = True) -> int | None:
    """
    Convert a string value to an integer.

    Args:
        value (str | None): string to parse.
        silent (bool, optional): if True, returns None on failure instead of raising. Defaults to True.

    Raises:
        ValueError: if the value cannot be parsed and silent is False.

    Returns:
        int | None: parsed integer, or None if conversion fails or input is empty/'-'.
    """
    if value is None or value.strip() in {"", "-"}:
        return None
    try:
        return int(value.strip())
    except ValueError:
        if silent:
            return None
        msg = f"Invalid float value: '{value}'"
        raise ValueError(msg)


def clear_number_str(value: str | None) -> str | None:
    """
    Strip all non-digit characters from a string.

    Args:
        value (str | None): string to clear.

    Returns:
        str | None: string containing only numeric digits, or None if input is falsy.
    """
    if value:
        return re.sub(r"\D", "", value)

    return None


def parse_date(date: str) -> str | None:

    match = re.search(r"([A-Z][a-z]+) (\d{1,2})(?:st|nd|rd|th)?[,\s]+(\d{4})", date)

    if match:
        month, day, year = match.groups()
        try:
            parsed_date = datetime.strptime(f"{month} {day} {year}", "%B %d %Y")
            return parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            return None

    return None


def get_common_timezones() -> list[str]:
    """
    Return a list of common IANA timezone names.

    Returns:
        list[str]: list of IANA timezone strings.
    """
    return pytz.common_timezones

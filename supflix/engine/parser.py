import re
from typing import Optional

QUALITY_PATTERN = r"(2160p|4K|1080p|720p|480p|360p)"
YEAR_PATTERN = r"(19\d{2}|20\d{2})"
SEASON_EPISODE_PATTERN = r"S(\d{1,2})E(\d{1,2})"

LANGUAGES = [
    "Hindi",
    "English",
    "Tamil",
    "Telugu",
    "Malayalam",
    "Kannada",
    "Bengali",
    "Punjabi",
    "Marathi",
    "Japanese",
    "Korean",
    "Chinese",
    "Dual Audio",
    "Multi Audio"
]

SOURCES = [
    "WEB-DL",
    "WEBRip",
    "BluRay",
    "HDRip",
    "HDTV",
    "DVDRip",
    "CAM",
    "NF",
    "AMZN"
]

CODECS = [
    "x264",
    "x265",
    "H264",
    "H265",
    "HEVC",
    "AV1"
]


def _extract_year(text: str) -> Optional[int]:
    match = re.search(YEAR_PATTERN, text)
    return int(match.group()) if match else None


def _extract_quality(text: str):
    match = re.search(QUALITY_PATTERN, text, re.IGNORECASE)
    return match.group() if match else None


def _extract_source(text: str):
    for source in SOURCES:
        if source.lower() in text.lower():
            return source
    return None


def _extract_codec(text: str):
    for codec in CODECS:
        if codec.lower() in text.lower():
            return codec
    return None


def _extract_languages(text: str):
    found = []

    for lang in LANGUAGES:
        if lang.lower() in text.lower():
            found.append(lang)

    return found


def _extract_season_episode(text: str):
    match = re.search(SEASON_EPISODE_PATTERN, text, re.IGNORECASE)

    if not match:
        return None, None

    return int(match.group(1)), int(match.group(2))


def _clean_title(text: str):

    title = text

    title = re.sub(r"\.[^.]+$", "", title)

    title = title.replace(".", " ")
    title = title.replace("_", " ")

    title = re.sub(SEASON_EPISODE_PATTERN, "", title, flags=re.IGNORECASE)
    title = re.sub(YEAR_PATTERN, "", title)
    title = re.sub(QUALITY_PATTERN, "", title, flags=re.IGNORECASE)

    for source in SOURCES:
        title = re.sub(source, "", title, flags=re.IGNORECASE)

    for codec in CODECS:
        title = re.sub(codec, "", title, flags=re.IGNORECASE)

    for lang in LANGUAGES:
        title = re.sub(lang, "", title, flags=re.IGNORECASE)

    title = re.sub(r"HDR10\+?", "", title, flags=re.IGNORECASE)
    title = re.sub(r"HDR", "", title, flags=re.IGNORECASE)
    title = re.sub(r"DV", "", title, flags=re.IGNORECASE)
    title = re.sub(r"Dolby Vision", "", title, flags=re.IGNORECASE)

    title = re.sub(r"\s+", " ", title).strip()

    return title


def parse_filename(filename: str):

    season, episode = _extract_season_episode(filename)

    media_type = "tv" if season else "movie"

    return {
        "title": _clean_title(filename),
        "type": media_type,
        "year": _extract_year(filename),
        "season": season,
        "episode": episode,
        "quality": _extract_quality(filename),
        "source": _extract_source(filename),
        "codec": _extract_codec(filename),
        "languages": _extract_languages(filename),
        "hdr": "hdr" in filename.lower(),
        "dolby_vision": (
            "dolby vision" in filename.lower()
            or " dv " in f" {filename.lower()} "
        ),
    }
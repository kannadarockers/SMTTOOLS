from dataclasses import dataclass, field


@dataclass
class MediaQuality:

    quality: str

    telegram_file_id: str | None = None

    file_name: str | None = None

    file_size: int | None = None

    codec: str | None = None

    languages: list[str] = field(default_factory=list)


@dataclass
class Media:

    title: str

    type: str

    year: int | None = None

    season: int | None = None

    episode: int | None = None

    source: str | None = None

    hdr: bool = False

    dolby_vision: bool = False

    qualities: list[MediaQuality] = field(default_factory=list)
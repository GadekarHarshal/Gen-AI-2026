from dataclasses import dataclass


@dataclass
class Record:
    course_id: str
    course_name: str
    discipline: str
    institute: str
    duration_weeks: int | str
    course_url: str
    
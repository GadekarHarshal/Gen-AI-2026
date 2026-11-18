
from datetime import date

from ui.planner import (
    calculate_weekly_workload,
    find_exam_clashes
)


def test_detect_exam_clash():
    schedule = [
        {"Course": "Course A", "Exam Date": date(2027, 2, 10)},
        {"Course": "Course B", "Exam Date": date(2027, 2, 10)}
    ]

    clashes = find_exam_clashes(schedule)

    assert clashes == {date(2027, 2, 10): 2}


def test_no_exam_clash():
    schedule = [
        {"Course": "Course A", "Exam Date": date(2027, 2, 10)},
        {"Course": "Course B", "Exam Date": date(2027, 2, 11)}
    ]

    clashes = find_exam_clashes(schedule)

    assert clashes == {}


def test_two_courses_workload():
    result = calculate_weekly_workload(2)

    assert result == 6


def test_three_courses_workload():
    result = calculate_weekly_workload(3)

    assert result == 9

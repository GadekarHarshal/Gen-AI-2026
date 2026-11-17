
import pytest

from app.tools import course_plan_checker


def test_valid_course_plan():
    result = course_plan_checker(
        ["noc26_cs169", "noc26_cs98"],
        8
    )

    assert result["total_courses"] == 2
    assert result["total_credits"] == 6
    assert result["estimated_hours_per_week"] == 6
    assert result["workload_status"] == "Sufficient study hours"


def test_insufficient_study_hours():
    result = course_plan_checker(
        ["noc26_cs169", "noc26_cs98"],
        4
    )

    assert result["workload_status"] == "Insufficient study hours"


def test_invalid_course_id():
    result = course_plan_checker(
        ["invalid_course", "noc26_cs169"],
        8
    )

    assert result["total_courses"] == 1
    assert result["unknown_course_ids"] == ["invalid_course"]


def test_empty_course_list():
    with pytest.raises(ValueError):
        course_plan_checker([], 8)


def test_invalid_available_hours():
    with pytest.raises(ValueError):
        course_plan_checker(["noc26_cs169"], 0)


def test_exam_dates_unavailable():
    result = course_plan_checker(
        ["noc26_cs169"],
        8
    )

    assert "Unavailable" in result["exam_clash_check"]

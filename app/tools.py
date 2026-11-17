
from app.records import get_by_id


# Planned credit mapping
CREDIT_MAPPING = {
    4: 1,
    8: 2,
    12: 3
}

# Planning assumption, not official NPTEL workload
ESTIMATED_HOURS_PER_COURSE = 3


def course_plan_checker(
    course_ids,
    available_hours_per_week
):
    """
    Check a student's selected NPTEL courses.

    Estimates 3 study hours per course per week.
    Credits are calculated using course duration.
    """

    if not course_ids:
        raise ValueError("Please provide at least one course ID.")

    if available_hours_per_week <= 0:
        raise ValueError("Available study hours must be greater than zero.")

    selected_courses = []
    total_credits = 0
    total_estimated_hours = 0
    not_found = []

    for course_id in course_ids:

        course = get_by_id(course_id)

        if course is None:
            not_found.append(course_id)
            continue

        try:
            duration = int(course["duration_weeks"])
        except (ValueError, TypeError):
            duration = None

        credits = CREDIT_MAPPING.get(duration)

        if credits is not None:
            total_credits += credits

        estimated_hours = ESTIMATED_HOURS_PER_COURSE

        total_estimated_hours += estimated_hours

        selected_courses.append({
            "course_id": course["course_id"],
            "course_name": course["course_name"],
            "duration_weeks": duration,
            "credits": credits,
            "estimated_hours_per_week": estimated_hours
        })

    if not selected_courses:
        raise ValueError("No valid course IDs were found.")

    workload_status = (
        "Sufficient study hours"
        if total_estimated_hours <= available_hours_per_week
        else "Insufficient study hours"
    )

    return {
        "selected_courses": selected_courses,
        "total_courses": len(selected_courses),
        "total_credits": total_credits,
        "available_hours_per_week": available_hours_per_week,
        "estimated_hours_per_week": total_estimated_hours,
        "workload_status": workload_status,
        "workload_assumption": (
            "3 estimated study hours per course per week"
        ),
        "unknown_course_ids": not_found,
        "exam_clash_check": (
            "Unavailable: examination dates are not present "
            "in the dataset."
        )
    }

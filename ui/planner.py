
import json
from datetime import date, timedelta
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RECORDS_FILE = PROJECT_ROOT / "data" / "records.json"

HOURS_PER_COURSE = 3  # Project estimate, not official NPTEL workload


def load_courses():
    """Load available courses from records.json."""
    with open(RECORDS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def find_exam_clashes(schedule):
    """Return exam dates shared by two or more courses."""
    exam_counts = {}

    for course in schedule:
        exam_day = course["Exam Date"]
        exam_counts[exam_day] = exam_counts.get(exam_day, 0) + 1

    return {
        exam_day: count
        for exam_day, count in exam_counts.items()
        if count > 1
    }


def calculate_weekly_workload(number_of_courses):
    """Estimate weekly workload using 3 hours per course."""
    return number_of_courses * HOURS_PER_COURSE


def render_planner():
    st.header("📅 Semester Planner")

    st.info(
        "Exam dates must be entered manually. "
        "They are student-provided dates, not official NPTEL dates."
    )

    try:
        courses = load_courses()
    except (OSError, json.JSONDecodeError) as error:
        st.error(f"Unable to load course records: {error}")
        return

    course_options = {
        course["course_name"]: course
        for course in courses
    }

    selected_names = st.multiselect(
        "Select your NPTEL courses",
        options=list(course_options.keys())
    )

    available_hours = st.number_input(
        "How many hours can you study per week?",
        min_value=1,
        max_value=100,
        value=10,
        step=1
    )

    if not selected_names:
        st.info("Select at least one course to create your semester plan.")
        return

    st.subheader("Course Schedule")

    schedule = []

    for course_name in selected_names:

        course = course_options[course_name]

        with st.expander(course_name, expanded=True):

            st.write(f"**Institute:** {course.get('institute', 'Unknown')}")
            st.write(f"**Duration:** {course.get('duration_weeks', 'Unknown')} weeks")

            start_date = st.date_input(
                "Study start date",
                value=date.today(),
                key=f"start_{course['course_id']}"
            )

            exam_date = st.date_input(
                "Exam date (enter manually)",
                value=date.today() + timedelta(
                    weeks=int(course.get("duration_weeks", 12))
                ),
                key=f"exam_{course['course_id']}"
            )

            if exam_date < start_date:
                st.error("Exam date cannot be before the study start date.")
                continue

            schedule.append({
                "Course": course_name,
                "Institute": course.get("institute", "Unknown"),
                "Start Date": start_date,
                "Exam Date": exam_date,
                "Duration (Weeks)": course.get("duration_weeks", "Unknown")
            })

    if not schedule:
        st.warning("Please correct the course dates to view your plan.")
        return

    dataframe = pd.DataFrame(schedule)

    st.divider()
    st.subheader("Semester Timeline")

    chart = alt.Chart(dataframe).mark_bar(
        cornerRadius=5,
        height=25
    ).encode(
        x=alt.X("Start Date:T", title="Timeline"),
        x2="Exam Date:T",
        y=alt.Y("Course:N", title="Selected Courses", sort=None),
        tooltip=[
            "Course:N",
            "Institute:N",
            "Start Date:T",
            "Exam Date:T"
        ]
    ).properties(
        height=max(150, len(schedule) * 55)
    )

    st.altair_chart(chart, use_container_width=True)

    st.subheader("Exam Clash Check")

    clashes = find_exam_clashes(schedule)

    if clashes:
        for exam_day, count in clashes.items():
            st.error(
                f"Exam clash: {count} courses have an exam on "
                f"{exam_day.strftime('%d %B %Y')}."
            )
    else:
        st.success("No exam-date clashes found in your entered schedule.")

    st.subheader("Weekly Workload")

    estimated_hours = calculate_weekly_workload(len(schedule))

    col1, col2 = st.columns(2)

    col1.metric("Estimated weekly study hours", estimated_hours)
    col2.metric("Your available weekly hours", available_hours)

    if estimated_hours > available_hours:
        st.warning(
            "Your estimated workload exceeds your available weekly hours. "
            "Consider reducing courses or increasing study time."
        )
    else:
        st.success("Your estimated workload is within your available hours.")

    st.subheader("Plan Summary")
    st.dataframe(dataframe, use_container_width=True)

    csv_data = dataframe.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Semester Plan (CSV)",
        data=csv_data,
        file_name="nptel_semester_plan.csv",
        mime="text/csv"
    )

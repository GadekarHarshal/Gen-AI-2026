from app.records import load_records, search, count_by, get_by_id


def main():
    records = load_records()

    print("\n===== NPTELPicker =====")
    print("Total Courses:", len(records))

    while True:
        print("\n1. Show all courses")
        print("2. Search course")
        print("3. Count by discipline")
        print("4. Find course by ID")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            for course in records:
                print(course["course_name"], "-", course["institute"])

        elif choice == "2":
            keyword = input("Enter course keyword: ")
            results = search(keyword)

            for course in results:
                print(course["course_name"])

            if not results:
                print("No courses found.")

        elif choice == "3":
            print(count_by("discipline"))

        elif choice == "4":
            course_id = input("Enter course ID: ")
            result = get_by_id(course_id)

            if result:
                print(result)
            else:
                print("Course not found.")

        elif choice == "0":
            print("Thank you for using NPTELPicker!")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()

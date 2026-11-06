
while True:
    print("\n1. About NPTELPicker")
    print("2. Sample Questions")
    print("3. Course Rule Check")
    print("0. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        print("NPTELPicker helps students find NPTEL courses.")

    elif choice == "2":
        print("1. Best Python course?")
        print("2. Best AI course?")

    elif choice == "3":
        interest = input("Enter interest (python/ai): ")

        if interest == "python":
            print("Explore Python courses.")
        elif interest == "ai":
            print("Explore AI courses.")
        else:
            print("Explore other NPTEL courses.")

    elif choice == "0":
        print("Goodbye!")
        break

    else:
        print("Invalid choice.")

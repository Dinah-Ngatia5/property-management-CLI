def main_menu():
    while True:
        print("\nProperty Management System Menu 🏰:")
        print("1. Property Operations 🏠")
        print("2. Owner Operations 👨‍💼")
        print("3. Tenant Operations 🤝")
        print("4. Rent Payment Operations 💰")
        print("5. Maintenance Request Operations 🛠️")
        print("6. Expense Operations 💸")
        print("7. Document Operations 📁")
        print("8. Reports and Analytics 📊")
        print("9. Exit 🚪")
        
        choice = input("\nEnter your choice: ")

        if choice  == "1":
            property_operations()
        elif choice == "2":
            owner_operations()
        elif choice == "3":
            owner_operations()
        elif choice == "4":
            owner_operations()
        elif choice == "5":
            owner_operations()
        elif choice == "6":
            owner_operations()
        elif choice == "7":
            owner_operations()
        elif choice == "8":
            owner_operations()
        elif choice == "9":
            print("Goodbye! See yah👋")
            break
        else:
            print("Invalid choice. Please try again.")










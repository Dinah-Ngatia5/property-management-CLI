
from cli import property, owner, tenant, expense, document, main, rent_payment, maintenance_request
def main_menu():
    while True:
        print("\nProperty Management System Menu 🏰:\n")
        print("1. Property Operations 🏠")
        print("2. Owner Operations 👨‍💼")
        print("3. Tenant Operations 🤝")
        print("4. Rent Payment Operations 💰")
        print("5. Maintenance Request Operations 🛠️")
        print("6. Expense Operations 💸")
        print("7. Document Operations 📁")
        print("8. Register or Login")
        print("9. Exit 🚪")
        
        choice = input("\nEnter your choice: ")

        if choice  == "1":
            property()
        elif choice == "2":
            owner()
        elif choice == "3":
            tenant()
        elif choice == "4":
            rent_payment()
        elif choice == "5":
            maintenance_request()
        elif choice == "6":
            expense()
        elif choice == "7":
            document()
        elif choice == "8":
            main()
        elif choice == "9":
            print("Goodbye! See yah👋")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()







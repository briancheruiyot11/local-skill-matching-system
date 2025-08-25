from lib.models.worker import Worker, SKILLS
from lib.helpers import display_table


# Main Menu 
def main_menu():
    while True:
        print("\n=== LOCAL SKILL MATCHING ===")
        print("1. Workers")
        print("2. Service Requests")
        print("3. Reviews")
        print("4. Search Workers")
        print("0. Exit")

        choice = input("> ").strip()

        if choice == "1":
            workers_menu()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


# Workers Menu 
def workers_menu():
    while True:
        print("\n--- Workers Menu ---")
        print("1. Add Worker")
        print("2. Delete Worker")
        print("3. List All Workers")
        print("4. Find Worker by ID")
        print("5. Find Worker by Name")
        print("6. Find Workers by Skill")
        print("7. Find Workers by Location")
        print("8. View a Worker's Service Requests")
        print("9. View a Worker's Reviews")
        print("0. Back")

        choice = input("> ").strip()

        if choice == "1":
            name = input("Name: ")
            skill = input(f"Skill {SKILLS}: ")
            phone = input("Phone: ")
            location = input("Location: ")
            try:
                worker = Worker.create(name=name, skill=skill, phone=phone, location=location)
                print(f"Worker {worker.name} added successfully!")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "2":
            wid = input("Enter Worker ID to delete: ")
            if Worker.delete(int(wid)):
                print("Worker deleted.")
            else:
                print("Worker not found.")

        elif choice == "3":
            workers = Worker.get_all()
            data = [(w.id, w.name, w.skill, w.phone, w.location, w.created_at) for w in workers]
            display_table(data, headers=["ID", "Name", "Skill", "Phone", "Location", "Created At"])

        elif choice == "4":
            wid = input("Worker ID: ")
            worker = Worker.get_by_id(int(wid))
            if worker:
                display_table(
                    [(worker.id, worker.name, worker.skill, worker.phone, worker.location, worker.created_at)],
                    headers=["ID", "Name", "Skill", "Phone", "Location", "Created At"]
                )
            else:
                print("Worker not found.")

        elif choice == "5":
            name = input("Enter name to search: ")
            workers = Worker.find_by_name(name)
            data = [(w.id, w.name, w.skill, w.phone, w.location) for w in workers]
            display_table(data, headers=["ID", "Name", "Skill", "Phone", "Location"])

        elif choice == "6":
            skill = input(f"Enter skill {SKILLS}: ")
            workers = Worker.find_by_skill(skill)
            data = [(w.id, w.name, w.skill, w.phone, w.location) for w in workers]
            display_table(data, headers=["ID", "Name", "Skill", "Phone", "Location"])

        elif choice == "7":
            loc = input("Enter location substring: ")
            workers = Worker.find_by_location(loc)
            data = [(w.id, w.name, w.skill, w.phone, w.location) for w in workers]
            display_table(data, headers=["ID", "Name", "Skill", "Phone", "Location"])

        elif choice in ["8", "9"]:
            print("Feature coming soon")

        elif choice == "0":
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main_menu()

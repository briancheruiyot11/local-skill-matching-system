from lib.models.worker import Worker, SKILLS
from lib.models.service_request import ServiceRequest, STATUS
from lib.models.review import Review
from lib.helpers import display_table, print_header


def main_menu():
    while True:
        print_header("=== 👷🛠️ Local Skill Matching System 🛠️👷 ===")
        print("1. Workers")
        print("2. Service Requests")
        print("3. Reviews")
        print("0. Exit")

        choice = input("Pick an option: ").strip()

        if choice == "1":
            workers_menu()
        elif choice == "2":
            service_requests_menu()
        elif choice == "3":
            reviews_menu()
        elif choice == "0":
            print("🙋 Welcome Back Again!! 👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")


def workers_menu():
    while True:
        print_header("=== 👷‍♂️ Workers Menu ⚒️ ===")
        print("1. Add Worker")
        print("2. Delete Worker")
        print("3. List All Workers")
        print("4. Find Worker by ID")
        print("5. Find Worker by Name")
        print("6. Find Workers by Skill")
        print("7. Find Workers by Location")
        print("8. View a Worker's Service Requests")
        print("9. View a Worker's Reviews")
        print("10. Update Worker Details")
        print("0. Back")

        choice = input("Pick an option: ").strip()

        if choice == "1":
            try:
                name = input("Name: ")
                skill = input(f"Skill {SKILLS}: ")
                phone = input("Phone: ")
                location = input("Location: ")
                Worker.create(name, skill, phone, location)
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "2":
            try:
                wid = int(input("Worker ID: "))
            except ValueError:
                print("❌ Invalid ID.")
                continue
            if Worker.delete(wid):
                print("🚮 Worker deleted successfully.")
            else:
                print("❌ Worker not found.")

        elif choice == "3":
            workers = Worker.get_all()
            data = [(w.id, w.name, w.skill, w.phone, w.location) for w in workers]
            display_table(data, ["ID", "Name", "Skill", "Phone", "Location"])

        elif choice == "4":
            try:
                wid = int(input("Worker ID: "))
            except ValueError:
                print("❌ Invalid ID.")
                continue
            worker = Worker.get_by_id(wid)
            if worker:
                data = [(worker.id, worker.name, worker.skill, worker.phone, worker.location)]
                display_table(data, ["ID", "Name", "Skill", "Phone", "Location"])
            else:
                print("❌ Worker not found.")

        elif choice == "5":
            name = input("Enter name to search: ")
            workers = Worker.find_by_name(name)
            data = [(w.id, w.name, w.skill, w.phone, w.location) for w in workers]
            display_table(data, ["ID", "Name", "Skill", "Phone", "Location"])

        elif choice == "6":
            skill = input(f"Enter skill {SKILLS}: ")
            workers = Worker.find_by_skill(skill)
            data = [(w.id, w.name, w.skill, w.phone, w.location) for w in workers]
            display_table(data, ["ID", "Name", "Skill", "Phone", "Location"])

        elif choice == "7":
            location = input("Enter location to search: ")
            workers = Worker.find_by_location(location)
            data = [(w.id, w.name, w.skill, w.phone, w.location) for w in workers]
            display_table(data, ["ID", "Name", "Skill", "Phone", "Location"])

        elif choice == "8":
            try:
                wid = int(input("Worker ID: "))
            except ValueError:
                print("❌ Invalid ID.")
                continue
            ServiceRequest.list_by_worker(wid)

        elif choice == "9":
            try:
                wid = int(input("Worker ID: "))
            except ValueError:
                print("❌ Invalid ID.")
                continue
            Review.list_by_worker(wid)

        elif choice == "10":
            try:
                wid = int(input("Enter Worker ID to update: "))
            except ValueError:
                print("❌ Invalid ID.")
                continue
            worker = Worker.get_by_id(wid)
            if not worker:
                print("❌ Worker not found.")
                continue

            print("Leave a field blank to keep the current value.")
            name = input(f"New Name [{worker.name}]: ") or None
            skill = input(f"New Skill {SKILLS} [{worker.skill}]: ") or None
            phone = input(f"New Phone [{worker.phone}]: ") or None
            location = input(f"New Location [{worker.location}]: ") or None

            try:
                worker.update(name=name, skill=skill, phone=phone, location=location)
            except Exception as e:
                print(f"Error updating worker: {e}")

        elif choice == "0":
            break

        else:
            print("❌ Invalid choice. Please try again.")


def service_requests_menu():
    while True:
        print_header("=== 🧰 Service Requests Menu 🧰 ===")
        print("1. Add Service Request")
        print("2. Delete Service Request")
        print("3. List All Service Requests")
        print("4. Find Service Request by ID")
        print("5. View Request's Worker")
        print("6. Update Service Request")
        print("0. Back")

        choice = input("Pick an option: ").strip()

        if choice == "1":
            try:
                worker_id = int(input("Worker ID: "))
                requester_name = input("Requester Name: ")
                notes = input("Notes/Description: ")
                ServiceRequest.create(worker_id=worker_id, requester_name=requester_name, notes=notes)
                print("🎉 Service request added successfully.")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "2":
            try:
                rid = int(input("Request ID: "))
            except ValueError:
                print("❌ Invalid ID.")
                continue
            if ServiceRequest.delete(rid):
                print("🚮 Service Request deleted.")
            else:
                print("❌ Service Request not found.")

        elif choice == "3":
            ServiceRequest.list_all()

        elif choice == "4":
            try:
                rid = int(input("Request ID: "))
            except ValueError:
                print("❌ Invalid ID.")
                continue
            ServiceRequest.find_by_id(rid)

        elif choice == "5":
            try:
                rid = int(input("Request ID: "))
            except ValueError:
                print("❌ Invalid ID.")
                continue
            ServiceRequest.view_worker(rid)

        elif choice == "6":
            try:
                rid = int(input("Enter Service Request ID to update: "))
            except ValueError:
                print("❌ Invalid ID.")
                continue
            req = ServiceRequest.get_by_id(rid)
            if not req:
                print("❌ Service Request not found.")
                continue

            print("Leave blank to keep current value.")
            new_name = input(f"Current requester name: {req.requester_name}\nNew requester name: ") or None
            new_notes = input(f"Current notes: {req.notes}\nNew notes: ") or None
            new_status = input(f"Current status: {req.status}\nNew status {STATUS}: ") or None

            confirm = input("Confirm update? (yes/no): ").strip().lower()
            if confirm == "yes":
                try:
                    req.update(requester_name=new_name, notes=new_notes, status=new_status)
                    print("🎉 Service Request updated successfully.")
                except Exception as e:
                    print(f"Error updating service request: {e}")
            else:
                print("Update cancelled.")

        elif choice == "0":
            break

        else:
            print("❌ Invalid choice. Please try again.")


def reviews_menu():
    while True:
        print_header("=== ⭐ Reviews Menu ⭐ ===")
        print("1. Add Review")
        print("2. Delete Review")
        print("3. List All Reviews")
        print("4. Find Review by ID")
        print("5. View Review's Worker")
        print("0. Back")

        choice = input("Pick an option: ").strip()

        if choice == "1":
            try:
                worker_id = int(input("Worker ID: "))
                rating = int(input("Rating (1-5): "))
                comment = input("Comment: ")
                Review.create(worker_id=worker_id, rating=rating, comment=comment)
                print("🎉 Review added successfully.")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "2":
            try:
                rid = int(input("Review ID: "))
            except ValueError:
                print("Invalid ID.")
                continue
            if Review.delete(rid):
                print("🚮 Review deleted.")
            else:
                print("❌ Review not found.")

        elif choice == "3":
            Review.list_all()

        elif choice == "4":
            try:
                rid = int(input("Review ID: "))
            except ValueError:
                print("❌ Invalid ID.")
                continue
            Review.find_by_id(rid)

        elif choice == "5":
            try:
                rid = int(input("Review ID: "))
            except ValueError:
                print("❌ Invalid ID.")
                continue
            Review.view_worker(rid)

        elif choice == "0":
            break

        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()

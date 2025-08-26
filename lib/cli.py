from lib.models.worker import Worker, SKILLS
from lib.models.service_request import ServiceRequest, STATUS
from lib.models.review import Review
from lib.helpers import display_table


# Main Menu
def main_menu():
    while True:
        print("\n=== LOCAL SKILL MATCHING ===")
        print("1. Workers")
        print("2. Service Requests")
        print("3. Reviews")
        print("0. Exit")

        choice = input("> ").strip()

        if choice == "1":
            workers_menu()
        elif choice == "2":
            requests_menu()
        elif choice == "3":
            reviews_menu()
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
            data = [(w.id, w.name, w.skill, w.phone, w.location, w.created_at) for w in workers]
            display_table(data, headers=["ID", "Name", "Skill", "Phone", "Location", "Created At"])

        elif choice == "6":
            skill = input(f"Enter skill {SKILLS}: ")
            workers = Worker.find_by_skill(skill)
            data = [(w.id, w.name, w.skill, w.phone, w.location, w.created_at) for w in workers]
            display_table(data, headers=["ID", "Name", "Skill", "Phone", "Location", "Created At"])

        elif choice == "7":
            loc = input("Enter location substring: ")
            workers = Worker.find_by_location(loc)
            data = [(w.id, w.name, w.skill, w.phone, w.location, w.created_at) for w in workers]
            display_table(data, headers=["ID", "Name", "Skill", "Phone", "Location", "Created At"])

        elif choice == "8":
            wid = input("Worker ID: ")
            requests = ServiceRequest.for_worker(int(wid))
            data = [(r.id, r.requester_name, r.date, r.status, r.notes) for r in requests]
            display_table(data, headers=["ID", "Requester", "Date", "Status", "Notes"])

        elif choice == "9":
            wid = input("Worker ID: ")
            reviews = Review.for_worker(int(wid))
            data = [(rv.id, rv.rating, rv.comment, rv.created_at) for rv in reviews]
            display_table(data, headers=["ID", "Rating", "Comment", "Created At"])

        elif choice == "0":
            break
        else:
            print("Invalid choice. Try again.")

 
# Service Requests Menu
def requests_menu():
    while True:
        print("\n--- Service Requests Menu ---")
        print("1. Create Service Request")
        print("2. Delete Service Request")
        print("3. List All Requests")
        print("4. Find Request by ID")
        print("5. Find Requests by Status")
        print("6. Update Request Status")
        print("7. View Request's Worker")
        print("0. Back")

        choice = input("> ").strip()

        if choice == "1":
            wid = int(input("Worker ID: "))
            requester = input("Requester Name: ")
            status = input(f"Status {STATUS}: ")
            notes = input("Notes: ")
            try:
                req = ServiceRequest.create(worker_id=wid, requester_name=requester, status=status, notes=notes)
                print(f"Request {req.id} created successfully.")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "2":
            rid = int(input("Request ID: "))
            if ServiceRequest.delete(rid):
                print("Deleted successfully")
            else:
                print("Not found")

        elif choice == "3":
            reqs = ServiceRequest.get_all()
            data = [(r.id, r.worker_id, r.requester_name, r.date, r.status, r.notes) for r in reqs]
            display_table(data, headers=["ID", "Worker ID", "Requester", "Date", "Status", "Notes"])

        elif choice == "4":
            rid = int(input("Request ID: "))
            req = ServiceRequest.get_by_id(rid)
            if req:
                display_table([(req.id, req.worker_id, req.requester_name, req.date, req.status, req.notes)],
                              headers=["ID", "Worker ID", "Requester", "Date", "Status", "Notes"])
            else:
                print("Not found")

        elif choice == "5":
            status = input(f"Enter status {STATUS}: ")
            reqs = ServiceRequest.find_by_status(status)
            data = [(r.id, r.worker_id, r.requester_name, r.date, r.status, r.notes) for r in reqs]
            display_table(data, headers=["ID", "Worker ID", "Requester", "Date", "Status", "Notes"])

        elif choice == "6":
            rid = int(input("Request ID: "))
            req = ServiceRequest.get_by_id(rid)
            if not req:
                print("Not found")
            else:
                new_status = input(f"New status {STATUS}: ")
                try:
                    req.update_status(new_status)
                    print("Updated successfully")
                except Exception as e:
                    print(f"Error: {e}")

        elif choice == "7":
            rid = int(input("Request ID: "))
            req = ServiceRequest.get_by_id(rid)
            if req:
                worker = Worker.get_by_id(req.worker_id)
                display_table([(worker.id, worker.name, worker.skill, worker.phone, worker.location, worker.created_at)],
                              headers=["ID", "Name", "Skill", "Phone", "Location", "Created At"])
            else:
                print("Not found")

        elif choice == "0":
            break
        else:
            print("Invalid choice.")


# Reviews Menu
def reviews_menu():
    while True:
        print("\n--- Reviews Menu ---")
        print("1. Add Review")
        print("2. Delete Review")
        print("3. List All Reviews")
        print("4. Find Review by ID")
        print("5. View Review's Worker")
        print("0. Back")

        choice = input("> ").strip()

        if choice == "1":
            wid = int(input("Worker ID: "))
            rating = int(input("Rating (1-5): "))
            comment = input("Comment: ")
            try:
                review = Review.create(worker_id=wid, rating=rating, comment=comment)
                print(f"Review {review.id} added successfully")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "2":
            rid = int(input("Review ID: "))
            if Review.delete(rid):
                print("Deleted")
            else:
                print("Not found")

        elif choice == "3":
            reviews = Review.get_all()
            data = [(rv.id, rv.worker_id, rv.rating, rv.comment, rv.created_at) for rv in reviews]
            display_table(data, headers=["ID", "Worker ID", "Rating", "Comment", "Created At"])

        elif choice == "4":
            rid = int(input("Review ID: "))
            rv = Review.get_by_id(rid)
            if rv:
                display_table([(rv.id, rv.worker_id, rv.rating, rv.comment, rv.created_at)],
                              headers=["ID", "Worker ID", "Rating", "Comment", "Created At"])
            else:
                print("Not found")

        elif choice == "5":
            rid = int(input("Review ID: "))
            rv = Review.get_by_id(rid)
            if rv:
                worker = Worker.get_by_id(rv.worker_id)
                display_table([(worker.id, worker.name, worker.skill, worker.phone, worker.location, worker.created_at)],
                              headers=["ID", "Name", "Skill", "Phone", "Location", "Created At"])
            else:
                print("Not found")

        elif choice == "0":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main_menu()

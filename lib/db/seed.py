from faker import Faker
import random
from datetime import date, timedelta
from lib.models.worker import Worker, SKILLS
from lib.models.service_request import ServiceRequest, STATUS
from lib.models.review import Review
from lib.db.db import Base, engine, SessionLocal

fake = Faker()

# Kenyan first and last names
KENYAN_FIRST_NAMES = [
    "James", "Mary", "John", "Grace", "Peter", "Faith", "Daniel", "Esther",
    "Joseph", "Anne", "David", "Mercy", "Michael", "Rose", "Paul", "Linda", "Vivian"
]
KENYAN_LAST_NAMES = [
    "Kiprop", "Mutua", "Odinga", "Kamau", "Wambui", "Otieno", "Mwangi", "Njoroge", "Gichure"
]

# Kenyan cities
KENYAN_CITIES = [
    "Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret", "Thika", "Naivasha", "Machakos"
]

# Realistic review comments
REVIEW_COMMENTS = [
    "He is good at his job",
    "She completed the job on time",
    "Very professional and reliable",
    "Work quality was excellent",
    "Would hire again",
    "Friendly and efficient",
    "Did the job as expected",
    "Highly recommend this worker",
    "Arrived on time and finished well",
    "Communication was great"
]

def random_name():
    return f"{random.choice(KENYAN_FIRST_NAMES)} {random.choice(KENYAN_LAST_NAMES)}"

def random_location():
    return random.choice(KENYAN_CITIES)

def random_date_within_years(years=10):
    """Generate a random Python date within the last `years` years"""
    start_date = date.today() - timedelta(days=365*years)
    random_days = random.randint(0, 365*years)
    return start_date + timedelta(days=random_days)

def seed_data(n_workers=20, n_requests=10, n_reviews=30):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session = SessionLocal()

    try:
        # Seed Workers
        workers = []
        for _ in range(n_workers):
            try:
                w = Worker(
                    name=random_name(),
                    skill=random.choice(SKILLS),
                    phone="07" + str(random.randint(10000000, 99999999)),
                    location=random_location()
                )
                session.add(w)
                session.commit()
                session.refresh(w)   
                workers.append(w)
            except Exception as e:
                session.rollback()
                print(f"Skipping worker: {e}")

        # Seed Service Requests
        for _ in range(n_requests):
            try:
                worker = random.choice(workers)
                skill = worker.skill.lower()

                # Generate notes based on skill
                if skill == "carpenter":
                    note = f"I need a {fake.color_name()} {fake.word()} table"
                elif skill == "plumber":
                    note = f"Fix a leaking {fake.word()}"
                elif skill == "electrician":
                    note = f"Install {fake.word()} lighting in the {fake.word()}"
                elif skill == "painter":
                    note = f"Paint the {fake.color_name()} {fake.word()} wall"
                elif skill == "mechanic":
                    note = f"Repair the {fake.word()} in my car"
                elif skill == "mason":
                    note = f"Build a {fake.color_name()} {fake.word()} wall"
                else:
                    note = fake.sentence()

                sr = ServiceRequest(
                    worker_id=worker.id,
                    requester_name=random_name(),
                    date=random_date_within_years(),
                    status=random.choice(STATUS),
                    notes=note
                )
                session.add(sr)
                session.commit()
            except Exception as e:
                session.rollback()
                print(f"Skipping request: {e}")

        # Seed Reviews
        for _ in range(n_reviews):
            try:
                r = Review(
                    worker_id=random.choice(workers).id,
                    rating=random.randint(1, 5),
                    comment=random.choice(REVIEW_COMMENTS)
                )
                session.add(r)
                session.commit()
            except Exception as e:
                session.rollback()
                print(f"Skipping review: {e}")

        print("Database seeded ✅")

    finally:
        session.close()

if __name__ == "__main__":
    seed_data()

from faker import Faker
import random
from lib.models.worker import Worker, SKILLS
from lib.models.service_request import ServiceRequest, STATUS
from lib.models.review import Review
from lib.db.db import Base, engine, SessionLocal

fake = Faker("en_US")

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
                    name=fake.name(),
                    skill=random.choice(SKILLS),
                    phone="07" + str(random.randint(10000000, 99999999)),
                    location=fake.city()
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
                sr = ServiceRequest(
                    worker_id=random.choice(workers).id,
                    requester_name=fake.name(),
                    date=fake.date_this_decade(),
                    status=random.choice(STATUS),
                    notes=fake.sentence()
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
                    comment=fake.sentence(nb_words=10)
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

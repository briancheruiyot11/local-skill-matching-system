from faker import Faker
import random
from lib.models.worker import Worker, SKILLS
from lib.db.db import Base, engine

fake = Faker("en_US")

def seed_workers(n=30):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    for _ in range(n):
        try:
            Worker.create(
                name=fake.name(),
                skill=random.choice(SKILLS),
                phone="07" + str(random.randint(10000000, 99999999)),
                location=fake.city()
            )
        except Exception as e:
            print(f"Skipping duplicate/invalid: {e}")

if __name__ == "__main__":
    seed_workers(30)
    print("Workers seeded.")

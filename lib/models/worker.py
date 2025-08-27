from sqlalchemy import Column, Integer, String, DateTime, func
from lib.db.db import Base, SessionLocal
from lib.helpers import normalize_phone, validate_skill

SKILLS = ("Plumber", "Electrician", "Carpenter", "Mechanic", "Painter", "Mason")

class Worker(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    skill = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    location = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # CRUD + Find Methods

    @classmethod
    def create(cls, name, skill, phone, location):
        session = SessionLocal()
        try:
            worker = cls(
                name=name,
                skill=validate_skill(skill, SKILLS),
                phone=normalize_phone(phone),
                location=location,
            )
            session.add(worker)
            session.commit()
            session.refresh(worker)
            print(f"✅ Worker '{worker.name}' created with ID {worker.id}")
            return worker
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @classmethod
    def delete(cls, id):
        session = SessionLocal()
        worker = session.get(cls, id)
        if not worker:
            session.close()
            return False
        session.delete(worker)
        session.commit()
        session.close()
        return True

    @classmethod
    def get_all(cls):
        session = SessionLocal()
        workers = session.query(cls).all()
        session.close()
        return workers

    @classmethod
    def get_by_id(cls, id):
        session = SessionLocal()
        worker = session.get(cls, id)
        session.close()
        return worker

    @classmethod
    def find_by_name(cls, substring):
        session = SessionLocal()
        results = session.query(cls).filter(cls.name.ilike(f"%{substring}%")).all()
        session.close()
        return results

    @classmethod
    def find_by_skill(cls, skill):
        session = SessionLocal()
        results = session.query(cls).filter(cls.skill == skill).all()
        session.close()
        return results

    @classmethod
    def find_by_location(cls, substring):
        session = SessionLocal()
        results = session.query(cls).filter(cls.location.ilike(f"%{substring}%")).all()
        session.close()
        return results

    # Update worker details
    def update(self, name=None, skill=None, phone=None, location=None):
        session = SessionLocal()
        try:
            worker = session.get(Worker, self.id)
            if name:
                worker.name = name
            if skill:
                worker.skill = validate_skill(skill, SKILLS)
            if phone:
                worker.phone = normalize_phone(phone)
            if location:
                worker.location = location
            session.commit()
            session.refresh(worker)
            print(f"✅ Worker {worker.id} updated successfully.")
            return worker
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

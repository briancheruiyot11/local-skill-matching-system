from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from lib.db.db import Base, SessionLocal
from datetime import datetime, date  

STATUS = ("Pending", "In Progress", "Completed", "Cancelled")

class ServiceRequest(Base):
    __tablename__ = "service_requests"

    id = Column(Integer, primary_key=True)
    worker_id = Column(Integer, ForeignKey("workers.id"))
    requester_name = Column(String, nullable=False)
    date = Column(Date, nullable=False, default=date.today)  
    status = Column(String, nullable=False, default="Pending")
    notes = Column(String)

    worker = relationship("Worker", backref="service_requests")

    @classmethod
    def create(cls, **kwargs):
        session = SessionLocal()
        try:
            # Handle date input
            date_value = kwargs.get("date", date.today())
            if isinstance(date_value, str):
                date_value = datetime.strptime(date_value, "%Y-%m-%d").date()

            req = cls(
                worker_id=kwargs["worker_id"],
                requester_name=kwargs["requester_name"],
                date=date_value,
                status=kwargs.get("status", "Pending"),
                notes=kwargs.get("notes", "")
            )

            if req.status not in STATUS:
                raise ValueError(f"Status must be one of {STATUS}")

            session.add(req)
            session.commit()
            session.refresh(req)   
            return req
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @classmethod
    def get_all(cls):
        session = SessionLocal()
        data = session.query(cls).all()
        session.close()
        return data

    @classmethod
    def get_by_id(cls, id):
        session = SessionLocal()
        obj = session.query(cls).get(id)
        session.close()
        return obj

    @classmethod
    def delete(cls, id):
        session = SessionLocal()
        obj = session.query(cls).get(id)
        if not obj:
            session.close()
            return False
        session.delete(obj)
        session.commit()
        session.close()
        return True

    @classmethod
    def find_by_status(cls, status):
        session = SessionLocal()
        results = session.query(cls).filter(cls.status == status).all()
        session.close()
        return results

    def update_status(self, new_status):
        if new_status not in STATUS:
            raise ValueError(f"Status must be one of {STATUS}")
        session = SessionLocal()
        self.status = new_status
        session.add(self)
        session.commit()
        session.close()

    @classmethod
    def for_worker(cls, worker_id):
        """Return all service requests for a given worker"""
        session = SessionLocal()
        results = session.query(cls).filter(cls.worker_id == worker_id).all()
        session.close()
        return results

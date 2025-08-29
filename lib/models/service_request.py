from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, joinedload
from lib.db.db import Base, SessionLocal
from lib.helpers import display_table
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

# CRUD + Find Methods

    @classmethod
    def create(cls, **kwargs):
        session = SessionLocal()
        try:
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
        session = SessionLocal()
        results = session.query(cls).filter(cls.worker_id == worker_id).all()
        session.close()
        return results

    @classmethod
    def list_by_worker(cls, worker_id):
        requests = cls.for_worker(worker_id)
        if requests:
            data = [(r.id, r.requester_name, r.date, r.status, r.notes) for r in requests]
            display_table(data, ["ID", "Requester", "Date", "Status", "Notes"])
        else:
            print(f"❌ No service requests found for worker ID {worker_id}")

    @classmethod
    def list_all(cls):
        requests = cls.get_all()
        if requests:
            data = [(r.id, r.worker_id, r.requester_name, r.date, r.status, r.notes) for r in requests]
            display_table(data, ["ID", "Worker ID", "Requester", "Date", "Status", "Notes"])
        else:
            print("❌ No service requests found.")

    @classmethod
    def find_by_id(cls, id):
        req = cls.get_by_id(id)
        if req:
            data = [(req.id, req.worker_id, req.requester_name, req.date, req.status, req.notes)]
            display_table(data, ["ID", "Worker ID", "Requester", "Date", "Status", "Notes"])
        else:
            print(f"❌ Service Request with ID {id} not found.")

    @classmethod
    def view_worker(cls, request_id):
        """Display the worker assigned to a given service request using a live session"""
        session = SessionLocal()
        req = session.query(cls).options(joinedload(cls.worker)).filter(cls.id == request_id).first()
        if req and req.worker:
            worker = req.worker
            data = [(worker.id, worker.name, worker.skill, worker.phone, worker.location)]
            display_table(data, ["ID", "Name", "Skill", "Phone", "Location"])
        elif req:
            print(f"❌ Service Request {request_id} has no assigned worker.")
        else:
            print(f"❌ Service Request with ID {request_id} not found.")
        session.close()

    def update(self, requester_name=None, notes=None, status=None):
        """Update the service request fields"""
        session = SessionLocal()
        try:
            if requester_name is not None:
                self.requester_name = requester_name
            if notes is not None:
                self.notes = notes
            if status is not None:
                if status not in STATUS:
                    raise ValueError(f"Status must be one of {STATUS}")
                self.status = status
            session.add(self)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

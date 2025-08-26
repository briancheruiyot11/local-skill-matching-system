from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from lib.db.db import Base, SessionLocal

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    worker_id = Column(Integer, ForeignKey("workers.id"))
    rating = Column(Integer, nullable=False)
    comment = Column(String(500))
    created_at = Column(DateTime, server_default=func.now())

    worker = relationship("Worker", backref="reviews")

    @classmethod
    def create(cls, **kwargs):
        session = SessionLocal()
        try:
            rating = kwargs["rating"]
            if rating < 1 or rating > 5:
                raise ValueError("Rating must be between 1 and 5")
            review = cls(
                worker_id=kwargs["worker_id"],
                rating=rating,
                comment=kwargs.get("comment", "")
            )
            session.add(review)
            session.commit()
            session.refresh(review)  
            return review
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @classmethod
    def get_all(cls):
        session = SessionLocal()
        reviews = session.query(cls).all()
        session.close()
        return reviews

    @classmethod
    def get_by_id(cls, id):
        session = SessionLocal()
        review = session.query(cls).get(id)
        session.close()
        return review

    @classmethod
    def delete(cls, id):
        session = SessionLocal()
        review = session.query(cls).get(id)
        if not review:
            session.close()
            return False
        session.delete(review)
        session.commit()
        session.close()
        return True

    @classmethod
    def for_worker(cls, worker_id):
        session = SessionLocal()
        results = session.query(cls).filter(cls.worker_id == worker_id).all()
        session.close()
        return results

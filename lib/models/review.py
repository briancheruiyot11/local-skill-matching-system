from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship, joinedload
from lib.db.db import Base, SessionLocal
from lib.helpers import display_table

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
    def list_all(cls):
        """List all reviews in a table"""
        reviews = cls.get_all()
        if reviews:
            data = [(r.id, r.worker_id, r.rating, r.comment, r.created_at) for r in reviews]
            display_table(data, ["ID", "Worker ID", "Rating", "Comment", "Created At"])
        else:
            print("❌ No reviews found.")

    @classmethod
    def get_by_id(cls, id):
        session = SessionLocal()
        review = session.query(cls).get(id)
        session.close()
        return review

    @classmethod
    def find_by_id(cls, id):
        """Find a review by ID and display it"""
        review = cls.get_by_id(id)
        if review:
            data = [(review.id, review.worker_id, review.rating, review.comment, review.created_at)]
            display_table(data, ["ID", "Worker ID", "Rating", "Comment", "Created At"])
        else:
            print(f"❌ Review with ID {id} not found.")

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

    @classmethod
    def list_by_worker(cls, worker_id):
        """List all reviews for a given worker and display in table"""
        reviews = cls.for_worker(worker_id)
        if reviews:
            data = [(r.id, r.rating, r.comment, r.created_at) for r in reviews]
            display_table(data, ["ID", "Rating", "Comment", "Created At"])
        else:
            print(f"❌ No reviews found for worker ID {worker_id}")

    @classmethod
    def view_worker(cls, review_id):
        """Display the worker assigned to a review"""
        session = SessionLocal()
        review = session.query(cls).options(joinedload(cls.worker)).filter(cls.id == review_id).first()
        if review and review.worker:
            worker = review.worker
            data = [(worker.id, worker.name, worker.skill, worker.phone, worker.location)]
            display_table(data, ["ID", "Name", "Skill", "Phone", "Location"])
        elif review:
            print(f"❌ Review {review_id} has no assigned worker.")
        else:
            print(f"❌ Review with ID {review_id} not found.")
        session.close()

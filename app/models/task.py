from app.extensions import db
from datetime import datetime, date
from app.models.user import User  #  Add this line

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending, in-progress, completed
    due_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    is_active = db.Column(db.Boolean, default=True, nullable=False)  # soft delete

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship("User", back_populates="tasks")

    __table_args__ = (
        db.Index('ix_task_user_id', 'user_id'),  # index for performance
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "user_id": self.user_id,
            "is_active": self.is_active
        }


# New: TaskLogger model
class TaskLogger(db.Model):
    __tablename__ = 'task_logger'

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    logged_date = db.Column(db.Date, default=date.today, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship("User", lazy='joined')

    def to_dict(self):
        return {
            "id": self.id,
            "task_id": self.task_id,
            "title": self.title,
            "status": self.status,
            "logged_date": self.logged_date.isoformat(),
            "user_id": self.user_id,
        }

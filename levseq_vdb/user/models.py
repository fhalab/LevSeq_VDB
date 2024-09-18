# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.dialects.postgresql import JSONB

from levseq_vdb.database import Column, PkModel, db, reference_col, relationship
from levseq_vdb.extensions import bcrypt


class Role(PkModel):
    """A role for a user."""

    __tablename__ = "roles"
    name = Column(db.String(80), unique=True, nullable=False)
    user_id = reference_col("users", nullable=True)
    user = relationship("User", backref="roles")

    def __init__(self, name, **kwargs):
        """Create instance."""
        super().__init__(name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Role({self.name})>"

class Group(PkModel):
    __tablename__ = 'groups'
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String)


# Define the Experiment model
class Experiment(PkModel):
    __tablename__ = 'experiments'

    id = db.Column(db.Integer, primary_key=True)
    user_created = db.Column(db.Integer, db.ForeignKey('users.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    batch_id = db.Column(db.Integer, db.ForeignKey('batch.id'))

    name = db.Column(db.String(255))
    meta = db.Column(db.String(10000))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    date_last_edited = db.Column(db.TIMESTAMP)

    # Ensure to put in the group relationships
    group = relationship("Group")

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Name({self.name!r})>"


class Data(PkModel):
    __tablename__ = 'data'

    id = db.Column(db.Integer, primary_key=True)
    user_created = db.Column(db.Integer, db.ForeignKey('users.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    experiment_id = db.Column(db.Integer, db.ForeignKey('experiments.id'))
    type = db.Column(db.String(255))
    data = db.Column(db.String(1000))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    date_edited = db.Column(db.TIMESTAMP)


class Batch(PkModel):
    """ This is basically a batch of experiments, for example, associated with a specific enzyme family and class."""
    __tablename__ = 'batch'

    id = db.Column(db.Integer, primary_key=True)
    user_created = db.Column(db.Integer, db.ForeignKey('users.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    experiment_id = db.Column(db.Integer, db.ForeignKey('experiments.id'))
    name = db.Column(db.String(255))
    type = db.Column(db.String(255))
    data = db.Column(db.String(10000))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    date_edited = db.Column(db.TIMESTAMP)


class User(UserMixin, PkModel):
    """A user of the app."""

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    _password = Column("password", db.LargeBinary(128), nullable=True)
    created_at = Column(
        db.DateTime, nullable=False, default=dt.datetime.now(dt.timezone.utc)
    )
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)

    @hybrid_property
    def password(self):
        """Hashed password."""
        return self._password

    @password.setter
    def password(self, value):
        """Set password."""
        self._password = bcrypt.generate_password_hash(value)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self._password, value)

    @property
    def full_name(self):
        """Full username."""
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<User({self.username!r})>"

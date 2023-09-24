from extensions import db
from datetime import datetime

'''
@COMPLETED_1 
Data Modeling
CRITERIA:
- Architect relational database models in Python.

MEETS SPECIFICATIONS:
- Use of correct data types for fields
- Use of primary and optional foreign key ids
'''


class ActorMovieAssociation(db.Model):
    __tablename__ = 'actor_movie_association'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    actor_id = db.Column(db.Integer, db.ForeignKey('Actor.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('Movie.id'), nullable=False)
    actor = db.relationship('Actor', back_populates='movie_associations')
    movie = db.relationship('Movie', back_populates='actor_associations')


class Actor(db.Model):
    __tablename__ = 'Actor'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.String(10), nullable=False)

    is_time_available = db.Column(db.Boolean, default=False)

    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now,
                          onupdate=datetime.now)

    # many-to-many relationship
    movie_associations = db.relationship(
        'ActorMovieAssociation', back_populates='actor'
    )

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, value in data.items():
            setattr(self, key, value)


class Movie(db.Model):
    __tablename__ = 'Movie'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120), nullable=False)
    date = db.Column(db.Date, nullable=False)

    # many-to-many relationship
    actor_associations = db.relationship(
        'ActorMovieAssociation', back_populates='movie'
    )

    def save(self):
        db.session.add(self)
        db.session.commit()

from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from config import db 

class Episode(db.Model, SerializerMixin):
    __tablename__ = 'episodes'
    serialize_rules = ('-appearances.guest.appearances',)

    id = db.Column(db.Integer, primary_key= True)
    date = db.Column(db.String, nullable= False)
    number = db.Column(db.Integer, nullable=False)

    appearances = db.relationship('Appearance', back_populates= 'episode', cascade = 'all, delete-orphan')



class Guest(db.Model, SerializerMixin):
    __tablename__ = 'guests'
    serialize_rules =('-appearances.episode.appearances',)

    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String, nullable = False)
    occupation = db.Column(db.String, nullable= False)

    appearances = db.relationship('Appearance', back_populates= 'guest', cascade = 'all, delete-orphan')




class Appearance(db.Model, SerializerMixin):
    __tablename__ = 'appearances'
    serialize_rules = ('guest', 'episode')

    id = db.Column(db.Integer, primary_key= True)
    rating = db.Column(db.Integer, nullable=False)

    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'), nullable= False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable= False)

    episode = db.relationship("Episode", back_populates = "appearances")
    guest = db.relationship("Guest", back_populates = "appearances")
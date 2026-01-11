from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from config import db 

class Episode(db.Model, SerializerMixin):
    __tablename__ = 'episodes'
    serialize_rules = ('-appearances.episode',)

    id = db.Column(db.Integer, primary_key= True)
    date = db.Column(db.String, nullable= False)
    number = db.Column(db.Integer, nullable=False)

    appearances = db.relationship('Appearance', back_populates= 'episode', cascade = 'all, delete-orphan')

    def to_dict(self, include_appearances=False):
        data = {
            "id": self.id,
            "date": self.date,
            "number": self.number
        }
        if include_appearances:
            data["appearances"] = [a.to_dict() for a in self.appearances]
        return data



class Guest(db.Model, SerializerMixin):
    __tablename__ = 'guests'
    serialize_rules =('-appearances.guest',)

    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String, nullable = False)
    occupation = db.Column(db.String, nullable= False)

    appearances = db.relationship('Appearance', back_populates= 'guest', cascade = 'all, delete-orphan')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "occupation": self.occupation
        }



class Appearance(db.Model, SerializerMixin):
    __tablename__ = 'appearances'
    serialize_rules = ('-guest.appearances', 'episode.appearances')

    id = db.Column(db.Integer, primary_key= True)
    rating = db.Column(db.Integer, nullable=False)

    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'), nullable= False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable= False)

    episode = db.relationship("Episode", back_populates = "appearances")
    guest = db.relationship("Guest", back_populates = "appearances")

   
    @validates('rating')
    def validate_rating(self, key, value):
        if not 1<= value <=5 :
            raise ValueError("Rating must be between 1 and 5")
        return value
    
    def to_dict(self):
        return {
            "id": self.id,
            "episode_id": self.episode_id,
            "guest_id": self.guest_id,
            "rating": self.rating,
            "guest": self.guest.to_dict()
        }
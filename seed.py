from app import app
from config import db
from model import Episode, Guest, Appearance
from faker import Faker
import random

fake = Faker()

with app.app_context():

    # Clear existing data
    Appearance.query.delete()
    Episode.query.delete()
    Guest.query.delete()

    db.session.commit()

    # Generate Episodes
    episodes = []
    for i in range(1, 10):  # 10 episodes
        ep = Episode(
            date=fake.date(pattern="%m/%d/%y"),
            number=i
        )
        episodes.append(ep)
    db.session.add_all(episodes)
    db.session.commit()

    # Generate Guests
    guests = []
    for _ in range(10):  # 10 guests
        g = Guest(
            name=fake.name(),
            occupation=fake.job()
        )
        guests.append(g)
    db.session.add_all(guests)
    db.session.commit()

    # Generate Appearances
    appearances = []
    for _ in range(20):  # 20 appearances
        ep = random.choice(episodes)
        g = random.choice(guests)
        rating = random.randint(1, 5)
        a = Appearance(
            episode_id=ep.id,
            guest_id=g.id,
            rating=rating
        )
        appearances.append(a)

    db.session.add_all(appearances)
    db.session.commit()

    print("🌱 Seeded 10 episodes, 10 guests, 20 appearances!")

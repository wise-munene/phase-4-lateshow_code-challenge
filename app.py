from flask import request
from flask_restful import Resource
from model import Guest, Appearance, Episode
from config import db, api, app


class Episodes(Resource):
    def get(self):
        return [episodes.to_dict() for episodes in Episode.query.all()],200

class EpisodesByID(Resource):
    def get(self, id):
        episode = Episode.query.get(id)
        if not episode:
            return{"error":"Episode not found"},404
        return{
             "id": episode.id,
            "date": episode.date,
            "number": episode.number,
            "appearances": [
                {"id": a.id, "episode_id": a.episode_id, "guest_id": a.guest_id, "rating": a.rating,
                    "guest": { "id": a.guest.id, "name": a.guest.name, "occupation": a.guest.occupation
                    } } for a in episode.appearances]}, 200

    def delete(self, id):
        episode = Episode.query.get(id)
        if not episode:
            return {"error": "Episode not found"}, 404
        db.session.delete(episode)
        db.session.commit()
        return {"message": f"Episode {id} deleted successfully"}, 200
        
class Guests(Resource):
    def get(self):
        return [guest.to_dict() for guest in Guest.query.all()],200

class Appearances(Resource):
    def post(self):
        data = request.get_json()
        
        rating = data.get("rating")
        episode_id = data.get("episode_id")
        guest_id = data.get("guest_id")

        if not rating or not (1 <= rating <= 5) or not episode_id or not guest_id:
            return {"errors": ["validation errors"]}, 400

        episode = Episode.query.get(episode_id)
        guest = Guest.query.get(guest_id)

        if not episode or not guest:
            return {"errors": ["validation errors"]}, 400

        
        appearance = Appearance(rating=rating, episode_id=episode.id, guest_id=guest.id)
        db.session.add(appearance)
        db.session.commit()

        response = {
            "id": appearance.id,
            "rating": appearance.rating,
            "guest_id": appearance.guest_id,
            "episode_id": appearance.episode_id,
            "episode": {"id": episode.id, "date": episode.date, "number": episode.number},
            "guest": {"id": guest.id, "name": guest.name, "occupation": guest.occupation}
        }
        return response, 201
    
           
api.add_resource(Episodes, '/episodes')
api.add_resource(EpisodesByID, '/episodes/<int:id>')
api.add_resource(Guests, '/guests')
api.add_resource(Appearances, '/appearances')


if __name__ == '__main__':
    app.run( debug=True)
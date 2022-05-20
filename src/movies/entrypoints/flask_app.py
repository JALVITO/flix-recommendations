from email.policy import default
from flask import Flask, request, jsonify
import json
from storage import Storage
from movies.utils.invalid_api_usage import InvalidAPIUsage
from recommendations.recommender_factory import RecommenderFactory, AlgorithmType
from movies.movie_fetcher import get_movies

app = Flask(__name__)
storage = Storage()

# Clean Movie DB and re-populate
movies = get_movies()
storage.clean_movies()
for movie in movies:
    storage.store_movie(**movie)

def process_required_arg(name):
    value = request.args.get(name)
    if value is None:
        raise InvalidAPIUsage(f'No {name} provided!', status_code=400)
    return value

@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(e):
    return jsonify(e.to_dict()), e.status_code

# Get Recommendations endpoint
@app.route('/get_recommendations', methods=['GET'])
def get_recommendations():
    username = process_required_arg('username')
    descending = request.args.get('descending', default=True, type=json.loads)

    user = storage.get_user(username)
    if user is None:
        raise InvalidAPIUsage("User cannot be found!", status_code=404)

    preferences = [int(p) for p in user.preferences.split(',')]
    algorithm = RecommenderFactory.create_recommender(AlgorithmType.CATEGORY_PRODUCT)
    key = algorithm.generate_preference_key(preferences)
    movies = storage.get_movies(key, descending)

    return {'movies': [m.as_dict() for m in movies]}, 200

# Create user endpoint
@app.route('/create_user', methods=['POST'])
def create_user():
    username = process_required_arg('username')
    email = process_required_arg('email')

    preferences = request.args.getlist('preferences')
    if preferences is None:
        raise InvalidAPIUsage("No preferences provided!", status_code=400)
    if len(preferences) != 3:
        raise InvalidAPIUsage("3 preferences must be selected!", status_code=400)

    str_preferences = ','.join(preferences)
    user = storage.store_user(username, email, str_preferences)

    if user is None:
        raise InvalidAPIUsage("User already exists!", status_code=409)

    return {'message': 'User created succesfully!', 'user': user.as_dict()}, 200

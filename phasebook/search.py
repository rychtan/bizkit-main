from flask import Blueprint, request, jsonify

from .data.search_data import USERS


bp = Blueprint("search", __name__, url_prefix="/search")


@bp.route("")
def search():
    id = request.args.get('id')
    name = request.args.get('name')
    age = request.args.get('age')
    occupation = request.args.get('occupation')


    search_results = search_users(USERS, id=id, name=name, age=age, occupation=occupation)

#    search_results = search_users(USERS, **request.args.to_dict())

    return jsonify(search_results), 200


def search_users(users, id=None, name=None, age=None, occupation=None):
    age = int(age) if age is not None else None
    results = []
    print(id,name,age,occupation)

    for user in users:
        score = 0
        if id is not None and user['id'] == id:
            score += 4
        if name is not None and name.lower() in user['name'].lower():
            score += 3
        if age is not None and abs(user['age'] - age) <= 1:
            score += 2
        if occupation is not None and occupation.lower() in user['occupation'].lower():
            score += 1
        if score > 0:
            user['score'] = score
            results.append(user)

    results.sort(key=lambda x: x['score'], reverse=True)

    for user in results:
        del user['score']
    return results


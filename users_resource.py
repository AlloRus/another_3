from data import db_session
from data.users import User
from flask_restful import abort, Resource
from flask import jsonify
from .reqparse import parser

def abort_if_users_not_found(users_id):
    sess = db_session.create_session()
    users = sess.query(User).get(users_id)
    if not users:
        abort(404, message=f"User {users_id} not found")


class UsersResource(Resource):
    def get(self, users_id):
        abort_if_users_not_found(users_id)
        sess = db_session.create_session()
        users = sess.query(User).get(users_id)
        return jsonify(
        {
            'users': users.to_dict(only=(
                'id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'hashed_password', 'modified_date'))
        }
    )

    def delete(self, users_id):
        abort_if_users_not_found(users_id)
        db_sess = db_session.create_session()
        users = db_sess.query(User).get(users_id)
        db_sess.delete(users)
        db_sess.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        users = db_sess.query(User).all()
        return jsonify(
            {
                'users':
                    [item.to_dict(only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'hashed_password', 'modified_date')) 
                    for item in users]
            }
        )

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        users = User(
            id=args['id'],
            name=args['name'],
            about=args['about'],
            email=args['email']
        )
        db_sess.add(users)
        db_sess.commit()
        return jsonify({'success': 'OK'})

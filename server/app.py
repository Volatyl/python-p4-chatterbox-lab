from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)


@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.all()

        msgs = []
        for msg in messages:
            msg_dict = msg.to_dict()
            msgs.append(msg_dict)

        res = make_response(jsonify(msgs), 200)

        return res

    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        body = data.get('body')

        new_msg = Message(username=username, body=body)

        db.session.add(new_msg)
        db.session.commit()

        msg_dict = new_msg.to_dict()

        res = make_response(jsonify(msg_dict), 200)

        return res


@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    msg = Message.query.filter_by(id=id).first()

    if request.method == 'PATCH':
        # data = request.get_json()
        for attr, value in request.json.items():
            setattr(msg, attr, value)

        db.session.commit()

        res_body = msg.to_dict()

        res = make_response(jsonify(res_body), 200)

        return res

    if request.method == 'DELETE':
        db.session.delete(msg)
        db.session.commit()

        res_body = {
            "delete": True,
            "Delete msg": "Message deleted"
        }

        res = make_response(jsonify(res_body), 200)
        return res


if __name__ == '__main__':
    app.run(port=5555)

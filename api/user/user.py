# from flask import Flask, render_template, request
# import os
# from app import app
#
#
# class Login(object):
#     @app.route('/', methods=['GET'])
#     def index(self):
#         return render_template('index.html')
#
#     @app.route('/', methods=['POST'])
#     def index_post(self):
#         # Read the values from the form
#         original_text = request.form['text']
#         target_language = request.form['language']
#
#         # Load the values from .env
#         key = os.environ['KEY']
#         endpoint = os.environ['ENDPOINT']
#         location = os.environ['LOCATION']
#
#         # Indicate that we want to translate and the API version (3.0) and the target language
#         path = '/translate?api-version=3.0'
#         # Add the target language parameter
#         target_language_parameter = '&to=' + target_language
#         # Create the full URL
#         constructed_url = endpoint + path + target_language_parameter
#
#         # Set up the header information, which includes our subscription key
#         headers = {
#             'Ocp-Apim-Subscription-Key': key,
#             'Ocp-Apim-Subscription-Region': location,
#             'Content-type': 'application/json',
#             'X-ClientTraceId': str(uuid.uuid4())
#         }
#
#         # Create the body of the request with the text to be translated
#         body = [{'text': original_text}]
#
#         # Make the call using post
#         translator_request = requests.post(constructed_url, headers=headers, json=body)
#         # Retrieve the JSON response
#         translator_response = translator_request.json()
#         # Retrieve the translation
#         translated_text = translator_response[0]['translations'][0]['text']
#
#         # Call render template, passing the translated text,
#         # original text, and target language to the template
#         return render_template(
#             'results.html',
#             translated_text=translated_text,
#             original_text=original_text,
#             target_language=target_language
#         )
import pymongo
from flask import Blueprint, request, jsonify
from flask.views import MethodView


class UserView(MethodView):
    def __init__(self, db_config=None):
        app = Blueprint('login', __name__, template_folder='user', url_prefix='/api')
        self.app = app
        client = pymongo.MongoClient(db_config)
        self.db = client.Test
        self._init_route()
        self._init_db()

    def _init_db(self):
        self.db.test.create_index([("username", pymongo.DESCENDING)])

    def _init_route(self):
        user_view = UserView.as_view('user_api')
        self.app.add_url_rule('/users', defaults={'user_id': None},
                              view_func=user_view, methods=['GET'])
        self.app.add_url_rule('/users', view_func=user_view, methods=['POST'])
        self.app.add_url_rule('/users/<int:user_id>', view_func=user_view,
                              methods=['GET', 'PUT', 'DELETE'])

    def get(self, user_id):
        """
            account
            ---
            tags:
              - User
            parameters:
              - name: user_id
                in: path
                type: integer
                description: search 條件
            responses:
              0:
                description: Success
              200:
                description: Error
                schema:
                  id: result
                  properties:
                    errcode:
                      type: int
                      description: error code
                      default: 0
                    result:
                      type: dict
                      description: return result
                      default: {'username':'user','password':'pass'}

            """
        if user_id is None:
            users = self.db.user.find(projection={'_id': False})
            result = []
            for user in users:
                result.append(user)
            return jsonify({'result': result})
        else:
            users = self.db.user.find_one({'id': user_id}, projection={'_id': False})
            # 显示一个用户
            return users

    def post(self):
        # 註冊使用者
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        user_id = request.json.get('id', None)
        result_data = self.db.user.insert_one({'username': username, 'password': password,'id': user_id})
        result = {'errcode': 0, 'result': None}
        return jsonify(result)

    def put(self, user_id):

        username = request.json.get('username', None)
        password = request.json.get('password', None)

        result = self.db.user.find_one_and_update({"id": user_id},
                                                  {"$set": {"username": username, "password": password}},
                                                  projection={'_id': False})
        return jsonify(result)

    def delete(self, user_id):
        self.db.user.delete_one({"id": user_id})
        return {'errcode': 0}


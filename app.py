from flask import Flask, jsonify, request
import random
import os
from dotenv import load_dotenv
from api.user.user import UserView
from flasgger import Swagger

# <editor-fold desc="修改env">
ENV = 'test'
if ENV == 'production':
    load_dotenv('.env.production')
elif ENV == 'staging':
    load_dotenv('.env.stage')
load_dotenv('.env')
print(os.environ['name'])
# </editor-fold>

# 優化 debug mode 或是 pycharm 降板至2021.1
app = Flask(__name__, instance_path="/{project_folder_abs_path}/instance")
# app = Flask(__name__)
user = UserView(os.environ['mongo'])
api_handlers = [user]
for handler in api_handlers:
    app.register_blueprint(handler.app)
Swagger(app)


# @app.route('/', methods=['Get'])
# def index():
#     """
#        index
#        Retrieve node list index
#        ---
#        tags:
#          - Node APIs
#        produces: application/json,
#        parameters:
#        - name: name
#          in: path
#          type: str
#          required: true
#        - name: node_id
#          in: path
#          type: str
#          required: true
#        responses:
#          401:
#            description: Unauthorized error
#          200:
#            description: Retrieve node list
#            examples:
#              node-list: [{"id":26},{"id":44}]
#      """
#     return '首頁'

@app.route('/api/<string:language>/', methods=['GET'])
def index(language):
    """
    This is the language awesomeness API
    Call this api passing a language name and get back its features
    ---
    tags:
      - Awesomeness Language API
    parameters:
      - name: language
        in: path
        type: string
        required: true
        description: The language name
      - name: size
        in: query
        type: integer
        description: size of awesomeness
    responses:
      500:
        description: Error The language is not awesome!
      200:
        description: A language with its awesomeness
        schema:
          id: awesome
          properties:
            language:
              type: string
              description: The language name
              default: Lua
            features:
              type: array
              description: The awesomeness list
              items:
                type: string
              default: ["perfect", "simple", "lovely"]

    """

    language = language.lower().strip()
    features = [
        "awesome", "great", "dynamic",
        "simple", "powerful", "amazing",
        "perfect", "beauty", "lovely"
    ]
    size = int(request.args.get('size', 1))
    if language in ['php', 'vb', 'visualbasic', 'actionscript']:
        return "An error occurred, invalid language for awesomeness", 500
    return jsonify(
        language=language,
        features=random.sample(features, size)
    )


if __name__ == '__main__':
    app.run(debug=True)


from flask import Flask
from flask_cors import CORS #comment this on deployment
from flask_restful import Api
from backend.api.UserDBHandler import UserDBHandler, RegisterUser
from backend.api.SearchHandler  import SearchHandler
from backend.UserSessions import CreateToken, Logout, Profile
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

# create Flask server instance
app = Flask(__name__, static_url_path='', static_folder='frontend/public')
# create flask_restful Api instance
api = Api(app)
# create Bcrypt instance for hashing passwords
bcrypt = Bcrypt(app)
# create instance to handle user db interactions
userRecord = UserDBHandler('user', bcrypt)
CORS(app) #comment this on deployment
#initialize JSON Web Token
jwt = JWTManager(app)


#json web token config settings
app.config["JWT_SECRET_KEY"] = "SUPER-SECRET-KEY"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

api.add_resource(SearchHandler, '/flask/search')
api.add_resource(RegisterUser, '/flask/register',resource_class_kwargs={'table':'user', 'bcryptObject': bcrypt})
api.add_resource(CreateToken, '/token', resource_class_kwargs={'jwt': jwt, 'userRecord': userRecord})
api.add_resource(Logout, '/logout', resource_class_kwargs={'jwt': jwt, 'userRecord': userRecord})
api.add_resource(Profile, '/profile', resource_class_kwargs={'jwt': jwt, 'userRecord': userRecord})

from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, \
                                unset_jwt_cookies, jwt_required
from flask_restful import reqparse, Resource
from flask import jsonify



class JWTSession(Resource):
    def __init__(self,jwt, userRecord):
        self.jwt = jwt               # JSON Web Token object
        self.userRecord = userRecord # UserDBHandler object

        
    
# # To be implemented if time
# # class RefreshToken(JWTSession):
# #     @jwt_required(refresh=True)
# #     def post(self):
# #         identity = get_jwt_identity()
# #         access_token = create_access_token(identity=identity)
# #         return jsonify(access_token=access_token)

class CreateToken(JWTSession):
    def __init__(self, jwt, userRecord):
        super().__init__(jwt, userRecord)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()
        if args:
            db_results = self.userRecord.get_user_from_db(args.email)
            password_matches = self.userRecord.bcrypt.check_password_hash(db_results[1], args.password)
            if db_results is None or args.email != db_results[0] or not password_matches:
                response = {"msg": "Wrong email or password"}, 401
            else:
                access_token = create_access_token(identity=args.email)
                response = {"access_token": access_token}
        else:
            response = {"msg": "Bad request"}, 400
        print(response)
        return response


class Logout(JWTSession):
    def __init__(self,jwt,userRecord):
        super().__init__(jwt,userRecord)


    @jwt_required()
    def get(self):
        response = jsonify({"msg": "logout successful"})
        unset_jwt_cookies(response)
        return response


# return user profile data to the requester
class Profile(JWTSession):
    def __init__(self, jwt, userRecord):
        super().__init__(jwt, userRecord)

    @jwt_required()
    def post(self):
        response_body = {   "name": "test",
                            "about": "test"
                        }
        return response_body

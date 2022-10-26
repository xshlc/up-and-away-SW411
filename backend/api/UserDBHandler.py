from backend.Record import Record
from flask_restful import reqparse, Resource




class UserDBHandler(Resource):
    def __init__(self, table, bcryptObject):
        self.tableRecord = Record(table)
        self.bcrypt = bcryptObject

    def get_user_from_db(self,emailaddress):
        self.tableRecord.addQuery("email", emailaddress)
        self.tableRecord.query()
        try:
            record = next(self.tableRecord.results())
        except StopIteration:
            return None
        return [record['email'],record['userpassword']]


class RegisterUser(UserDBHandler):
    def __init__(self,table,bcryptObject):
        super().__init__(table,bcryptObject)
    # Create new user
    def post(self):
        #Retrieve post content body
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()
        # hash password and store to db
        if args:
            hashed_password = self.bcrypt.generate_password_hash(args.password).decode('utf-8')
            self.tableRecord.insert(f"{args.name},{args.email},{hashed_password}")
            self.tableRecord.commit()

            #debug print
            self.tableRecord.query()
            for row in self.tableRecord.results():
                print(row)
            #end debug print
            # success message returned to user
            message = "Message"
        else:
            # failure message returned to user
            message = "No Message"
        return message










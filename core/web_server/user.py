import psycopg2
import jwt
import datetime
from system_info import SystemInfo

class User:
    """ User Model for storing user related details """
    __tablename__ = "users"
    BCRYPT_LOG_ROUNDS = 4
    SECRET_KEY = "\xf9'\xe4p(\xa9\x12\x1a!\x94\x8d\x1c\x99l\xc7\xb7e\xc7c\x86\x02MJ\xa0"

    def __init__(self, name, password):
        self.name = name
        self.password = password

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                User.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, User.SECRET_KEY)
            return 200
        except jwt.ExpiredSignatureError:
            return 401
        except jwt.InvalidTokenError:
            return 402

    @staticmethod
    def query(name, password):
        conn = psycopg2.connect(host=SystemInfo.postgres_ip,
                                port=SystemInfo.postgres_port,
                                database=SystemInfo.postgres_db,
                                user=SystemInfo.postgres_user,
                                password=SystemInfo.postgres_password)
        cur = conn.cursor()
        cur.execute("select * from utente where nome = %s and password = %s", (name, password))
        result = cur.fetchone()
        if result:
            return User(result[0], result[1])
        else:
            return None

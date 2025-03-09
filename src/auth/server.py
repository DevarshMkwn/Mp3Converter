import jwt, datetime, os
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from dotenv import load_dotenv

load_dotenv()

server = Flask(__name__)

# Configure MySQL
server.config["MYSQL_USER"] = os.environ.get('MYSQL_USER')
server.config["MYSQL_PASSWORD"] = os.environ.get('MYSQL_PASSWORD')
server.config["MYSQL_DB"] = os.environ.get('MYSQL_DB')
server.config["MYSQL_PORT"] = int(os.environ.get('MYSQL_PORT', 3306))
server.config["MYSQL_HOST"] = os.environ.get('MYSQL_HOST')

# Initialize MySQL
mysql = MySQL(server)

@server.route('/')
def index():
    return 'MySQL configuration loaded successfully!'

@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "missing credentials", 401
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT email, password FROM user WHERE email = %s", (auth.username,))
    user = cur.fetchone()
    cur.close()

    if user and user[1] == auth.password:  # user[1] is password
        token = createJwtToken(auth.username, True)
        return jsonify({'token': token})
    return "invalid credentials", 401

def createJwtToken(username, authz):
    payload = {
        'username': username,
        'admin': authz,
        'exp': datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1),
        'iat': datetime.datetime.now(tz=datetime.timezone.utc)
    }
    token = jwt.encode(payload, os.environ.get('JWT_SECRET'), algorithm='HS256')
    return token

@server.route("/validate", methods=["POST"])
def validate():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return "missing token", 401

    parts = auth_header.split()
    if parts[0].lower() != 'bearer' or len(parts) != 2:
        return "invalid token type", 401
    
    token = parts[1]

    try:
        payload = jwt.decode(token, os.environ.get("JWT_SECRET"), algorithms=['HS256'])
        return jsonify({'username': payload['username'], 'admin': payload['admin']})
    except jwt.ExpiredSignatureError:
        return "token expired", 401
    except jwt.InvalidTokenError:
        return "invalid token", 401

# Create the user table if it doesn't exist
def init_db():
    cur = mysql.connection.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(120) UNIQUE NOT NULL,
            password VARCHAR(120) NOT NULL
        )
    """)
    mysql.connection.commit()
    cur.close()

if __name__ == '__main__':
    # with server.app_context():
    #     init_db()  # Initialize database tables
    server.run("0.0.0.0", 5000)
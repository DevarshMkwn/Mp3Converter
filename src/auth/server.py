import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL
from dotenv import load_dotenv

load_dotenv()

server = Flask(__name__)
mysql = MySQL(server)

# Access MySQL-related environment variables
server.config["MYSQL_USER"] = os.getenv('MYSQL_USER')
server.config["MYSQL_PASSWORD"] = os.getenv('MYSQL_PASSWORD')
server.config["MYSQL_DB"] = os.getenv('MYSQL_DB')
server.config["MYSQL_PORT"] = os.getenv('MYSQL_PORT')


@server.route('/')
def index():
    return 'MySQL configuration loaded successfully!'

@server.route("/login",methods=["POST"])
def login():


if __name__ == '__main__':
    server.run(debug=True)
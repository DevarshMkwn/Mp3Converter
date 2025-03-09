import os, gridfs, pika, json
from flask import Flask, request
from flask_pymongo import PyMongo
from auth_svc import access
from storage import utils
from auth import validate

server = Flask(__name__)
server.config["MONGO_URI"] = "mongodb://host.minikube.internal:27017/videos"

mongo = PyMongo(server)
fs = gridfs.GridFS(mongo.db)

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()

@server.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)
    if err:
        return err 
    else:
        return token

@server.route("/upload", methods=["POST"])
def upload():
    access, err = validate.token(request)
    access = json.loads(access)

    if access["admin"]:
        if len(request.files) > 1 or len(request.files) < 1:
            return "Only 1 file required!", 400
        for _, file in request.files.items():
            err = utils.upload_file(file, fs, channel, access)
    
@server.route("/download",methods=["GET"])
def download():
    pass

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)
from flask import Flask, jsonify, request
from pycocks.cocks.cocks import CocksPKG, Cocks
from gmpy2 import mpz
import pickle
import json
import sys
import os
import datetime

args = sys.argv

cocks_pkg = CocksPKG()  # Optional param.: bit size (default = 2048)
cocks = Cocks(cocks_pkg.n)  # Must use same public modulus, n, from cocks_pkg
app = Flask(__name__)

UserDic = {}

BASE_DIR = os.getcwd()
MESSAGE_DIR = BASE_DIR + "/data/message"


@app.route("/users", methods=["POST"])
def createUser():
    id = request.get_json()["id"]
    r, a = cocks_pkg.extract(id)
    res = {"id": id, "private_key": int(r), "public_key": int(a)}
    UserDic[id] = {"private_key": int(r), "public_key": int(a)}
    return jsonify(res)


@app.route("/users", methods=["GET"])
def showUsers():
    return jsonify(UserDic)


@app.route("/message/encrypt", methods=["POST"])
def createMessage():
    public_key = request.get_json()["public_key"]
    message = request.get_json()["message"]
    c = encrypt(message, int(public_key))

    dt_now = datetime.datetime.now()
    filename = "mes" + dt_now.strftime("%H%M%S")
    with open(MESSAGE_DIR + "/" + filename, "wb") as binfile:
        pickle.dump(c, binfile)

    return "saved as " + filename


@app.route("/message/decrypt", methods=["POST"])
def decryptMessage():
    public_key = request.get_json()["public_key"]
    private_key = request.get_json()["private_key"]
    crypto_message_file = request.get_json()["crypto_file"]
    with open(MESSAGE_DIR + "/" + crypto_message_file, "rb") as binfile:
        crypto_message = pickle.load(binfile)
    ptext = decrypt(crypto_message, private_key, public_key)

    return ptext


#######################################


def encrypt(p, a):
    mesbin = p.encode("utf-8")
    c = cocks.encrypt(mesbin, mpz(a))
    return c


def decrypt(c, r, a):
    original_message = cocks.decrypt(c, r, a)
    return original_message.decode("utf-8")


def server_main():
    app.run(debug=False, host="0.0.0.0", port=12300)


if __name__ == "__main__":
    print("server start")
    server_main()

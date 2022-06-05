from flask import Flask, jsonify, request
from pycocks.cocks.cocks import CocksPKG, Cocks
import pickle

cocks_pkg = CocksPKG()  # Optional param.: bit size (default = 2048)
cocks = Cocks(cocks_pkg.n)  # Must use same public modulus, n, from cocks_pkg
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World"


@app.route("/users", methods=["POST"])
def index():
    id = request.get_json()["id"]
    r, a = cocks_pkg.extract(id)
    res = {"id": id, "private_key": int(r), "public_key": int(a)}
    return jsonify(res)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=12300)

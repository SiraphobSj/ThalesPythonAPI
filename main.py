from flask import Flask, request, jsonify
import logging
import json

app = Flask(__name__)

logging.basicConfig(filename="KLDsim.log", 
                    format='%(asctime)s.%(msecs)03d %(name)-12s %(levelname)-8s %(message)s', 
                    level=logging.DEBUG)
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s', 
                              "%H:%M:%S")
console.setFormatter(formatter)
logging.getLogger().addHandler(console)

@app.route("/get-user/<user_id>")
def get_user(user_id):
    user_data = {
        "user_id": user_id,
        "name": "Siraphob Jet",
        "email": "siraphobjet@example.com"
    }

    extra =  request.args.get("extra")
    if extra:
        user_data["extra"] = extra

    logging.debug(f"[GET] get-user called, user_id={user_id}, extra={extra}")

    return jsonify(user_data), 200

@app.route("/create-user", methods=["POST"])
def create_user():
    data = request.get_json()
    logging.debug(f"[POST] create-user called")
    return jsonify(data), 201

@app.route("/KLDsim", methods=["POST"])
def kldsim_post():
    reqData = request.get_json()

    with open("APIresponse.json", 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    with open('APIresponse.json', 'w') as f:
        data["requester"] = reqData["username"]
        seq = data["seq"]
        data["seq"] = seq + 1
        json.dump(data, f, indent=4)

    logging.debug(f"[POST] KLDsim called, user={data["requester"]}, seq={seq}")

    return jsonify(data), 201

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)

# logging.debug("DEBUG")
# logging.info("INFO")
# logging.warning("WARNING")
# logging.error("ERROR")
# logging.critical("CRITICAL")
from flask import Flask, request, jsonify, make_response
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

@app.route("/KLDsim/json", methods=["POST"])
def kldsim_post():
    reqData = request.get_json()

    with open("APIresponse.json", 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    with open('APIresponse.json', 'w') as f:
        data["requester"] = reqData["username"]
        seq = data["seq"]
        data["seq"] = seq + 1
        json.dump(data, f, indent=4)

    logging.debug(f"[POST] KLDsim/json called, user={data["requester"]}, seq={seq}")

    return jsonify(data), 201

@app.route("/KLDsim/rsp", methods=["POST"])
def kldsim_rsp():
    reqData = request.get_json()
    logging.debug(f"[POST] KLDsim/rsp called, user={reqData["username"]}")

    response = make_response("mQIwMFAPMVExYjJjM2QtNGU1ZjZnWBhBQUFBQUFBQUFBRDhEQzk3NEFEMjNFQUFRB1BUTy1TS0lSB1N1cHBvcnRTCjAxMjM0NTY3ODlUEDYzMTAwMDE0MDk5ODUxMDFVAlNFVgMyMDJZEDAzRDhEQzk3NEFEMjNFQUFACTEyMzQ1Njc4OVdAMu7TmeDQRxXnIl5YKYj5JY7Q0A8Ha4eHMtnhKsg4taH34YN5PvkG7tVnNBN/MtqCdyPv+mP/jHvfzfY+O4o55w==", 200)
    response.mimetype = "text/plain"

    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)

# logging.debug("DEBUG")
# logging.info("INFO")
# logging.warning("WARNING")
# logging.error("ERROR")
# logging.critical("CRITICAL")
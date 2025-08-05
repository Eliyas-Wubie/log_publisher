from flask import Flask,request,jsonify

app=Flask(__name__)

@app.route("/hey",methods=["POST"])
def print_log():
    data=request.json
    print(data)
    return jsonify({"done":"yes"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=9000, debug=True)
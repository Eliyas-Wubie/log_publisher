from package_setup_example import log_publisher
from flask import Flask,request,jsonify

app=Flask(__name__)

@app.route("/hi", methods=["GET","POST"])
def check():
    print("foo")
    log_publisher.log("heyyy")
    return jsonify({"message":"hey"})


if __name__=="__main__":
    app.run(host="127.0.0.1", port=3333, debug=False)
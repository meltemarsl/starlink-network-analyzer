from flask import Flask,jsonify
from orchestrator import Orchestrator

app = Flask(__name__)
orch = Orchestrator("config.yaml")

@app.route("/start",methods=["POST"])
def start():
    results = orch.run_all_tests()
    return jsonify(results)

@app.route("/health",methods=["GET"])
def health():
    return jsonify({"status":"ok"})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=8000,debug=True)

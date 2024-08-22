from flask import Flask, request, jsonify
import subprocess
import os
import json

app = Flask(__name__)

def index_directory(root_dir):
    index = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for dirname in dirnames:
            index.append(os.path.join(dirpath, dirname))
    return index

@app.route('/index', methods=['POST'])
def index():
    root_dir = "/home/newkleer/LDAP"
    index = index_directory(root_dir)
    index_json = json.dumps(index, indent=4)
    with open("program_index.json", "w") as f:
        f.write(index_json)
    return jsonify(index)

@app.route('/share', methods=['POST'])
def share():
    path = "/mnt/cloudcode/"
    name = "offsec"
    result = subprocess.run(["sudo", "tailscale", "drive", "share", name, path], capture_output=True, text=True)
    if result.returncode == 0:
        return jsonify({"status": "success", "message": result.stdout}), 200
    else:
        return jsonify({"status": "error", "message": result.stderr}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

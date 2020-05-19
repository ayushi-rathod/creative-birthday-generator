from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)

@app.route('/genlink', methods = ['POST'])
def genlink():
    if request.method == 'POST':
        data = request.get_json()
        output = ""
        if data is not None:
            output = data['name']
            # Create a link
            # Add to db
            # send back page link
        return jsonify({"res": output})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)

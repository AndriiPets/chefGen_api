
from flask import Flask
from generator import generation_function
from flask import request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello():
    return 'Hello world!'


@app.route('/generate', methods=['POST'])
def generate():
    request_data = request.get_json()

    text = request_data['prompt']

    if request_data.get("lang"):
        generated_recepie = generation_function(
            text, lang=request_data["lang"])
    else:
        generated_recepie = generation_function(text)

    return generated_recepie


if __name__ == '__main__':
    app.run()

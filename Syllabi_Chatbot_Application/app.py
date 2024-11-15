from flask import Flask, request, render_template, jsonify
from openai import OpenAI

from database import concatenate

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    # Collect information from the jsonify input
    data = request.json
    message = data.get('message')
    db_info = concatenate()

    # Use ChatGPT to extract information from document
    client = OpenAI()

    pro = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "user", "content": db_info},
            {"role": "user", "content": message}
        ]
    )

    res = pro.choices[0].message.content

    # Handle information
    if message:
        response = {
            'status': 'success',
            'message': f'{res}'
        }
    else:
        response = {
            'status': 'error',
            'message': 'No information received'
        }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
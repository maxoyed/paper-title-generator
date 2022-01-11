from flask import Flask, json, render_template, request, jsonify
import requests

app = Flask(__name__)
TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'


def get_access_token(API_KEY, SECRET_KEY):
    data = {
        'grant_type': 'client_credentials',
        'client_id': API_KEY,
        'client_secret': SECRET_KEY
    }
    res = requests.post(TOKEN_URL, data).json()
    return res['access_token']


def easydl_api(access_token, abstract, API_URL):
    url = API_URL + "?access_token=" + access_token
    print(url)
    text = "摘要：" + abstract + "标题："
    data = {'text': text, 'max_gen_len': 128}
    res = requests.post(url, json=data).json()
    print(res)
    return res['result']['content']


@app.route('/demo1', methods=['GET'])
def index():
    return render_template('demo1.html')


@app.route('/text_gen', methods=['POST'])
def text_gen():
    data = request.json
    API_KEY = data["API_KEY"]
    SECRET_KEY = data["SECRET_KEY"]
    API_URL = data["API_URL"]
    abstract = data["abstract"]
    access_token = get_access_token(API_KEY, SECRET_KEY)
    title = easydl_api(access_token, abstract, API_URL)
    return jsonify({
        "title": title
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

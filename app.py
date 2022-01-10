from flask import Flask, render_template, request
import requests

app = Flask(__name__)
EASYDL_TEXT_CLASSIFY_URL = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/text_gen/a2t_b"
TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'


def get_access_token(API_KEY, SECRET_KEY):
    data = {
        'grant_type': 'client_credentials',
        'client_id': API_KEY,
        'client_secret': SECRET_KEY
    }
    res = requests.post(TOKEN_URL, data).json()
    return res['access_token']


def easydl_api(access_token, abstract):
    url = EASYDL_TEXT_CLASSIFY_URL + "?access_token=" + access_token
    print(url)
    text = "摘要：" + abstract + "标题："
    data = {'text': text, 'max_gen_len': 128}
    res = requests.post(url, json=data).json()
    print(res)
    return res['result']['content']


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/text_gen', methods=['POST'])
def text_gen():
    API_KEY = request.form["API_KEY"]
    SECRET_KEY = request.form["SECRET_KEY"]
    abstract = request.form["abstract"]
    if abstract == '':
        return render_template('index.html')
    access_token = get_access_token(API_KEY, SECRET_KEY)
    title = easydl_api(access_token, abstract)
    return render_template('index.html', title=title, abstract=abstract)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
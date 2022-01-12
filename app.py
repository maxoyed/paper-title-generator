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
    res = requests.post(TOKEN_URL, data)
    # print(f"get access token res status_code: {res.status_code}")
    # print(f"get access token res json: {res.json()}")
    if res.status_code != 200:
        return False
    else:
        return res.json()['access_token']


def easydl_api(access_token, abstract, API_URL, with_prefix=False):
    url = API_URL + "?access_token=" + access_token
    text = abstract
    if with_prefix:
        text = "摘要：" + abstract + "标题："
    data = {'text': text, 'max_gen_len': 128}
    try:
        res = requests.post(url, json=data)
        # print(f"easydl api res status_code: {res.status_code}")
        # print(f"easydl api res json: {res.json()}")
        return res.json()['result']['content']
    except:
        return False


@app.route('/', methods=['GET'])
@app.route('/demo1', methods=['GET'])
def demo1():
    return render_template('demo1.html')


@app.route('/demo2', methods=['GET'])
def demo2():
    return render_template('demo2.html')


@app.route('/demo3', methods=['GET'])
def demo3():
    return render_template('demo3.html')


@app.route('/text_gen', methods=['POST'])
def text_gen():
    data = request.json
    access_token = get_access_token(data["API_KEY"], data["SECRET_KEY"])
    if access_token:
        title = easydl_api(access_token, data["abstract"], data["API_URL"],
                           data["with_prefix"])
        if title:
            return jsonify({"title": title})
        else:
            return jsonify({"msg": "API URL 错误"}), 403
    else:
        return jsonify({"msg": "API KEY 或 SECRET KEY 错误"}), 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

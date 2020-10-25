from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만들거나 사용합니다.


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/order', methods=['POST'])
def get_order():
    # 1. 클라이언트로부터 데이터를 받기
    name_receive=request.form['name_give']
    address_receive=request.form['address_give']
    num_receive=request.form['num_give']
    call_receive=request.form['call_give']

    doc={
        "name":name_receive,
        "number":num_receive,
        "address":address_receive,
        "call":call_receive
    }

    # 3. mongoDB에 데이터 넣기
    db.order.insert_one(doc)

    return jsonify({'result': 'success', 'msg': '주문완료!'})


@app.route('/order', methods=['GET'])
def read_articles():
    # 1. mongoDB에서 _id 값을 제외한 모든 데이터 조회해오기(Read)

    all_order=list(db.order.find({},{'_id': False}))

    # 2. articles라는 키 값으로 articles 정보 보내주기
    return jsonify({'result': 'success', 'msg': 'GET 연결되었습니다!','orders':all_order})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
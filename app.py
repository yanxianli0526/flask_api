# Reference
# https://medium.com/@twilightlau94/rest-apis-with-flask-%E7%B3%BB%E5%88%97%E6%95%99%E5%AD%B8%E6%96%87-1-5405216d3166

from flask import Flask, jsonify, request
from config import *

app = Flask(__name__)
app.config.from_object(__name__)

app.config["JSON_AS_ASCII"] = False


# default data
stores = [{
    'name': 'first',
    'items': [{'name': 'my item 1', 'price': 30}]
},
    {
    'name': 'second',
    'items': [{'name': 'my item 2', 'price': 15}]
}
]

# get /store/<name> data: {name :}   http://127.0.0.1:8081/store/first
@app.route('/store/<string:name>', methods=['GET'])
def get_store(name):
    # return stores
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message': 'store not found'})


# get /store   http://127.0.0.1:8081/store
@app.route('/store', methods=['GET'])
def get_stores():
    return jsonify(stores)

# get /store   http://127.0.0.1:8081/credit_card  測試查詢信用卡表  裡面有更新跟新增的測試
@app.route('/credit_card', methods=['GET'])
def get_data():
    db = SQLManager()
    # update test
    # db.moddify("UPDATE `credit_card` SET `num`=%s WHERE id = %s",('3','378'))
    # insert test
    # db.moddify("INSERT INTO `credit_card`(`num`, `bank`, `title`, `description`, `description_2`, `bonus_1`, `bonus_2`, `bonus_3`, `consume_1`, `consume_2`, `consume_3`, `consume_4`, `bonus_4`, `bonus_5`, `bonus_6`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",('2','2','2','2','2','2','2','2','2','2','2','2','2','2','2'))

    citys = db.get_list("SELECT * FROM `credit_card` WHERE id = '2'")
    db.close()
    return jsonify(citys)

# get /store   http://127.0.0.1:8081/credit_card/1   測試取得get參數 name  去id查詢
@app.route('/credit_card/<string:name>', methods=['GET'])
def get_data2(name):
    # name = request.values.get("name")

    # return str(name)
    db = SQLManager()
    citys = db.get_list("SELECT * FROM `credit_card` WHERE id = %s", name)
    db.close()
    return jsonify(citys)

# get /store   http://127.0.0.1:8081/credit_card2/where_1?name=1&name2=2&name3=3   取得name1 name2 name3 內容
@app.route('/credit_card2/where_1', methods=['GET'])
def get_data3():
    # 取得get key 為name的val
    name = request.args.get("name")
    db = SQLManager()
    citys = db.get_list("SELECT * FROM `credit_card` WHERE bonus_2 = %s",name)
    db.close()
    return jsonify(citys)


# post /store data: {name :}   http://127.0.0.1:8081/store   body:{"name" :"123"}
@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)

# post /store/<name> data: {name :}/item    http://127.0.0.1:8081/store/first/item    body:{"name1": "abc","name2": "zxc","price": 999}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()  # post的資料
    for store in stores:
        if store['name'] == name:
            stores.remove(store)
    new_item = {
        'name': request_data['name1'],
        'items': [{
            'name': request_data['name2'],
            'price': request_data['price']
        }]
    }
    stores.append(new_item)
    return jsonify(new_item)

# get /store/<name>/item data: {name :}/item
@app.route('/store/<string:name>/item')
def get_item_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})
    return jsonify({'message': 'store not found'})


# start service
# export FLASK_ENV=development
# flask run
# flask run
app.run(host='0.0.0.0', port=80, debug=True)
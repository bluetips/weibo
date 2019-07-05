import json

from flask import Flask, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient(host='139.196.91.125', port=27017)
db_1 = client['weibo']['comment']


@app.route('/get_data')
def get_data():
    pn = int(request.args.get('pn')) - 1
    ret = db_1.find().sort([{'created_at',-1},]).skip(pn*10).limit(10)
    item_list = []
    for i in ret:
        i['_id'] = ''
        item_list.append(i)
    return json.dumps(item_list)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8091,debug=True)

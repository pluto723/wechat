# coding=gb2312
from flask import Flask
import pymysql
import json

app = Flask(__name__)

conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='123456789',
    db='foodsafety',
    charset='utf8'
)

cur1 = conn.cursor()
sql1 = "select * from 化学成分"
cur1.execute(sql1)
content = cur1.fetchall()
a = list()
for index in content:
    b = list()
    for lis in index:
        if lis is not None:
            b.append(lis)
    a.append(b)
content = a
number = 0
example = content[number]

cur2 = conn.cursor()
sql2 = "select * from 成分"
cur2.execute(sql2)
information = cur2.fetchall()
a = list()
for index in range(len(information)):
    b = list()
    for lis in (list(information[index])):
        lis = lis.replace("\n", "")
        b.append(lis)
    a.append(b)
information = a

cur3 = conn.cursor()
sql3 = "select * from disease"
cur3.execute(sql3)
disease = cur3.fetchall()
d = list()
for index in range(len(disease)):
    d.append(list(disease[index]))
disease = d

cur4 = conn.cursor()
sql4 = "select * from benefit"
cur4.execute(sql4)
benefit = cur4.fetchall()
a = list()
for index in benefit:
    b = list()
    for lis in index:
        if lis is not None:
            b.append(lis)
    a.append(b)
benefit = a

node = [{"id": example[0], "name": example[0], "val": 16, "color": "red", 'symbol': 'diamond'}]
for i in range(1, len(example)):
    node.append({"id": example[i], "name": example[i], "val": 12, "color": "skyblue"})

link = []
for i in range(1, len(example)):
    link.append({"source": example[0], "target": example[i]})

disease_list = []
for i in range(1, len(example)):
    for index in disease:
        if example[i] == index[0]:
            for lis in index[1:]:
                if lis is not None:
                    node.append({"id": lis, "name": lis, "val": 8, "color": "pink"})
                    link.append({"source": index[0], "target": lis, "colorkey": "red"})
                    disease_list.append(lis)

for i in range(1, len(example)):
    for index in benefit:
        if example[i] == index[0]:
            for lis in index[1:]:
                if lis is not None:
                    node.append({"id": lis, "name": lis, "val": 8, "color": "pink"})
                    link.append({"source": index[0], "target": lis, "colorkey": "blue", "relation": "预防"})


@app.route('/content', methods=['POST'])
def graph():
    GraphDate = [node, link, information]
    return json.dumps(GraphDate, ensure_ascii=False)


@app.route('/result', methods=['POST'])
def result():
    ResultDate = [example[0],example[1:]]
    return json.dumps(ResultDate, ensure_ascii=False)


@app.route('/person', methods=['POST'])
def person():
    PrsonDate = [disease_list]
    return json.dumps(PrsonDate, ensure_ascii=False)


if __name__ == "__main__":
    app.run(port=2020, host="127.0.0.1", debug=True)

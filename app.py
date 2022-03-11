# %%
from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
import json

# %%
app = Flask(__name__)
local = True
if local:
    client = MongoClient('mongodb://127.0.0.1:27017')
else:
    #  client = MongoClient("mongodb+srv://krishnan314:ln1vHOw7OBY8JdZ8@cluster0.xt6pr.mongodb.net/ja?retryWrites=true&w=majority")
    client = MongoClient(
        "mongodb+srv://krishnan314:XkVRwWZVNqSbxhSQ@cluster0.xt6pr.mongodb.net/ja?retryWrites=true&w=majority"
    )

#%%
db = client['ja']
col = db['mywords']
hoteru = db['hoteru']

#%%
card_set = iter(list(col.find({}).sort([("seq", 1)]).limit(5)))
current_card_id = -1
current_card = None
card_mod = {}


@app.route('/', methods=['GET', 'POST'])
def index():
    global card_set, card_mod, current_card
    if request.method == 'POST':
        return render_template('success.html', note="post request in home")
    if request.method == 'GET':
        try:
            current_card = next(card_set)
            note = str(current_card["seq"]) + ' : ' + str(
                current_card["offset"])
        except StopIteration:
            card_set = iter(list(col.find({}).sort([("seq", 1)]).limit(15)))
            current_card = next(card_set)
            note = str(current_card["_id"])
        except Exception as ex:
            note = str(ex) + '\n' + ':::::' + str([i for i in card_set])
            return render_template('error.html', note=note)
        return render_template('home.html',
                               note=note,
                               current_card=current_card)


@app.route('/next/<int:ID>/<int:offset>', methods=['GET', 'POST'])
def next_card(ID, offset):
    global current_card_id, card_mod, current_card
    current_card_id = ID

    try:
        col.update_one({"_id": ID}, {
            "$set": {
                "seq": current_card["seq"] + offset,
                "offset": current_card["offset"] + offset,
            }
        })
    except Exception as ex:
        note = 'from next_card() : ' + str(ex)
        return render_template('error.html', note=note)
    return redirect('/')


@app.route('/commit', methods=['GET', 'POST'])
def commit():
    #    try:
    #        note = 'Commit Success' + '\n' + str(card_mod)
    #    except Exception as ex:
    #        note = 'from commit() : ' + str(ex) + '\n' + str(card_mod)
    #        return render_template('error.html', note=note)
    return render_template('success.html',
                           note="Every action is saved instantly")


@app.route('/search', methods=['GET', 'POST'])
def search():
    global card_set, card_mod, current_card
    if request.method == 'POST':
        qstring = request.form['qstring'].lower()
        kquery_set = []
        if qstring != "":
            query_set = list(db['word'].find({
                "word": qstring
            }).sort([("seq", 1)]))
            for char in qstring:
                kquery_set.extend(list(db['kanji'].find({"word": char})))
            if query_set == []:
                query_set = list(db['word'].find({"pronounciation": qstring}))
            if query_set == []:
                query_set = list(db['word'].find({"meaning": qstring}))
            if kquery_set == []:
                kquery_set.extend(list(db['kanji'].find({"meaning": qstring})))

            return render_template('search.html',
                                   query_set=query_set,
                                   kquery_set=kquery_set,
                                   note=str(qstring))
        else:
            query_set = list(db['word'].find({
                "word": current_card["front"]
            }).sort([("seq", 1)]))
            for char in current_card["front"]:
                kquery_set.extend(list(db['kanji'].find({"word": char})))
            return render_template('search.html',
                                   query_set=query_set,
                                   kquery_set=kquery_set,
                                   note=str(qstring))

    return render_template('search.html',
                           query_set=[],
                           kquery=[],
                           note='Empty [not POST]')


@app.route('/search/<qstring>', methods=['GET', 'POST'])
def searchGet(qstring):
    global card_set, card_mod, current_card
    if request.method == 'GET':
        kquery_set = []
        if qstring != "":
            query_set = list(db['word'].find({
                "word": qstring
            }).sort([("seq", 1)]))
            for char in qstring:
                kquery_set.extend(list(db['kanji'].find({"word": char})))
            if query_set == []:
                query_set = list(db['word'].find({"pronounciation": qstring}))
            if query_set == []:
                query_set = list(db['word'].find({"meaning": qstring}))
            if kquery_set == []:
                kquery_set.extend(list(db['kanji'].find({"meaning": qstring})))

            return render_template('search.html',
                                   query_set=query_set,
                                   kquery_set=kquery_set,
                                   note=str(qstring))
        else:
            query_set = list(db['word'].find({
                "word": current_card["front"]
            }).sort([("seq", 1)]))
            for char in current_card["front"]:
                kquery_set.extend(list(db['kanji'].find({"word": char})))
            return render_template('search.html',
                                   query_set=query_set,
                                   kquery_set=kquery_set,
                                   note=str(qstring))

    return render_template('search.html',
                           query_set=[],
                           kquery=[],
                           note='Empty [not POST]')


@app.route('/e3', methods=['GET', 'POST'])
def e3():
    return render_template('error.html')


@app.route('/display', methods=['GET', 'POST'])
def display():
    words = hoteru.find({"offset": {"$lte": 100}}).sort([("seq", 1)]).limit(50)
    return render_template('display.html', words=words)


# def addData():
#     data = json.load(open('dataBank.json'))
#     for card in data:
#         db.session.add(Word(FRONT=card['front'], BACK=card['back']))
#     db.session.commit()

if __name__ == '__main__':
    app.run(
        #        host='192.168.29.165',  #HOME
        host='0.0.0.0',  #HOME
        #        host='10.42.240.17',  #IITM
        port=80,
        debug=True,
        #        threaded=True
    )

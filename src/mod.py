from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('mongodb://127.0.0.1:27017')
db = client['ja']
col = db['mywords']
words = db["word"]
hoteru = db["hoteru"]

#with open('hotorunohikari.html') as f:
#    soup = BeautifulSoup(f.read(), 'lxml')
#
#tables = soup.find_all('table')
#spans = soup.find_all('span', class_="lln-word")
#
## %%
#word_set = {}
#for span in spans:
#    #    if "with-translit" in span['class']:
#    #    print(span["data-word-key"])
#    if span["data-word-key"] not in word_set:
#        word_set[span["data-word-key"]] = 0
#    word_set[span["data-word-key"]] += 1
#
## %%
#iword_set = {}
#for k, v in word_set.items():
#    if v not in iword_set:
#        iword_set[v] = []
#    iword_set[v].append(k.split('|')[1])
#
## %%
#seq = 0
#for freq in sorted(iword_set, reverse=True):
#    for word in iword_set[freq]:
#        if not word.isdigit():
#            pronounciation = {}
#            for i in words.find({"word": word}):
#                if i["pronounciation"] not in pronounciation:
#                    pronounciation[i["pronounciation"]] = []
#                for meaning in i["meaning"]:
#                    if meaning not in pronounciation[i["pronounciation"]]:
#                        pronounciation[i["pronounciation"]].append(meaning)
#            m = ""
#            pr = ", ".join(pronounciation.keys())
#            if len(pronounciation) > 1:
#                for p, M in pronounciation.items():
#                    m += "(" + p + ") " + ", ".join(M) + "; "
#            else:
#                m += ", ".join(i["meaning"])
#            print(word, pr, m)
#            hoteru.update_one({"front": word},
#                              {"$set": {
#                                  "pronounciation": pr,
#                                  "back": m,
#                              }})
#            seq += 1

## %%
#count = 0
#for myw in col.find({}):
#    for hw in hoteru.find({"front": myw["front"]}):
#        #        res = hoteru.update_one({"front": myw["front"]},
#        #                                {"$set": {
#        #                                    "offset": myw["offset"]
#        #                                }})
#        print(myw["front"], myw["offset"], hw["front"], hw["offset"],
#              res.acknowledged)
#        count += 1
#print(count)
#
## %%
#col.update_many({}, {"$set": {"displayed": 0}})

# %%
for wd in hoteru.find():
    print(f'{wd["front"]}', f'({wd["pronounciation"]})', wd["back"])
    for wdw in words.find({"word": wd["front"]}).limit(1):
        print(f'\t {wdw["pronounciation"]} {wdw["meaning"]}')
#        hoteru.update_one({"_id": wd["_id"]}, {
#            "$set": {
#                "back": ", ".join(wdw["meaning"]),
#                "pronounciation": wdw["pronounciation"]
#            }
#        })

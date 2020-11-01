from tinydb import TinyDB, Query

db = TinyDB('db.json')

User = Query()
insert_if_none = db.search(User.name.exists())
if insert_if_none:
    print(insert_if_none)

val = db.search(User.name == 'John')
# present_value = val['name']
# print(type(val))
for val in db:
    print(val['name'])
# db.insert({'name': 'John', 'age': 22})



# db.update({'name': "jon"}, User.name == 'jon')
# print(db.all())
# db.update({'name': "jonaa"}, User.name == 'John')
# print(db.all())

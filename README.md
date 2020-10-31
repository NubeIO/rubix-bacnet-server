# bacnet-flask

```
cd bacnet-flask/
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

HTTP POST:
/read
```
{
    "device_id": "192.168.0.202",
    "object_id": "1",
    "object_type": "analogInput",
    "prop": "presentValue"
}
```

HTTP POST:
/write
```
{
    "device_id": "192.168.0.202",
    "object_id": "1",
    "object_type": "analogOutput",
    "value": 22
}
```

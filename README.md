# bacnet-flask

```
cd bacnet-flask/
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python app.py
```


using bacstack to test
```
read presentValue
./bacrp 123 4 1 85
read array
./bacrp 123 4 1 87
Write a value to @16 of 1
./bacwp 123 4 1 85 16 -1 9 1
Write a value to @16 of null
./bacwp 123 4 1 85 16 -1 0 0
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
    "value": 22.2
}
```

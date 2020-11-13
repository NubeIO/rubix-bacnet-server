# bacnet-flask


## to run a file that imports other classes
```
PYTHONPATH=. python server/bac_server.py

```

```
cd bacnet-flask/
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python app.py
```



## HTTP GET:
Will return all the points
```
/api/bacnet/points
```

Will return all the a point when the UUID is passed in
```
/api/bacnet/points/<uuid>
```





## HTTP POST:
Add a new point
```
/api/bacnet/points
```
body:
```
{
  "object_type": "analogOutput",
  "object_name": "object_name",
  "address": 1,
  "relinquish_default": 1,
  "priority_array_write": {
    "_1": null,
    "_2": null,
    "_3": null,
    "_4": null,
    "_5": null,
    "_6": null,
    "_7": null,
    "_8": 99.9,
    "_9": 892.02,
    "_10": null,
    "_11": null,
    "_12": null,
    "_13": null,
    "_14": null,
    "_15": null,
    "_16": 16.9089
  },
  "units": "volts",
  "description": "description",
  "enable": true,
  "fault": false,
  "data_round": 2,
  "data_offset": 16
}

```



## HTTP PATCH:
Update an existing point
```
/api/bacnet/points/<uuid>
```

body:
```
{
  "object_type": "analogOutput",
  "object_name": "object_name",
  "address": 1,
  "relinquish_default": 1,
  "units": "volts",
  "description": "description",
  "enable": true,
  "fault": false,
  "data_round": 2,
  "data_offset": 16
}

```




## Using a bacnet master to test

### using bacstack to test for a BO
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



### using bacstack to test for a AO
```
read presentValue
./bacrp 123 1 1 85
read array
./bacrp 123 1 1 87
Write a value to @16 of 1
./bacwp 123 1 1 85 16 -1 4 1
Write a value to @16 of null
./bacwp 123 1 1 85 16 -1 0 0
```


### using bacstack to read device/point info

point info
```
pointName
./bacrp 123 1 1 77
pointDisc
./bacrp 123 1 1 28
pointUnits
./bacrp 123 1 1 117
pointEventState
./bacrp 123 1 1 36
```

device info, if the deviceId is 123
```
debian@beaglebone:~/bacnet-stack-0.8.6/bin$ ./bacrp 123 8 123 77
"nube-io"
debian@beaglebone:~/bacnet-stack-0.8.6/bin$ ./bacrp 123 8 123 75
(device, 123)
debian@beaglebone:~/bacnet-stack-0.8.6/bin$ ./bacrp 123 8 123 112
operational-read-only
debian@beaglebone:~/bacnet-stack-0.8.6/bin$ ./bacrp 123 8 123 121
"NUBE-IO-IO vendor_name"
debian@beaglebone:~/bacnet-stack-0.8.6/bin$ ./bacrp 123 8 123 120
1173
```

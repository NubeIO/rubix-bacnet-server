# Rubix BACnet server

## Running in development

- Use [`poetry`](https://github.com/python-poetry/poetry) to manage dependencies
- Simple script to install

    ```bash
    ./setup.sh
    ```

- Join `venv`

    ```bash
    poetry shell
    ```

- Build local binary

    ```bash
    poetry run pyinstaller run.py -n rubix-bacnet --clean --onefile --add-data pyproject.toml:. --add-data config:config
    ```

  The output is: `dist/rubix-bacnet`

## Docker build

### Build

```bash
./docker.sh
```

The output image is: `rubix-bacnet:dev`

### Run

```bash
docker volume create rubix-bacnet-data
docker run --rm -it -p 1919:1919 -v rubix-bacnet-data:/data --name rubix-bacnet rubix-bacnet:dev
```

## Deploy on Production

- Download release artifact
- Review help and start

```bash
$ rubix-bacnet -h
Usage: rubix-bacnet [OPTIONS]

Options:
  -p, --port INTEGER              Port  [default: 1717]
  -g, --global-dir PATH           Global dir
  -d, --data-dir PATH             Application data dir
  -c, --conf-dir PATH             Application config dir
  -i, --identifier TEXT           Identifier  [default: bacnet]
  --prod                          Production mode
  -s, --setting-file TEXT         Rubix BACnet: setting json file
  -l, --logging-conf TEXT         Rubix BACnet: logging config file
  --workers INTEGER               Gunicorn: The number of worker processes for handling requests.
  --gunicorn-config TEXT          Gunicorn: config file(gunicorn.conf.py)
  --log-level [FATAL|ERROR|WARN|INFO|DEBUG]
                                  Logging level
  -h, --help                      Show this message and exit.
```

### MQTT client

##### Topic structure

Publish value topic
```
<client_id>/<client_name>/<site_id>/<site_name>/<device_id>/<device_name>/rubix/bacnet_server/points/<type>/<object_identifier>
```

Debug topic
```
<client_id>/<client_name>/<site_id>/<site_name>/<device_id>/<device_name>/rubix/bacnet_server/debug
```

Example debug topic

```
+/+/+/+/+/+/rubix/bacnet_server/debug
```

## CURL

Get flask server details

```bash
curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET http://0.0.0.0:1717/api/system/ping
```

Get bacnet server details

```bash
curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET http://0.0.0.0:1717/api/bacnet/server
```

Get bacnet server points

```bash
curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET http://0.0.0.0:1717/api/bacnet/points
```

HTTP PATCH new bacnet server `device_id`

```bash
curl --data '{"device_id": "1233"}' -i -H "Accept: application/json" -H "Content-Type: application/json" -X PATCH http://0.0.0.0:1717/api/bacnet/server
```

HTTP PATCH new bacnet server `ip`

```bash
curl --data '{"ip": "192.168.0.123"}' -i -H "Accept: application/json" -H "Content-Type: application/json" -X PATCH http://0.0.0.0:1717/api/bacnet/server
```

## Get details


> GET: `/api/bacnet/points`

> GET: `/api/bacnet/points/uuid/<uuid>`

## Add a new point

> POST: /api/bacnet/points

> Body
```json
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

> PATCH: `/api/bacnet/points/uuid/<uuid>`

> Body
```json
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

## BACnet server

> GET: `/api/bacnet/server`

```json
{
    "ip": "192.168.0.101",
    "port": 47808,
    "device_id": "2508",
    "local_obj_name": "Nube-IO",
    "model_name": "rubix-bac-stack-RC4",
    "vendor_id": "1173",
    "vendor_name": "Nube iO Operations Pty Ltd"
}
```

> PATCH: `/api/bacnet/server`

```json
{
    "device_id": "2508"
}
```

## Using a bacnet master to test

### Using bacstack to test for a BO

```
read presentValue
./bacrp 2508 4 1 85
read array
./bacrp 2508 4 1 87
Write a value to @16 of 1
./bacwp 2508 4 1 85 16 -1 9 1
Write a value to @16 of null
./bacwp 2508 4 1 85 16 -1 0 0
```

### Using bacstack to test for a AO

```
read presentValue
./bacrp 2508 1 1 85
read array
./bacrp 2508 1 1 87
Write a value to @16 of 1
./bacwp 2508 1 1 85 16 -1 4 1
Write a value to @16 of null
./bacwp 2508 1 1 85 16 -1 0 0
```

### Using bacstack to read device/point info

Point info

```
pointName
./bacrp 2508 1 1 77
pointDisc
./bacrp 2508 1 1 28
pointUnits
./bacrp 2508 1 1 117
pointEventState
./bacrp 123 1 1 36
```

Device info, if the deviceId is 123

```
debian@beaglebone:~/bacnet-stack-0.8.6/bin$ ./bacrp 2508 8 123 77
"nube-io"
debian@beaglebone:~/bacnet-stack-0.8.6/bin$ ./bacrp 2508 8 123 75
(device, 123)
debian@beaglebone:~/bacnet-stack-0.8.6/bin$ ./bacrp 2508 8 123 112
operational-read-only
debian@beaglebone:~/bacnet-stack-0.8.6/bin$ ./bacrp 2508 8 123 121
"NUBE-IO-IO vendor_name"
debian@beaglebone:~/bacnet-stack-0.8.6/bin$ ./bacrp 2508 8 123 120
1173
```

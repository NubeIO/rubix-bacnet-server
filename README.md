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
    poetry poetry run pyinstaller run.py -n rubix-bacnet --clean --onefile \
    --add-data pyproject.toml:. \
    --add-data VERSION:. \
    --add-data config:config \
    --add-data migrations:migrations
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
<client_id>/<client_name>/<site_id>/<site_name>/<device_id>/<device_name>/rubix/bacnet_server/points/<type>/<object_identifier>/<object_name>
```

Debug topic
```
<client_id>/<client_name>/<site_id>/<site_name>/<device_id>/<device_name>/rubix/bacnet_server/debug
```

Example debug topic

```
+/+/+/+/+/+/rubix/bacnet_server/debug
```

## How to test using [bacnet-stack](https://github.com/bacnet-stack/bacnet-stack) (here, 2508 as device_id)

### Pre-requisite
- Run this app on our local PC
- Configure IP to your local PC IP or can configure by enabling enable_ip_by_nic_name & ip_by_nic_name
- Run this app
- Install bacnet-stack v1.0.0 on BBB or other device on the same network
- Now, it will make below commands available


### To get available device
```
> ./bacwi
;Device   MAC (hex)            SNET  SADR (hex)           APDU
;-------- -------------------- ----- -------------------- ----
  2508    0A:00:00:06:BA:C0    0     00                   1024
;
; Total Devices: 1
```

### To test for a BO

```
- Read present value
> ./bacrp 2508 4 1 85

- Read priority array
> ./bacrp 2508 4 1 87

- Write a value to @16 of 1
> ./bacwp 2508 4 1 85 16 -1 9 1

- Write a value to @16 of null
> ./bacwp 2508 4 1 85 16 -1 0 0
```

### To test for an AO

```
- Read present value
> ./bacrp 2508 1 1 85

- Read priority array
> ./bacrp 2508 1 1 87

- Write a value to @16 of 1
> ./bacwp 2508 1 1 85 16 -1 4 1

- Write a value to @16 of null
> ./bacwp 2508 1 1 85 16 -1 0 0
```

### To read device/point info

#### Point info

```
- Point Name
> ./bacrp 2508 1 1 77

- Point Discription
> ./bacrp 2508 1 1 28

- Point Units
> ./bacrp 2508 1 1 117

- Point Event State
> ./bacrp 2508 1 1 36
```

#### Device info

```
> ./bacrp 2508 8 2508 77
"nube-io"

> ./bacrp 2508 8 2508 75
(device, 2508)

> ./bacrp 2508 8 2508 112
operational-read-only

> ./bacrp 2508 8 2508 121
"NUBE-IO-IO vendor_name"

> ./bacrp 2508 8 2508 120
1173
```

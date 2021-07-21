# CHANGELOG
## [v1.7.2](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.7.2) (2020-07-21)
- Fix: DB lock issue

## [v1.7.1](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.7.1) (2020-07-20)
- Fix: timeout issue

## [v1.7.0](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.7.0) (2020-07-16)
- Refactor point mappings

## [v1.6.4](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.6.4) (2020-07-04)
- Redo bacnet version as pyproject file is not in the build

## [v1.6.3](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.6.3) (2020-07-04)
- Remove BAC0
- Upgrade gevent

## [v1.6.2](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.6.2) (2020-07-02)
- Optimize to reduce start up time on PI #137

## [v1.6.1](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.6.1) (2020-06-29)
- MQTT topic structure and payload schema change

## [v1.6.0](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.6.0) (2020-06-24)
- Upgrade rubix-registry to v1.1.1 (breaking change, use `rubix-service >= v1.7.7`)

## [v1.5.3](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.5.3) (2020-04-25)
- Migration setup
- Add field source ('OWN', 'MAPPING') for source filtration
- Add VERSION file

## [v1.5.2](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.5.2) (2020-04-20)
- mqtt-rest-bridge replacement with rubix-http
- Cascade delete points mapping

## [v1.5.1](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.5.1) (2020-04-12)
- Fix: On create point next available address

## [v1.5.0](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.5.0) (2020-04-12)
- On create point next available address

## [v1.4.9](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.4.9) (2020-03-23)
- Modbus <> BACnet point two way binding

## [v1.4.8](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.4.8) (2020-03-19)
- Fix: issue with point mapping

## [v1.4.7](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.4.7) (2020-03-17)
- Fix: PATCH lock issue (#105)
- Fix: point name change (#106)
- Fix: BACnet server restart on runtime (#106)

## [v1.4.6](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.4.6) (2020-03-10)
- Point Server Generic API uuid/name change support

## [v1.4.5](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.4.5) (2020-03-03)
- Upgrade MQTT rest bridge (listener issue fix)
- Stackoverflow issue fix: infinite recursion is removed out
- Separate data and config files

## [v1.4.4](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.4.4) (2020-02-26)
- Publish value topic issue fix

## [v1.4.3](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.4.3) (2020-02-25)
- Use rubix-mqtt base
- Standardize MQTT publish topic

## [v1.4.2](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.4.2) (2020-02-22)
- Point query issue fix
- Upgrade rubix-http version

## [v1.4.1](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.4.1) (2020-02-22)
- Support for Generic Point payload write
- Add validation for BACnet point > object_name
- Implement rubix-http for standardizing HTTP error msg

## [v1.4.0](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.4.0) (2020-02-16)
- Updates to protocal-bridge

## [v1.3.9](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.3.9) (2020-02-15)
- Updates to protocal-bridge

## [v1.3.8](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.3.8) (2020-02-09)
- MQTT REST bridge listener config read issue fix

## [v1.3.7](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.3.7) (2021-02-09)
- MQTT REST bridge integration & Generic Point <> BACnet Point sync service

## [v1.3.2](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.3.2) (2021-01-10)
- Fixes to threading as there was issues with the BACnet server
- updated MQTT topic to `rubix/bacnet`

## [v1.3.1](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.3.1) (2021-01-08)
- Don't use `gevent` anymore if don't know how to use it

## [v1.3.0](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.3.0) (2020-12-29)
- **Breaking Changes**: Make delivery artifact as `binary`
- Change setting file format from `.ini` to `.json`
- Dockerize

## [v1.3.0-rc.2](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.3.0-rc.2) (2020-12-28)
### Changed
- Change setting file format from `.ini` to `.json`

## [v1.3.0-rc.1](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.3.0-rc.1) (2020-12-28)
- **Breaking Changes**: Make delivery artifact as `binary`
- Change setting.conf format
- Dockerize

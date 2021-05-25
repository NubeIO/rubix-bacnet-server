# CHANGELOG
## [v1.5.3](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.5.3) (2020-04-25)
### Added
- Migration setup
- Add field source ('OWN', 'MAPPING') for source filtration

## [v1.5.2](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.5.2) (2020-04-20)
### Added
- mqtt-rest-bridge replacement with rubix-http
- Cascade delete points mapping

## [v1.5.1](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.5.1) (2020-04-12)
### Added
- Fix: On create point next available address

## [v1.5.0](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.5.0) (2020-04-12)
### Added
- On create point next available address

## [v1.4.9](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.4.9) (2020-03-23)
### Added
- Modbus <> BACnet point two way binding

## [v1.4.8](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.4.8) (2020-03-19)
### Added
- Fix: issue with point mapping

## [v1.4.7](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.4.7) (2020-03-17)
### Added
- Fix: PATCH lock issue (#105)
- Fix: point name change (#106)
- Fix: BACnet server restart on runtime (#106)

## [v1.4.6](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.4.6) (2020-03-10)
### Added
- Point Server Generic API uuid/name change support

## [v1.4.5](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.4.5) (2020-03-03)
### Added
- Upgrade MQTT rest bridge (listener issue fix)
- Stackoverflow issue fix: infinite recursion is removed out
- Separate data and config files

## [v1.4.4](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.4.4) (2020-02-26)
### Added
- Publish value topic issue fix

## [v1.4.3](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.4.3) (2020-02-25)
### Added
- Use rubix-mqtt base
- Standardize MQTT publish topic

## [v1.4.2](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.4.2) (2020-02-22)
### Added
- Point query issue fix
- Upgrade rubix-http version

## [v1.4.1](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.4.1) (2020-02-22)
### Added
- Support for Generic Point payload write
- Add validation for BACnet point > object_name
- Implement rubix-http for standardizing HTTP error msg

## [v1.4.0](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.4.0) (2020-02-16)
### Added
- Updates to protocal-bridge

## [v1.3.9](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.3.9) (2020-02-15)
### Added
- Updates to protocal-bridge

## [v1.3.8](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.3.8) (2020-02-09)
### Added
- MQTT REST bridge listener config read issue fix

## [v1.3.7](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.3.7) (2021-02-09)
### Added
- MQTT REST bridge integration & Generic Point <> BACnet Point sync service

## [v1.3.2](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.3.2) (2021-01-10)
### Added
- Fixes to threading as there was issues with the BACnet server
- updated MQTT topic to `rubix/bacnet`

## [v1.3.1](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.3.1) (2021-01-08)
### Added
- Don't use `gevent` anymore if don't know how to use it

## [v1.3.0](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.3.0) (2020-12-29)
### Added
- **Breaking Changes**: Make delivery artifact as `binary`
- Change setting file format from `.ini` to `.json`
- Dockerize

## [v1.3.0-rc.2](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.3.0-rc.2) (2020-12-28)
### Changed
- Change setting file format from `.ini` to `.json`

## [v1.3.0-rc.1](https://github.com/NubeIO/rubix-bacnet-server/tree/v1.3.0-rc.1) (2020-12-28)
### Added
- **Breaking Changes**: Make delivery artifact as `binary`
- Change setting.conf format
- Dockerize

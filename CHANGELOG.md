# CHANGELOG
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

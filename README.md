# Streaming Data Types

FlatBuffers is the format chosen for the ISIS data streaming system, derived from the
[ESS messaging system](https://github.com/ess-dmsc/streaming-data-types).

## Schema ids
| ID   | File name                        | Description                                                                                   |
|------|----------------------------------|-----------------------------------------------------------------------------------------------|
| f144 | `f144_logdata.fbs              ` | Controls related log data, typically from EPICS or NICOS. Note: not to be used for array data |
| ev44 | `ev44_events.fbs               ` | Multi-institution neutron event data for both single and multiple pulses                      |
| df12 | `df12_det_spec_map.fbs         ` | Detector-spectrum map for Mantid                                                              |
| se00 | `se00_data.fbs                 ` | Used for storing arrays with optional timestamps, for example waveform data. Replaces _senv_. | 
| ad00 | `ad00_area_detector_array.fbs  ` | EPICS area detector array data                                                                |
| hs01 | `hs01_event_histogram.fbs      ` | Event histogram stored in n dim array                                                         |
| ep01 | `ep01_epics_connection.fbs  `    | Status or event of EPICS connection. Replaces _ep00_                                          |
| json | `json_json.fbs                 ` | Carries a JSON payload                                                                        |
| pl72 | `pl72_run_start.fbs            ` | File writing, run start message for file writer and Mantid                                    |
| 6s4t | `6s4t_run_stop.fbs             ` | File writing, run stop message for file writer and Mantid                                     |
| answ | `answ_action_response.fbs      ` | Holds the result of a command to the filewriter                                               |
| wrdn | `wrdn_finished_writing.fbs     ` | Message from the filewriter when it is done writing a file                                    |
| x5f2 | `x5f2_status.fbs               ` | Status update and heartbeat message for any software                                          |
| fc00 | `fc00_forwarder_config.fbs     ` | Configuration update for Forwarder                                                            |
| al00 | `al00_alarm.fbs                ` | Generic alarm schema for EPICS, NICOS, etc.                                                   |
| da00 | `da00_dataarray.fbs            ` | Pseudo-scipp DataArray with time-dependent and constant Variables                             |
| un00 | `un00_units.fbs            `     | Engineering units update                                                                      |

use crate::flatbuffers_generated::action_response_answ::{ActionResponse, root_as_action_response};
use crate::flatbuffers_generated::alarm_al00::{Alarm, root_as_alarm};
use crate::flatbuffers_generated::area_detector_array_ad00::{ad00_ADArray, root_as_ad_00_adarray};
use crate::flatbuffers_generated::data_se00::{
    root_as_se_00_sample_environment_data, se00_SampleEnvironmentData,
};
use crate::flatbuffers_generated::dataarray_da00::{da00_DataArray, root_as_da_00_data_array};
use crate::flatbuffers_generated::det_spec_map_df12::{
    SpectraDetectorMapping, root_as_spectra_detector_mapping,
};
use crate::flatbuffers_generated::epics_connection_ep01::{
    EpicsPVConnectionInfo, root_as_epics_pvconnection_info,
};
use crate::flatbuffers_generated::event_histogram_hs01::{EventHistogram, root_as_event_histogram};
use crate::flatbuffers_generated::events_ev44::{Event44Message, root_as_event_44_message};
use crate::flatbuffers_generated::finished_writing_wrdn::{
    FinishedWriting, root_as_finished_writing,
};
use crate::flatbuffers_generated::forwarder_config_fc00::{
    fc00_ConfigUpdate, root_as_fc_00_config_update,
};
use crate::flatbuffers_generated::json_json::{JsonData, root_as_json_data};
use crate::flatbuffers_generated::logdata_f144::{f144_LogData, root_as_f_144_log_data};
use crate::flatbuffers_generated::run_start_pl72::{RunStart, root_as_run_start};
use crate::flatbuffers_generated::run_stop_6s4t::{RunStop, root_as_run_stop};
use crate::flatbuffers_generated::status_x5f2::{Status, root_as_status};
use crate::flatbuffers_generated::units_un00::{Units, root_as_units};
use flatbuffers::InvalidFlatbuffer;

#[allow(clippy::all)]
#[rustfmt::skip]
#[allow(dead_code, unused, non_snake_case, non_camel_case_types, non_upper_case_globals)]
pub mod flatbuffers_generated;

/// Enum containing all possible messages currently supported by
/// `deserialize_message`.
#[derive(Debug, Clone, PartialEq)]
pub enum DeserializedMessage<'a> {
    EventDataEv44(Event44Message<'a>),
    AreaDetectorAd00(ad00_ADArray<'a>),
    RunStartPl72(RunStart<'a>),
    RunStop6s4t(RunStop<'a>),
    LogDataF144(f144_LogData<'a>),
    DetSpecMapDf12(SpectraDetectorMapping<'a>),
    SenvSe00(se00_SampleEnvironmentData<'a>),
    HistogramHs01(EventHistogram<'a>),
    EpicsConnectionEp01(EpicsPVConnectionInfo<'a>),
    JsonDataJson(JsonData<'a>),
    ActionResponseAnsw(ActionResponse<'a>),
    FinishedWritingWrdn(FinishedWriting<'a>),
    StatusX5f2(Status<'a>),
    ForwarderConfigFc00(fc00_ConfigUpdate<'a>),
    AlarmAl00(Alarm<'a>),
    DataArrayDa00(da00_DataArray<'a>),
    UnitsUn00(Units<'a>),
}

/// Error raised from `deserialize_message` describing why a message
/// cannot be deserialized
#[derive(Debug, Eq, PartialEq)]
pub enum DeserializationError {
    UnsupportedSchema(String),
    InvalidFlatbuffer(InvalidFlatbuffer),
}

impl From<InvalidFlatbuffer> for DeserializationError {
    fn from(value: InvalidFlatbuffer) -> Self {
        DeserializationError::InvalidFlatbuffer(value)
    }
}

/// Get the schema ID from a message.
pub fn get_schema_id(data: &[u8]) -> Option<&[u8]> {
    data.get(4..8)
}

/// Deserialize an arbitrary message from Kafka.
///
/// Returns `Ok(DeserializedMessage)` if the message type is understood by
/// this function and the message deserialized correctly, or `Err` otherwise.
pub fn deserialize_message(data: &[u8]) -> Result<DeserializedMessage<'_>, DeserializationError> {
    match get_schema_id(data) {
        Some(b"ev44") => Ok(DeserializedMessage::EventDataEv44(
            root_as_event_44_message(data)?,
        )),
        Some(b"ad00") => Ok(DeserializedMessage::AreaDetectorAd00(
            root_as_ad_00_adarray(data)?,
        )),
        Some(b"pl72") => Ok(DeserializedMessage::RunStartPl72(root_as_run_start(data)?)),
        Some(b"6s4t") => Ok(DeserializedMessage::RunStop6s4t(root_as_run_stop(data)?)),
        Some(b"f144") => Ok(DeserializedMessage::LogDataF144(root_as_f_144_log_data(
            data,
        )?)),
        Some(b"df12") => Ok(DeserializedMessage::DetSpecMapDf12(
            root_as_spectra_detector_mapping(data)?,
        )),
        Some(b"se00") => Ok(DeserializedMessage::SenvSe00(
            root_as_se_00_sample_environment_data(data)?,
        )),
        Some(b"hs01") => Ok(DeserializedMessage::HistogramHs01(root_as_event_histogram(
            data,
        )?)),
        Some(b"ep01") => Ok(DeserializedMessage::EpicsConnectionEp01(
            root_as_epics_pvconnection_info(data)?,
        )),
        Some(b"json") => Ok(DeserializedMessage::JsonDataJson(root_as_json_data(data)?)),
        Some(b"answ") => Ok(DeserializedMessage::ActionResponseAnsw(
            root_as_action_response(data)?,
        )),
        Some(b"wrdn") => Ok(DeserializedMessage::FinishedWritingWrdn(
            root_as_finished_writing(data)?,
        )),
        Some(b"x5f2") => Ok(DeserializedMessage::StatusX5f2(root_as_status(data)?)),
        Some(b"fc00") => Ok(DeserializedMessage::ForwarderConfigFc00(
            root_as_fc_00_config_update(data)?,
        )),
        Some(b"al00") => Ok(DeserializedMessage::AlarmAl00(root_as_alarm(data)?)),
        Some(b"da00") => Ok(DeserializedMessage::DataArrayDa00(
            root_as_da_00_data_array(data)?,
        )),
        Some(b"un00") => Ok(DeserializedMessage::UnitsUn00(root_as_units(data)?)),
        _ => Err(DeserializationError::UnsupportedSchema(
            "Unknown message type passed to deserialize".to_owned(),
        )),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::flatbuffers_generated::units_un00::{UnitsArgs, finish_units_buffer};
    use flatbuffers::FlatBufferBuilder;

    #[test]
    fn test_deserialize_message() {
        let mut fbb = FlatBufferBuilder::new();
        let un00_args = UnitsArgs {
            source_name: Some(fbb.create_string("Hello")),
            timestamp: 0,
            units: Some(fbb.create_string("World")),
        };
        let un00 = Units::create(&mut fbb, &un00_args);
        finish_units_buffer(&mut fbb, un00);

        let deserialized = deserialize_message(fbb.finished_data());

        match deserialized {
            Ok(DeserializedMessage::UnitsUn00(msg)) => {
                assert_eq!(msg.source_name(), "Hello");
                assert_eq!(msg.timestamp(), 0);
                assert_eq!(msg.units(), Some("World"));
            }
            _ => panic!("Failed to deserialize message to correct type"),
        }
    }

    #[test]
    fn test_fail_deserialize_message() {
        let deserialized = deserialize_message(b"\0\0\0\0\0\0\0\0\0\0\0\0");

        assert_eq!(
            deserialized,
            Err(DeserializationError::UnsupportedSchema(
                "Unknown message type passed to deserialize".to_owned()
            ))
        );
    }
}

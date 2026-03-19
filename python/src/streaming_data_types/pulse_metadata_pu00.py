from collections import namedtuple
import flatbuffers

import streaming_data_types.fbschemas.pulse_metadata_pu00.Pu00Message as Pu00Message
from streaming_data_types.utils import check_schema_identifier

FILE_IDENTIFIER = b"pu00"

PulseMetadata = namedtuple("PulseMetadata", ("source_name", "message_id", "timestamp_ns", "vetos", "period_number", "proton_charge"))


def deserialise_pu00(buffer) -> PulseMetadata:
    check_schema_identifier(buffer, FILE_IDENTIFIER)
    pu00 = Pu00Message.Pu00Message.GetRootAsPu00Message(buffer, 0)

    return PulseMetadata(
        source_name=pu00.SourceName().decode("utf-8"),
        message_id=pu00.MessageId(),
        timestamp_ns=pu00.ReferenceTime(),
        period_number=pu00.PeriodNumber(),
        proton_charge=pu00.ProtonCharge(),
        vetos=pu00.Vetos(),
    )


def serialise_pu00(source_name: str, message_id: int, timestamp_ns: int, vetos: int | None, period_number: int | None, proton_charge: float | None) -> bytes:
    builder = flatbuffers.Builder(128)

    source_offset = builder.CreateString(source_name)

    Pu00Message.Pu00MessageStart(builder)
    Pu00Message.AddSourceName(builder, source_offset)
    Pu00Message.AddMessageId(builder, message_id)
    Pu00Message.AddReferenceTime(builder, timestamp_ns)
    if vetos is not None:
        Pu00Message.AddVetos(builder, vetos)
    if period_number is not None:
        Pu00Message.AddPeriodNumber(builder, period_number)
    if proton_charge is not None:
        Pu00Message.AddProtonCharge(builder, proton_charge)
    result = Pu00Message.Pu00MessageEnd(builder)

    builder.Finish(result, file_identifier=FILE_IDENTIFIER)
    return bytes(builder.Output())

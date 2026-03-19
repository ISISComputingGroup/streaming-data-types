from collections import namedtuple
from typing import Optional

import flatbuffers

from streaming_data_types.fbschemas.units_un00 import Units
from streaming_data_types.utils import check_schema_identifier

FILE_IDENTIFIER = b"un00"

UnitInfo = namedtuple("UnitInfo", ("source", "timestamp_ns", "units"))


def deserialise_un00(buffer) -> UnitInfo:
    check_schema_identifier(buffer, FILE_IDENTIFIER)
    units = Units.Units.GetRootAsUnits(buffer, 0)

    return UnitInfo(
        units.SourceName().decode("utf-8") if units.SourceName() else "",
        units.Timestamp(),
        units.Units().decode("utf-8") if units.Units() is not None else None,
    )


def serialise_un00(
    source: str, timestamp_ns: int, units: Optional[str]
) -> bytes:
    builder = flatbuffers.Builder(128)
    if units is not None:
        units_offset = builder.CreateString(units)
    source_offset = builder.CreateString(source)

    Units.UnitsStart(builder)
    Units.UnitsAddSourceName(builder, source_offset)
    Units.UnitsAddTimestamp(builder, timestamp_ns)
    if units is not None:
        Units.UnitsAddUnits(builder, units_offset)
    _units = Units.UnitsEnd(builder)

    builder.Finish(_units, file_identifier=FILE_IDENTIFIER)
    return bytes(builder.Output())

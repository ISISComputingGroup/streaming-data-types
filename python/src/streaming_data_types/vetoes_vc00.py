from collections import namedtuple

import flatbuffers

from streaming_data_types.fbschemas.vetoes_vc00 import Vetoes
from streaming_data_types.utils import check_schema_identifier

FILE_IDENTIFIER = b"vc00"

VetoesInfo = namedtuple("VetoesInfo", ("timestamp_ns", "vetoes"))


def deserialise_vc00(buffer) -> VetoesInfo:
    check_schema_identifier(buffer, FILE_IDENTIFIER)
    vetoes = Vetoes.Vetoes.GetRootAsVetoes(buffer, 0)
    return VetoesInfo(
        vetoes.Timestamp(),
        vetoes.Vetoes(),
    )


def serialise_vc00(timestamp_ns: int, vetoes: int) -> bytes:
    builder = flatbuffers.Builder(128)
    Vetoes.Start(builder)
    Vetoes.AddTimestamp(builder, timestamp_ns)
    Vetoes.AddVetoes(builder, vetoes)
    builder.Finish(Vetoes.VetoesEnd(builder), file_identifier=FILE_IDENTIFIER)
    return bytes(builder.Output())

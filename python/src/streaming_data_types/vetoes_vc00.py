from collections import namedtuple

import flatbuffers

from streaming_data_types.fbschemas.vetoes_vc00 import Vetoes
from streaming_data_types.utils import check_schema_identifier

FILE_IDENTIFIER = b"vc00"

VetoesInfo = namedtuple("VetoesInfo", ("timestamp_ns", "vetoes", "veto_names"))

NUM_VETOES = 32

def deserialise_vc00(buffer) -> VetoesInfo:
    check_schema_identifier(buffer, FILE_IDENTIFIER)
    vetoes = Vetoes.Vetoes.GetRootAsVetoes(buffer, 0)
    v = [vetoes.VetoNames(i) for i in range (vetoes.VetoNamesLength())]
    return VetoesInfo(
        vetoes.Timestamp(),
        vetoes.Vetoes(),
        v,
    )


def serialise_vc00(timestamp_ns: int, vetoes: int, veto_names: list[bytes]) -> bytes:
    if (l:= len(veto_names)) != NUM_VETOES:
        raise RuntimeError(f"Veto names not required amount of length (actual: {l}, expected {NUM_VETOES})")

    builder = flatbuffers.Builder(128)

    vec = [builder.CreateString(i) for i in veto_names]
    Vetoes.StartVetoNamesVector(builder, NUM_VETOES)
    for s in vec[::-1]:
        builder.PrependSOffsetTRelative(s)
    v = builder.EndVector()

    Vetoes.Start(builder)
    Vetoes.AddTimestamp(builder, timestamp_ns)
    Vetoes.AddVetoes(builder, vetoes)
    Vetoes.AddVetoNames(builder, v)
    builder.Finish(Vetoes.VetoesEnd(builder), file_identifier=FILE_IDENTIFIER)
    return bytes(builder.Output())

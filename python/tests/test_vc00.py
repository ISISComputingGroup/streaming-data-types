import pytest

from streaming_data_types import DESERIALISERS, SERIALISERS
from streaming_data_types.exceptions import WrongSchemaException
from streaming_data_types.vetoes_vc00 import deserialise_vc00, serialise_vc00


class TestSerialisationVC00:
    def test_serialises_and_deserialises_vc00_message_correctly(self):
        """
        Round-trip to check what we serialise is what we get back.
        """
        veto_names = [f"veto{i}".encode() for i in range(1,33)]
        buf = serialise_vc00(1234567890, 0x1, veto_names)
        entry = deserialise_vc00(buf)

        assert entry.timestamp_ns == 1234567890
        assert entry.vetoes == 0x1
        assert entry.veto_names == veto_names

    def test_if_buffer_has_wrong_id_then_throws(self):
        buf = serialise_vc00(1234567890, 0x1, [b"unused"]*32)

        # Manually hack the id
        buf = bytearray(buf)
        buf[4:8] = b"1234"

        with pytest.raises(WrongSchemaException):
            deserialise_vc00(buf)

    def test_throws_if_veto_list_wrong_length(self):
        with pytest.raises(RuntimeError):
            serialise_vc00(1234567890, 0x1, [b"unused"] * 31)

        with pytest.raises(RuntimeError):
            serialise_vc00(1234567890, 0x1, [b"unused"] * 33)

    def test_schema_type_is_in_global_serialisers_list(self):
        assert "vc00" in SERIALISERS
        assert "vc00" in DESERIALISERS

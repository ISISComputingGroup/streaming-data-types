import pytest

from streaming_data_types import DESERIALISERS, SERIALISERS
from streaming_data_types.exceptions import WrongSchemaException
from streaming_data_types.pulse_metadata_pu00 import deserialise_pu00, serialise_pu00


class TestSerialisationPu00:
    def test_serialises_and_deserialises_pu00_message_correctly(self):
        """
        Round-trip to check what we serialise is what we get back.
        """
        buf = serialise_pu00("some_source", 123, 456, vetos=1, period_number=2, proton_charge=3.)
        entry = deserialise_pu00(buf)

        assert entry.source_name == "some_source"
        assert entry.message_id == 123
        assert entry.timestamp_ns == 456
        assert entry.vetos == 1
        assert entry.period_number == 2
        assert entry.proton_charge == pytest.approx(3.)

    def test_serialises_and_deserialises_un00_message_correctly_with_none(self):
        """
        Round-trip to check what we serialise is what we get back with None specified as a unit.
        """
        buf = serialise_pu00("some_source", 123, 456, None, None, None)
        entry = deserialise_pu00(buf)

        assert entry.source_name == "some_source"
        assert entry.message_id == 123
        assert entry.timestamp_ns == 456
        assert entry.vetos is None
        assert entry.period_number is None
        assert entry.proton_charge is None

    def test_if_buffer_has_wrong_id_then_throws(self):
        buf = serialise_pu00("some_source", 1234567890, 123, None, None, None)

        # Manually hack the id
        buf = bytearray(buf)
        buf[4:8] = b"1234"

        with pytest.raises(WrongSchemaException):
            deserialise_pu00(buf)

    def test_schema_type_is_in_global_serialisers_list(self):
        assert "pu00" in SERIALISERS
        assert "pu00" in DESERIALISERS

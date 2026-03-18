import pytest

from streaming_data_types import DESERIALISERS, SERIALISERS
from streaming_data_types.exceptions import WrongSchemaException
from streaming_data_types.units_un00 import deserialise_un00, serialise_un00


class TestSerialisationUn00:
    def test_serialises_and_deserialises_un00_message_correctly(self):
        """
        Round-trip to check what we serialise is what we get back.
        """
        buf = serialise_un00("some_source", 1234567890, "Some unit")
        entry = deserialise_un00(buf)

        assert entry.source == "some_source"
        assert entry.timestamp_ns == 1234567890
        assert entry.units == "Some unit"

    def test_serialises_and_deserialises_un00_message_correctly_with_none_as_unit(self):
        """
        Round-trip to check what we serialise is what we get back with None specified as a unit.
        """
        buf = serialise_un00("some_source", 1234567890, None)
        entry = deserialise_un00(buf)

        assert entry.source == "some_source"
        assert entry.timestamp_ns == 1234567890
        assert entry.units is None

    def test_if_buffer_has_wrong_id_then_throws(self):
        buf = serialise_un00("some_source", 1234567890, "Some unit")

        # Manually hack the id
        buf = bytearray(buf)
        buf[4:8] = b"1234"

        with pytest.raises(WrongSchemaException):
            deserialise_un00(buf)

    def test_schema_type_is_in_global_serialisers_list(self):
        assert "un00" in SERIALISERS
        assert "un00" in DESERIALISERS

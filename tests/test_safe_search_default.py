"""
Test: proto3 bool vs optional bool default behavior for safe_search.

Demonstrates that a plain `bool` field cannot distinguish "unset" from
"explicitly set to false", while `optional bool` can — allowing the
server to apply the documented default of true when the field is unset.
"""

import safe_search_default_pb2 as pb


class TestBoolDefaultMismatch:
    """Tests showing the bug: plain bool loses the 'unset' signal."""

    def test_plain_bool_defaults_to_false(self):
        """A plain bool field defaults to false in proto3."""
        msg = pb.WebSourceBefore()
        assert msg.safe_search is False, (
            "Proto3 bool defaults to false, contradicting the documented default of true"
        )

    def test_plain_bool_cannot_detect_unset(self):
        """The server cannot tell 'unset' apart from 'explicitly false'."""
        unset = pb.WebSourceBefore()  # Client didn't set safe_search
        explicit_false = pb.WebSourceBefore(safe_search=False)  # Client wants adult content

        # These serialize to identical bytes — the server sees no difference
        assert unset.SerializeToString() == explicit_false.SerializeToString(), (
            "Unset and explicitly-false produce identical wire representations"
        )

    def test_plain_bool_has_no_presence_tracking(self):
        """HasField raises ValueError for plain bool — presence is not tracked."""
        import pytest

        msg = pb.WebSourceBefore()
        with pytest.raises(ValueError, match="does not have presence"):
            msg.HasField("safe_search")


class TestOptionalBoolFix:
    """Tests showing the fix: optional bool preserves the 'unset' signal."""

    def test_optional_bool_detects_unset(self):
        """Server can detect when the client didn't set the field."""
        msg = pb.WebSourceAfter()
        assert not msg.HasField("safe_search"), (
            "HasField returns False when the client never set safe_search"
        )

    def test_optional_bool_detects_explicit_false(self):
        """Server can detect when the client explicitly set false."""
        msg = pb.WebSourceAfter(safe_search=False)
        assert msg.HasField("safe_search"), (
            "HasField returns True when the client explicitly set safe_search=False"
        )

    def test_optional_bool_detects_explicit_true(self):
        """Server can detect when the client explicitly set true."""
        msg = pb.WebSourceAfter(safe_search=True)
        assert msg.HasField("safe_search")
        assert msg.safe_search is True

    def test_unset_and_false_have_different_wire_bytes(self):
        """Unlike plain bool, optional bool distinguishes the two on the wire."""
        unset = pb.WebSourceAfter()
        explicit_false = pb.WebSourceAfter(safe_search=False)

        # With optional, explicitly setting false IS encoded on the wire
        assert unset.SerializeToString() != explicit_false.SerializeToString(), (
            "optional bool encodes explicit false differently from unset"
        )

    def test_server_can_apply_documented_default(self):
        """The server can now implement the documented 'defaults to true' behavior."""
        def apply_server_default(request: pb.WebSourceAfter) -> bool:
            if request.HasField("safe_search"):
                return request.safe_search  # Honor explicit client choice
            return True  # Apply documented default

        assert apply_server_default(pb.WebSourceAfter()) is True, (
            "Unset → server applies default true (safe search ON)"
        )
        assert apply_server_default(pb.WebSourceAfter(safe_search=False)) is False, (
            "Explicit false → server honors client choice (safe search OFF)"
        )
        assert apply_server_default(pb.WebSourceAfter(safe_search=True)) is True, (
            "Explicit true → server honors client choice (safe search ON)"
        )

    def test_roundtrip_preserves_unset(self):
        """The 'unset' signal survives serialization and deserialization."""
        wire = pb.WebSourceAfter().SerializeToString()
        received = pb.WebSourceAfter()
        received.ParseFromString(wire)
        assert not received.HasField("safe_search"), (
            "Unset survives the wire roundtrip"
        )

    def test_roundtrip_preserves_explicit_false(self):
        """An explicit false survives serialization and deserialization."""
        wire = pb.WebSourceAfter(safe_search=False).SerializeToString()
        received = pb.WebSourceAfter()
        received.ParseFromString(wire)
        assert received.HasField("safe_search"), (
            "Explicit false survives the wire roundtrip"
        )
        assert received.safe_search is False

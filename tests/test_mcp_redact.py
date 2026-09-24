"""Tests proving debug_redact protects MCP credentials in debug output.

The debug_redact field option is a protobuf descriptor-level annotation that
tells runtimes to redact sensitive fields in debug/logging output.

The Python protobuf library (as of 6.31.x) does NOT yet honour debug_redact
in str()/repr()/text_format output.  Therefore:

  - "Bug" tests (MCPBefore) verify that credentials ARE exposed in string
    representations and that debug_redact is NOT set on the descriptor.

  - "Fix" tests (MCPAfter) verify that:
      1. The debug_redact option IS set on each sensitive field's descriptor.
      2. Actual field values are still accessible programmatically.
      3. Wire-format roundtrip preserves the real values (redaction is
         display-only and must never corrupt data).
"""

import pytest
from google.protobuf import descriptor_pb2

import mcp_redact_pb2


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

SECRET_TOKEN = "Bearer secret-token-123"
SECRET_HEADER_KEY = "X-Api-Key"
SECRET_HEADER_VAL = "key-456"


def _populate(msg):
    """Fill *msg* with sensitive credential values."""
    msg.authorization = SECRET_TOKEN
    msg.extra_headers[SECRET_HEADER_KEY] = SECRET_HEADER_VAL
    return msg


def _field_has_debug_redact(message_descriptor, field_name):
    """Return True if *field_name* has debug_redact = true in its options."""
    field = message_descriptor.fields_by_name[field_name]
    opts = field.GetOptions()
    return opts.debug_redact


# ---------------------------------------------------------------------------
# Bug tests — MCPBefore (no debug_redact)
# ---------------------------------------------------------------------------

class TestMCPBefore:
    """Before the fix: credentials leak in debug output."""

    def test_authorization_visible_in_str(self):
        msg = _populate(mcp_redact_pb2.MCPBefore())
        text = str(msg)
        assert SECRET_TOKEN in text, (
            "Expected the secret token to appear in str() since "
            "debug_redact is not set"
        )

    def test_extra_headers_visible_in_str(self):
        msg = _populate(mcp_redact_pb2.MCPBefore())
        text = str(msg)
        assert SECRET_HEADER_VAL in text, (
            "Expected the header value to appear in str() since "
            "debug_redact is not set"
        )

    def test_authorization_no_debug_redact_option(self):
        desc = mcp_redact_pb2.MCPBefore.DESCRIPTOR
        assert not _field_has_debug_redact(desc, "authorization"), (
            "MCPBefore.authorization must NOT have debug_redact"
        )

    def test_extra_headers_no_debug_redact_option(self):
        desc = mcp_redact_pb2.MCPBefore.DESCRIPTOR
        assert not _field_has_debug_redact(desc, "extra_headers"), (
            "MCPBefore.extra_headers must NOT have debug_redact"
        )


# ---------------------------------------------------------------------------
# Fix tests — MCPAfter (debug_redact = true)
# ---------------------------------------------------------------------------

class TestMCPAfter:
    """After the fix: descriptor marks fields as redacted; values stay intact."""

    # -- descriptor-level verification --

    def test_authorization_has_debug_redact(self):
        desc = mcp_redact_pb2.MCPAfter.DESCRIPTOR
        assert _field_has_debug_redact(desc, "authorization"), (
            "MCPAfter.authorization MUST have debug_redact = true"
        )

    def test_extra_headers_has_debug_redact(self):
        desc = mcp_redact_pb2.MCPAfter.DESCRIPTOR
        assert _field_has_debug_redact(desc, "extra_headers"), (
            "MCPAfter.extra_headers MUST have debug_redact = true"
        )

    # -- runtime value access (debug_redact must not block reads) --

    def test_authorization_value_accessible(self):
        msg = _populate(mcp_redact_pb2.MCPAfter())
        assert msg.authorization == SECRET_TOKEN

    def test_extra_headers_value_accessible(self):
        msg = _populate(mcp_redact_pb2.MCPAfter())
        assert msg.extra_headers[SECRET_HEADER_KEY] == SECRET_HEADER_VAL

    # -- wire roundtrip (redaction is display-only) --

    def test_wire_roundtrip_preserves_authorization(self):
        original = _populate(mcp_redact_pb2.MCPAfter())
        wire = original.SerializeToString()

        restored = mcp_redact_pb2.MCPAfter()
        restored.ParseFromString(wire)

        assert restored.authorization == SECRET_TOKEN

    def test_wire_roundtrip_preserves_extra_headers(self):
        original = _populate(mcp_redact_pb2.MCPAfter())
        wire = original.SerializeToString()

        restored = mcp_redact_pb2.MCPAfter()
        restored.ParseFromString(wire)

        assert restored.extra_headers[SECRET_HEADER_KEY] == SECRET_HEADER_VAL

    def test_wire_roundtrip_full_equality(self):
        """Serialize ⟶ deserialize must yield an equal message."""
        original = _populate(mcp_redact_pb2.MCPAfter())
        wire = original.SerializeToString()

        restored = mcp_redact_pb2.MCPAfter()
        restored.ParseFromString(wire)

        assert original == restored

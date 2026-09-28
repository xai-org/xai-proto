"""Tests proving the ToolCallStatus zero-value fix.

Bug (Before): IN_PROGRESS = 0 means uninitialized messages look "active".
Fix (After):  UNSPECIFIED = 0 is a safe sentinel; IN_PROGRESS = 4 is explicit.
"""

from tool_call_status_pb2 import (
    ToolCallBefore,
    ToolCallAfter,
    TOOL_CALL_STATUS_BEFORE_IN_PROGRESS,
    TOOL_CALL_STATUS_BEFORE_COMPLETED,
    TOOL_CALL_STATUS_AFTER_UNSPECIFIED,
    TOOL_CALL_STATUS_AFTER_IN_PROGRESS,
    TOOL_CALL_STATUS_AFTER_COMPLETED,
)


# ---------------------------------------------------------------------------
# Bug tests (Before): IN_PROGRESS = 0
# ---------------------------------------------------------------------------

class TestToolCallStatusBefore:
    """Demonstrate the zero-value bug when IN_PROGRESS is 0."""

    def test_uninitialized_has_phantom_in_progress(self):
        """An uninitialized ToolCallBefore has status == IN_PROGRESS (value 0).

        This is the bug: a message whose status was *never set* silently
        appears to be IN_PROGRESS, creating a phantom active state.
        """
        msg = ToolCallBefore()
        assert msg.status == TOOL_CALL_STATUS_BEFORE_IN_PROGRESS
        assert msg.status == 0

    def test_cannot_distinguish_unset_from_in_progress(self):
        """Cannot distinguish 'never set' from 'genuinely in progress'.

        Both have the same int value 0, so there is no way to tell whether
        the sender intentionally set IN_PROGRESS or simply never touched the
        field.
        """
        unset = ToolCallBefore()
        explicit = ToolCallBefore(status=TOOL_CALL_STATUS_BEFORE_IN_PROGRESS)

        # They are indistinguishable at the value level
        assert unset.status == explicit.status
        assert int(unset.status) == int(explicit.status) == 0

        # Wire bytes are identical -- no way to tell apart
        assert unset.SerializeToString() == explicit.SerializeToString()


# ---------------------------------------------------------------------------
# Fix tests (After): UNSPECIFIED = 0, IN_PROGRESS = 4
# ---------------------------------------------------------------------------

class TestToolCallStatusAfter:
    """Demonstrate the fix: UNSPECIFIED=0, IN_PROGRESS=4."""

    def test_uninitialized_has_safe_sentinel(self):
        """An uninitialized ToolCallAfter has status == UNSPECIFIED (value 0).

        This is the fix: unset fields default to a safe sentinel value,
        not a semantically meaningful state.
        """
        msg = ToolCallAfter()
        assert msg.status == TOOL_CALL_STATUS_AFTER_UNSPECIFIED
        assert msg.status == 0

    def test_explicit_in_progress_is_distinguishable(self):
        """Explicitly setting IN_PROGRESS gives value 4, distinguishable
        from the default 0.
        """
        msg = ToolCallAfter(status=TOOL_CALL_STATUS_AFTER_IN_PROGRESS)
        assert msg.status == TOOL_CALL_STATUS_AFTER_IN_PROGRESS
        assert int(msg.status) == 4
        assert msg.status != TOOL_CALL_STATUS_AFTER_UNSPECIFIED

    def test_server_side_branching(self):
        """A server-side function can correctly branch on status.

        UNSPECIFIED -> 'determine from context'
        IN_PROGRESS -> 'actually active'
        """

        def resolve_status(tool_call):
            if tool_call.status == TOOL_CALL_STATUS_AFTER_UNSPECIFIED:
                return "determine from context"
            elif tool_call.status == TOOL_CALL_STATUS_AFTER_IN_PROGRESS:
                return "actually active"
            elif tool_call.status == TOOL_CALL_STATUS_AFTER_COMPLETED:
                return "completed"
            else:
                return "other"

        unset_msg = ToolCallAfter()
        active_msg = ToolCallAfter(status=TOOL_CALL_STATUS_AFTER_IN_PROGRESS)
        completed_msg = ToolCallAfter(status=TOOL_CALL_STATUS_AFTER_COMPLETED)

        assert resolve_status(unset_msg) == "determine from context"
        assert resolve_status(active_msg) == "actually active"
        assert resolve_status(completed_msg) == "completed"

    def test_wire_roundtrip_unset_vs_in_progress(self):
        """Wire roundtrip: unset (0) and explicit IN_PROGRESS (4) serialize
        to different bytes.
        """
        unset_msg = ToolCallAfter()
        active_msg = ToolCallAfter(status=TOOL_CALL_STATUS_AFTER_IN_PROGRESS)

        unset_bytes = unset_msg.SerializeToString()
        active_bytes = active_msg.SerializeToString()

        # They must be different on the wire
        assert unset_bytes != active_bytes

        # Round-trip: deserialize and verify the values survived
        roundtrip_unset = ToolCallAfter()
        roundtrip_unset.ParseFromString(unset_bytes)
        assert roundtrip_unset.status == TOOL_CALL_STATUS_AFTER_UNSPECIFIED

        roundtrip_active = ToolCallAfter()
        roundtrip_active.ParseFromString(active_bytes)
        assert roundtrip_active.status == TOOL_CALL_STATUS_AFTER_IN_PROGRESS

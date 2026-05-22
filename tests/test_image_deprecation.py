"""Tests demonstrating the image field deprecation fix.

Bug: The singular `image` field (field 5) and the repeated `images` field (field 17)
in GenerateImageRequest are documented as mutually exclusive, but proto3 cannot
enforce mutual exclusivity between a singular and repeated field (repeated fields
cannot participate in a oneof).

Fix: Deprecate the singular `image` field so clients are steered toward `images`,
which is a strict superset (supports 0, 1, or many elements).
"""

from image_deprecation_pb2 import (
    GenerateImageRequestAfter,
    GenerateImageRequestBefore,
    ImageUrl,
)


# ---------------------------------------------------------------------------
# Bug tests (Before) -- demonstrate the ambiguity problem
# ---------------------------------------------------------------------------


class TestBugBeforeFix:
    """Tests on GenerateImageRequestBefore showing the mutual-exclusivity gap."""

    def test_both_image_and_images_can_be_set_simultaneously(self):
        """Both `image` and `images` can be populated at the same time --
        proto3 raises no error, which is the root of the ambiguity."""
        msg = GenerateImageRequestBefore()
        msg.image.CopyFrom(ImageUrl(url="https://example.com/single.png"))
        msg.images.append(ImageUrl(url="https://example.com/list1.png"))
        msg.images.append(ImageUrl(url="https://example.com/list2.png"))

        # No exception was raised -- both fields coexist happily
        assert msg.image.url == "https://example.com/single.png"
        assert len(msg.images) == 2

    def test_round_trip_preserves_both_fields(self):
        """Serialization round-trip keeps BOTH fields, proving ambiguity
        survives the wire."""
        msg = GenerateImageRequestBefore()
        msg.image.CopyFrom(ImageUrl(url="https://example.com/single.png"))
        msg.images.append(ImageUrl(url="https://example.com/list1.png"))

        wire = msg.SerializeToString()
        restored = GenerateImageRequestBefore()
        restored.ParseFromString(wire)

        # Both fields survived the round-trip
        assert restored.image.url == "https://example.com/single.png"
        assert len(restored.images) == 1
        assert restored.images[0].url == "https://example.com/list1.png"

    def test_server_cannot_distinguish_intent(self):
        """A server receiving a message with both fields set has no
        proto-level mechanism to determine which one the client intended."""
        msg = GenerateImageRequestBefore()
        msg.image.CopyFrom(ImageUrl(url="https://example.com/primary.png"))
        msg.images.append(ImageUrl(url="https://example.com/alt.png"))

        # The descriptor has no oneof containing these fields
        descriptor = GenerateImageRequestBefore.DESCRIPTOR
        image_field = descriptor.fields_by_name["image"]
        images_field = descriptor.fields_by_name["images"]

        # Neither field belongs to a oneof -- no built-in mutual exclusivity
        assert image_field.containing_oneof is None
        assert images_field.containing_oneof is None

        # Both fields report as set, so the server must guess
        assert msg.HasField("image")
        assert len(msg.images) > 0


# ---------------------------------------------------------------------------
# Fix tests (After) -- the deprecated annotation steers clients to `images`
# ---------------------------------------------------------------------------


class TestFixAfter:
    """Tests on GenerateImageRequestAfter showing the deprecation approach."""

    def test_image_field_is_marked_deprecated(self):
        """The `image` field descriptor carries the deprecated option."""
        descriptor = GenerateImageRequestAfter.DESCRIPTOR
        image_field = descriptor.fields_by_name["image"]
        assert image_field.GetOptions().deprecated is True

    def test_images_field_is_not_deprecated(self):
        """The `images` field remains current -- it is the replacement."""
        descriptor = GenerateImageRequestAfter.DESCRIPTOR
        images_field = descriptor.fields_by_name["images"]
        assert images_field.GetOptions().deprecated is False

    def test_single_element_images_is_equivalent_to_old_image(self):
        """`images` with one element carries the same data as the old
        singular `image` field."""
        old_msg = GenerateImageRequestAfter()
        old_msg.image.CopyFrom(ImageUrl(url="https://example.com/photo.png"))

        new_msg = GenerateImageRequestAfter()
        new_msg.images.append(ImageUrl(url="https://example.com/photo.png"))

        # The payload in images[0] is identical to what was in image
        assert new_msg.images[0].url == old_msg.image.url

    def test_images_supports_zero_elements(self):
        """`images` can be empty, representing 'no image provided'."""
        msg = GenerateImageRequestAfter()
        assert len(msg.images) == 0

    def test_images_supports_one_element(self):
        """`images` with one element replaces the old singular field."""
        msg = GenerateImageRequestAfter()
        msg.images.append(ImageUrl(url="https://example.com/one.png"))
        assert len(msg.images) == 1
        assert msg.images[0].url == "https://example.com/one.png"

    def test_images_supports_many_elements(self):
        """`images` can hold multiple elements -- a superset of singular."""
        msg = GenerateImageRequestAfter()
        for i in range(5):
            msg.images.append(ImageUrl(url=f"https://example.com/{i}.png"))
        assert len(msg.images) == 5

    def test_migration_path_image_to_images(self):
        """Data from the old `image` field can be migrated to `images[0]`."""
        # Simulate a legacy message that only set the singular field
        legacy = GenerateImageRequestAfter()
        legacy.image.CopyFrom(ImageUrl(url="https://example.com/legacy.png"))

        # Migration: copy singular into the repeated list
        migrated = GenerateImageRequestAfter()
        if legacy.HasField("image"):
            migrated.images.append(ImageUrl(url=legacy.image.url))

        # The migrated message uses only the non-deprecated field
        assert len(migrated.images) == 1
        assert migrated.images[0].url == "https://example.com/legacy.png"
        assert not migrated.HasField("image")  # singular field untouched

# Changelog

## [Unreleased]
### Added
- Added `GetCompletionsRequest.safety_identifier`, an opaque, stable string that your application assigns to the end user behind a request, so xAI can attribute a policy violation to that user instead of to your whole API key. Send a hash of your internal user ID, never an email address or display name. The legacy `user` field is still accepted.
- Added experimental `INCLUDE_OPTION_TOOL_CALL_STREAMING` to `IncludeOption` and experimental `ToolCall.index` field to support streaming client-side tool calls incrementally as they are generated. Known issue: the option is currently broken when combined with server-side tools.

### Changed
- Updates or modifications to existing features.

### Fixed
- Bug fixes or corrections to existing issues.

### Removed
- Features or functionalities that have been removed.

## [v1.0.0](https://github.com/xai-org/xai-proto/releases/tag/v1.0.0) - 2025-06-30
### Added
- Initial v1.0.0 release of the public protobuf definitions for xAI's gRPC based APIs

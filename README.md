# xAI API Protobuf Definitions

This repository hosts the public Protocol Buffer (protobuf) definitions for xAI's gRPC-based APIs. These protobuf files define the service interfaces and message structures compatible with xAI's gRPC servers, enabling developers to generate client SDKs in any language supported by the protobuf and gRPC ecosystems. xAI provides an official SDK for [Python](https://github.com/xai-org/xai-sdk-python), which is built on top of these protobuf definitions.

## Code Generation from proto definitions

You have multiple options for generating code from these `.proto` files, depending on your preferences and tech stack. While we describe using the [Buf CLI](https://buf.build/product/cli) for a streamlined workflow with support for linting and remote plugins, it is **not a requirement**. You are free to use `protoc` directly or leverage language-specific tools like `grpcio-tools` for Python, or any other compatible toolset. The choice is entirely up to you. The instructions below include guidance for using Buf, but alternative methods are equally valid.


### Code Generation with Buf CLI

#### Prerequisites

- Install the buf cli : Follow the [official installation guide](https://buf.build/docs/cli/installation/).


The `buf.gen.yaml` file includes plugins for generating Python code, as used in xAI's official SDK. However, you are free to modify `buf.gen.yaml` to include plugins for other languages or frameworks that suit your tech stack, enabling the creation of custom clients or SDKs tailored to your needs. To generate code using the provided configuration, run:

```bash
buf generate
```

This command will:
- Remove previously generated files (due to `clean: true` in `buf.gen.yaml`).
- Generate Python code in the `gen/python` directory, using plugins for Python (`protocolbuffers/python`, `grpc/python`, `protocolbuffers/pyi`).
- Can be customized by editing `buf.gen.yaml` to support additional languages via Buf's remote plugin ecosystem.
- Can also be customized to leverage locally installed plugins as well as remote ones.

## Versioning

xAI's API protobuf definitions generally follow [Semantic Versioning (SemVer)](https://semver.org). The versioning approach is as follows:

- **Major Versions (e.g., `v1`, `v2`)**: Introduce breaking changes, such as:
  - Removing or renaming fields, messages, or services.
  - Changing field types or behaviors in a non-backward-compatible way.
- **Minor Versions**: Add new features or fields in a backward-compatible manner.
- **Patch Versions**: Include bug fixes or minor updates that do not affect compatibility.

The protobuf files are organized by major version (e.g., `proto/xai/api/v1`). Breaking changes will be introduced in a new major version directory (e.g., `proto/xai/api/v2`) to ensure existing clients remain unaffected.

## Official SDKs

xAI maintains official SDKs for:
- [**Python**](https://github.com/xai-org/xai-sdk-python): Built using the generated code from the Python plugins in `buf.gen.yaml`.

These SDKs are available separately and provide a convenient, language-specific interface for interacting with xAI's gRPC APIs. For more details, visit [xAI's API documentation](https://docs.x.ai/).

## Contributing

Functional changes to the protobuf definitions are not accepted at this time, as these files are maintained by xAI to ensure compatibility with our API services. However, changes to improve documentation, fix typos, etc., are welcome. If you have feedback or suggestions, please contact xAI through the official API support channels [support@x.ai](mailto:support@x.ai).

Please see the [contributing documentation](./CONTRIBUTING.md) for full details on contributing to this repository.

## License

The protobuf definitions and related files are licensed under the Apache-2.0 License

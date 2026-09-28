module github.com/xai-org/xai-proto/examples/go/simple_client

go 1.26

replace github.com/xai-org/xai-proto => ../../..

require (
	github.com/xai-org/xai-proto v0.0.0-00010101000000-000000000000
	google.golang.org/grpc v1.71.0
)

require (
	golang.org/x/net v0.34.0 // indirect
	golang.org/x/sys v0.29.0 // indirect
	golang.org/x/text v0.21.0 // indirect
	google.golang.org/genproto/googleapis/rpc v0.0.0-20250115164207-1a7da9e5054f // indirect
	google.golang.org/protobuf v1.36.5 // indirect
)

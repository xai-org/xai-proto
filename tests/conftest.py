"""Generate protobuf Python code before tests run."""
import subprocess
import sys
import os

# Generate proto code at import time (before test collection)
_tests_dir = os.path.dirname(__file__)
_root_dir = os.path.dirname(_tests_dir)
_proto_file = os.path.join(_tests_dir, "tool_call_status.proto")
_pb2_file = os.path.join(_tests_dir, "tool_call_status_pb2.py")

if os.path.exists(_proto_file) and (
    not os.path.exists(_pb2_file)
    or os.path.getmtime(_proto_file) > os.path.getmtime(_pb2_file)
):
    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "grpc_tools.protoc",
            f"-I{_tests_dir}",
            f"--python_out={_tests_dir}",
            _proto_file,
        ]
    )

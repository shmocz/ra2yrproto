#!/bin/bash
: ${PROTOBUF_VERSION:="25.1"}

# ${..+x} expands to nothing if var is unset
if [ -z ${PROTOC_EXE+x} ]; then
	PROTOC_EXE="$(which protoc)"
fi
if [ -z "$PROTOC_EXE" ]; then
	PROTOC_EXE="protoc/bin/protoc"
	if [ ! -f "$PROTOC_EXE" ]; then
		curl -LO "https://github.com/protocolbuffers/protobuf/releases/download/v${PROTOBUF_VERSION}/protoc-${PROTOBUF_VERSION}-linux-x86_64.zip"
		unzip "protoc-${PROTOBUF_VERSION}-linux-x86_64.zip" -d protoc
	fi
	PROTOC_EXE="$(realpath "protoc/bin/protoc")"
fi

python -m pip install --upgrade pip
python -m pip install build
PROTOC_EXE="$PROTOC_EXE" python -m build

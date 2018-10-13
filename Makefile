SRC_DIR := ./server
PROTO_DIR := ./proto
PROTO_FILES := $(wildcard $(PROTO_DIR)/*.proto)
PROTO_GEN_FILES := $(patsubst $(PROTO_DIR)/%.proto,$(SRC_DIR)/proto/%_pb2.py,$(PROTO_FILES))

all: server

protobuf:
	@echo '** Building protobuf files'
	protoc -I=$(PROTO_DIR) --python_out=$(SRC_DIR)/proto $(PROTO_DIR)/*

server: protobuf
	@echo '** Building the server'
	pip install -e . -r requirements.txt

clean:
	@echo '** Cleaning project'
	$(RM) $(PROTO_GEN_FILES)

.PHONY: all server protobuf clean

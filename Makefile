SRC_DIR := ./server
PROTO_DIR := ./proto
PROTO_FILES := $(wildcard $(PROTO_DIR)/*.proto)
PROTO_GEN_FILES := $(patsubst $(PROTO_DIR)/%.proto,$(SRC_DIR)/proto/%_pb2.py,$(PROTO_FILES))

all: server

.SECONDARY:
$(SRC_DIR)/proto/%_pb2.py: $(PROTO_DIR)/%.proto
	protoc -I=$(PROTO_DIR) --python_out=$(SRC_DIR)/proto $<

server: $(PROTO_GEN_FILES)
	@echo '** Building the server'
	pip install -e . -r requirements.txt

clean:
	@echo '** Cleaning project'
	$(RM) $(PROTO_GEN_FILES)

.PHONY: all server clean

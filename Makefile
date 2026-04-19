.PHONY: generate test install

# Pinned openapi-python-client version.
OAPI_PY_CLIENT_VERSION ?= 0.24.3
SPEC ?= spec/openapi.yaml
OUT_DIR := src/plaidly/generated

generate:
	@mkdir -p $(OUT_DIR)
	rm -rf build/plaidly_api_client
	@mkdir -p build
	uvx --from openapi-python-client==$(OAPI_PY_CLIENT_VERSION) \
		openapi-python-client generate \
		--path $(SPEC) \
		--config openapi-python-client.yaml \
		--output-path build/plaidly_api_client \
		--overwrite \
		--meta none
	rm -rf $(OUT_DIR)
	mv build/plaidly_api_client $(OUT_DIR)
	@touch $(OUT_DIR)/__init__.py || true

install:
	pip install -e .[dev]

test:
	pytest tests/ -v

OPENAPI_JSON_ENDPOINT := ${TZ_API_URL}/${TZ_API_VERSION}/openapi.json
TEMP_SCHEMA_FILENAME := .temp-openapi-schema.json
GENERATED_SCHEMA_FILE := tz/client/api/generated_schema.py

openapi-schema:  ## Generate the OpenAPI model code from feo-core
	@# Curl to get the json schema
	curl -s ${OPENAPI_JSON_ENDPOINT}>${TEMP_SCHEMA_FILENAME}
	@# Run the code-gen
	datamodel-codegen \
		--input .temp-openapi-schema.json \
		--input-file-type openapi \
		--base-class tz.client.api.schemas.PydanticBaseModel \
		--target-python-version 3.10 \
		--use-double-quotes \
		--output-model-type pydantic_v2.BaseModel \
		>${GENERATED_SCHEMA_FILE}
	@# Run pre-commit on the file
	pre-commit run --files ${GENERATED_SCHEMA_FILE} || true
	@# Drop the lines (2nd and 3rd) saying where/when it was generated from
	awk -i inplace 'NR!=2 && NR!=3 { print }' ${GENERATED_SCHEMA_FILE}

help: ## See a list of all available targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.* ?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: all $(MAKECMDGOALS)

.DEFAULT_GOAL := help

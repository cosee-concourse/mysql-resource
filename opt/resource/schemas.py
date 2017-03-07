source_schema = {
    "type": "object",
    "properties": {
        "user": {
            "type": "string"
        },
        "password": {
            "type": "string"
        },
        "host": {
            "type": "string"
        }
    },
    "required": [
        "user",
        "password",
        "host"
    ]
}

version_schema = {
    "oneOf": [{
        "type": "object",
        "properties": {
            "schema": {
                "type": "string"
            }
        }
    }, {
        "type": "null"
    }]
}

check_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "source": source_schema,
        "version": version_schema
    },
    "required": [
        "source"
    ]
}

out_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "source": source_schema,
        "params": {
            "type": "object",
            "properties": {
                "config_file": {
                    "type": "string"
                }
            },
            "required": [
              "config_file"
            ],
            "additionalProperties": "false"
        }
    },
    "required": [
        "source",
        "params"
    ]
}

in_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "source": source_schema,
        "version": version_schema
    },
    "required": [
        "source",
        "version"
    ]
}

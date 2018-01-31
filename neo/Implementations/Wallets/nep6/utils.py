from jsonschema import validate
from logzero import logger
import json

nep6_schema = {
    "type": "object",
    "properties": {
        "name": {"type": ["string", "null"]},
        "version": {"type": "string"},
        "scrypt": {
            "type": "object",
            "properties": {
                "n": {"type": "integer"},
                "r": {"type": "integer"},
                "p": {"type": "integer"}
            },
            "required": ['n', "r", "p"]
        },
        "accounts": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "address": {"type": "string"},
                    "label": {"type": ["string", "null"]},
                    "isDefault": {"type": "boolean"},
                    "lock": {"type": "boolean"},
                    "key": {"type": "string"},
                    "contract": {
                        "type": "object",
                        "properties": {
                            "script": {"type": ["string", "null"]},
                            "parameters": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "type": {"type": "string"}
                                    },
                                    "required": ["name", "type"]
                                }
                            },
                            "deployed": {"type": "boolean"}
                        },
                        "required": ["script", "parameters", "deployed"]
                    },
                    "extra": {"type": ["object", "null"]}
                },
                "required": [
                    "address", "label", "isDefault", "lock", "key", "contract"
                ]
            }
        },
        "extra": {"type": ["object", "null"]}
    },
    "required": ["name", "version", "scrypt", "accounts"]
}


def is_nep6_wallet(path):
    """Checks if a given file follows the NEP6 standard

    This function tries to parse the files contents as JSON and the
    checks if all the required fields are accoring to the spec.

    Arguments:
    path - String contain the location of a given file

    Returns:
    True is it conforms with the spec, False otherwise.
    """
    try:
        with open(path) as wallet:
            content = json.loads(wallet.read())

        validate(content, nep6_schema)
        return True
    except Exception as e:
        logger.debug(str(e))
        return False

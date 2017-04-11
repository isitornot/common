from functools import wraps
import json
import jsonschema
from sanic import exceptions


def validate_json(schema_file=None):
    schema = json.load(open(schema_file))

    def factory(f):
        @wraps(f)
        def decorated(self, request, *args, **kargs):
            try:
                jsonschema.validate(request.json, schema)
            except json.JSONDecodeError as err:
                raise exceptions.InvalidUsage("Invalid JSON") from err
            except jsonschema.ValidationError as err:
                raise exceptions.SanicException("JSON does not match schema", status_code=422) from err
            return f(self, request, *args, **kargs)
        return decorated
    return factory


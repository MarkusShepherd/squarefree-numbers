"""Fill uninteresting strict response fields in fake CLI outputs."""
import json


def fill(value, schema):
    if schema.get('type') == 'object':
        value = dict(value or {})
        return {k: fill(value.get(k), child) for k, child in schema['properties'].items()}
    if value is not None:
        if schema.get('type') == 'array':
            return [fill(v, schema['items']) for v in value]
        return value
    if 'enum' in schema:
        return schema['enum'][0]
    return {'string': '', 'array': [], 'boolean': False}.get(schema.get('type'))

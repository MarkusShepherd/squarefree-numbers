"""Provider-independent validation and reproducibility helpers (stdlib only)."""
import copy
import hashlib
import json
import re
from pathlib import Path


def strict_schema(schema):
    """Require every field for both providers; use empty optional values, not omissions."""
    result = copy.deepcopy(schema)
    if 'enum' in result and 'type' not in result:
        result['type'] = 'string'
    if result.get('type') == 'object':
        result['additionalProperties'] = False
        result['properties'] = {k: strict_schema(v) for k, v in result['properties'].items()}
        result['required'] = list(result['properties'])
    elif result.get('type') == 'array':
        result['items'] = strict_schema(result['items'])
    return result


def validate(value, schema, path='$'):
    """Validate the JSON Schema subset used by this repository; fail closed."""
    supported = {'type', 'properties', 'required', 'additionalProperties', 'items', 'enum', 'pattern', 'minItems'}
    if set(schema) - supported:
        raise ValueError(f'{path}: unsupported schema keywords {set(schema) - supported}')
    kind = schema.get('type')
    types = {'object': dict, 'array': list, 'string': str, 'boolean': bool,
             'integer': int, 'number': (int, float)}
    if kind and (not isinstance(value, types[kind]) or kind in ('integer', 'number') and isinstance(value, bool)):
        raise ValueError(f'{path}: expected {kind}')
    if 'enum' in schema and value not in schema['enum']:
        raise ValueError(f'{path}: invalid enum value {value!r}')
    if 'pattern' in schema and not re.search(schema['pattern'], value):
        raise ValueError(f'{path}: does not match {schema["pattern"]}')
    if kind == 'object':
        missing = set(schema.get('required', [])) - value.keys()
        extra = value.keys() - schema['properties'].keys()
        if missing or extra and schema.get('additionalProperties') is False:
            raise ValueError(f'{path}: missing {sorted(missing)}, unexpected {sorted(extra)}')
        for key, child in value.items():
            if key in schema['properties']:
                validate(child, schema['properties'][key], f'{path}.{key}')
    if kind == 'array':
        if len(value) < schema.get('minItems', 0):
            raise ValueError(f'{path}: too few items')
        for i, child in enumerate(value):
            validate(child, schema['items'], f'{path}[{i}]')


def digest(path):
    path = Path(path)
    if path.is_symlink():
        # Record the link itself without dereferencing an untrusted agent output.
        return hash_json({"symlink": str(path.readlink())})
    if not path.exists():
        return None
    if path.is_file():
        return hashlib.sha256(path.read_bytes()).hexdigest()
    return hash_json({str(p.relative_to(path)): digest(p) for p in sorted(path.rglob('*')) if p.is_file() or p.is_symlink()})


def hash_json(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def input_hashes(directory):
    return {str(p.relative_to(directory)): digest(p) for p in sorted(directory.rglob('*')) if p.is_file() or p.is_symlink()}


def validate_verdict(v):
    if v['verdict'] == 'pass' and v['severity'] not in ('none', 'cosmetic', 'defect-confirmed'):
        raise ValueError('pass verdict cannot have gap/fatal severity')
    if v['verdict'] == 'fail' and v['severity'] not in ('gap', 'fatal'):
        raise ValueError('fail verdict must have gap/fatal severity')
    if (v['verdict'] == 'fail' or v['severity'] == 'defect-confirmed') and not v.get('objection', '').strip():
        raise ValueError('failure/defect requires an actionable objection')


def artifact_files(directory):
    """Numerical deliverables, including nested source modules, without harness metadata."""
    reserved = {'_stream.jsonl', '_stderr.txt', '_last.txt', '_schema.json',
                '_container-version.txt', '_candidate.json'}
    files = {}
    for path in sorted(directory.rglob('*')):
        relative = path.relative_to(directory)
        if path.is_symlink():
            raise ValueError('numerical artifacts must not contain symlinks')
        if any(part in ('.git', '__pycache__') for part in relative.parts):
            continue
        if path.is_file() and relative.parts[0] not in reserved:
            files[str(relative)] = path
    return files

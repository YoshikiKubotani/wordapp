from pydantic import Extra


class EntityConfig:
    extra = Extra.forbid
    validate_assignment = True


class ValueObjectConfig:
    extra = Extra.ignore
    validate_assignment = True
    frozen = True
import pytest

import strawberry
from strawberry.exceptions import (
    MissingArgumentsAnnotationsError,
    MissingReturnAnnotationError,
)


def test_resolver_fields():
    @strawberry.type
    class Query:
        @strawberry.field
        def name(self) -> str:
            return "Name"

    definition = Query._type_definition

    assert definition.name == "Query"
    assert len(definition.fields) == 1

    assert definition.fields[0].name == "name"
    assert definition.fields[0].type == str
    assert definition.fields[0].base_resolver == Query.name


def test_raises_error_when_return_annotation_missing():
    with pytest.raises(MissingReturnAnnotationError) as e:

        @strawberry.field
        def hello(self, info):
            return "I'm a resolver"

    assert e.value.args == (
        'Return annotation missing for field "hello", did you forget to add it?',
    )


def test_raises_error_when_argument_annotation_missing():
    with pytest.raises(MissingArgumentsAnnotationsError) as e:

        @strawberry.field
        def hello(self, info, query) -> str:
            return "I'm a resolver"

    assert e.value.args == (
        'Missing annotation for argument "query" in field "hello", '
        "did you forget to add it?",
    )

    with pytest.raises(MissingArgumentsAnnotationsError) as e:

        @strawberry.field
        def hello2(self, info, query, limit) -> str:
            return "I'm a resolver"

    assert e.value.args == (
        'Missing annotation for arguments "limit" and "query" '
        'in field "hello2", did you forget to add it?',
    )

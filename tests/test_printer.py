import textwrap
from typing import Optional

import strawberry
from strawberry.printer import print_schema


def test_simple_required_types():
    @strawberry.type
    class Query:
        s: str
        i: int
        b: bool
        f: float
        id: strawberry.ID

    expected_type = """
    type Query {
      s: String!
      i: Int!
      b: Boolean!
      f: Float!
      id: ID!
    }
    """

    schema = strawberry.Schema(query=Query)

    assert print_schema(schema) == textwrap.dedent(expected_type).strip()


# def test_recursive_type():
#     @strawberry.type
#     class Query:
#         s: "Query"

#     expected_type = """
#     type Query {
#       s: Query!
#     }
#     """

#     schema = strawberry.Schema(query=Query)

#     assert print_schema(schema) == textwrap.dedent(expected_type).strip()


def test_optional():
    @strawberry.type
    class Query:
        s: Optional[str]

    expected_type = """
    type Query {
      s: String
    }
    """

    schema = strawberry.Schema(query=Query)

    assert print_schema(schema) == textwrap.dedent(expected_type).strip()


def test_input_simple_required_types():
    @strawberry.input
    class MyInput:
        s: str
        i: int
        b: bool
        f: float
        id: strawberry.ID

    @strawberry.type
    class Query:
        @strawberry.field
        def search(self, input: MyInput) -> str:
            return input.s

    expected_type = """
    input MyInput {
      s: String!
      i: Int!
      b: Boolean!
      f: Float!
      id: ID!
    }

    type Query {
      search(input: MyInput!): String!
    }
    """

    schema = strawberry.Schema(query=Query)

    assert print_schema(schema) == textwrap.dedent(expected_type).strip()


# def test_input_optional_default():
#     @strawberry.input
#     class MyInput:
#         s: Optional[str]
#         i: int = 0
#         f: float = None

#     @strawberry.type
#     class Query:
#         @strawberry.field
#         def search(self, input: MyInput) -> str:
#             return input.s

#     expected_type = """
#     input MyInput {
#       s: String
#       i: Int! = 0
#       f: Float
#     }

#     type Query {
#       search(input: MyInput!): String!
#     }
#     """

#     schema = strawberry.Schema(query=Query)

#     assert print_schema(schema) == textwrap.dedent(expected_type).strip()


def test_interface():
    @strawberry.interface
    class Node:
        id: strawberry.ID

    @strawberry.type
    class User(Node):
        name: str

    @strawberry.type
    class Query:
        user: User

    expected_type = """
    interface Node {
      id: ID!
    }

    type Query {
      user: User!
    }

    type User implements Node {
      id: ID!
      name: String!
    }
    """

    schema = strawberry.Schema(query=Query)

    assert print_schema(schema) == textwrap.dedent(expected_type).strip()

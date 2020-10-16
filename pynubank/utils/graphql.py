import os
from collections import OrderedDict


def prepare_request_body(graphql_object, variables=None):
    if variables is None:
        variables = {}

    return OrderedDict({
        'variables': variables,
        'query': _get_query(graphql_object)
    })


def _get_query(query_name):
    root = os.path.abspath(os.path.dirname(__file__))
    gql_file = query_name + '.gql'
    path = os.path.join(root, '..', 'queries', gql_file)
    with open(path) as gql:
        return gql.read()

import logging
# from enum import Enum, auto
import networkx as nx
from pathlib import Path

# Note: Could add explicit schema checking to the adding of edges to make sure
# that the origin and destination nodes are of the proper type.


class ConnectionGraph:
    _internal_graph: nx.DiGraph

    NODETYPES = ['PERSON', 'ORGANIZATION', 'PLACE', 'ACCOUNT']
    EDGETYPES = ['ASSOCWITH', 'BASEDIN', 'ONACCOUNT']
    NODESIZE = {'size': 10.0}
    NODECOLORS = {'PERSON': {'r': 217, 'g': 125, 'b': 216},
                  'ORGANIZATION': {'r': 140, 'g': 185, 'b': 0},
                  'PLACE': {'r': 0, 'g': 199, 'b': 255},
                  'ACCOUNT': {'r': 255, 'g': 122, 'b': 69}}

    def __init__(self, graph_attributes: dict = {}):
        self._internal_graph = nx.DiGraph(**graph_attributes)

    @property
    def graph(self):
        return self._internal_graph.graph

    @property
    def nodes(self):
        return self._internal_graph.nodes

    @property
    def edges(self):
        return self._internal_graph.edges

    def clear(self):
        self._internal_graph.clear()

    def add_node(self, label: str, kind: str, keys: dict = {}) -> None:
        logging.info(f'Adding node \'{label}\' of kind {kind}.')
        if self._node_type_valid(kind):
            self._internal_graph.add_node(label,
                                          kind=kind,
                                          **(keys | self.NODECOLORS[kind] |
                                              self.NODESIZE))
        else:
            logging.error('Attempted to add unknown node '
                          f'type \'{kind}\'. Doing nothing.')

    def add_edge(self,
                 origin_node: str,
                 endpoint_node: str,
                 kind: str,
                 keys: dict = {}) -> None:
        logging.info(f'Adding edge ({origin_node}, '
                     '{endpoint_node}) of kind \'{kind}\'.')
        if self._edge_type_valid(kind):
            self._internal_graph.add_edge(origin_node,
                                          endpoint_node,
                                          label=kind,
                                          kind=kind,
                                          **keys)
        else:
            logging.error('Attempted to add unknown edge '
                          f'type \'{kind}\'. Doing nothing.')

    def add_person(self,
                   name: str,
                   place: str = "",
                   org: str = "",
                   account: str = "",
                   skills: str = ""):

        if name in self._internal_graph.nodes:
            logging.warning("Node \'{name}\' already exists in the graph!")
        self.add_node(name, kind='PERSON', keys={'skills': skills})

        if place:
            self.add_person_place_edge(name, place)

        if org:
            self.add_person_org_edge(name, org)

        if account:
            self.add_person_account_edge(name, account)

    def add_person_org_edge(self, name: str, org: str):
        if org not in self._internal_graph.nodes:
            self.add_node(org, kind='ORGANIZATION')
        if (name, org) in self._internal_graph.edges:
            logging.warning(f"Edge ({name}, {org}) already "
                            "exists in the graph!")
        self.add_edge(name, org, kind='ASSOCWITH')

    def add_person_place_edge(self, name: str, place: str):
        if place not in self._internal_graph.nodes:
            self.add_node(place, kind='PLACE')

        if (name, place) in self._internal_graph.edges:
            logging.warning(f"Edge ({name}, {place}) already "
                            "exists in the graph!")
        self.add_edge(name, place, kind='BASEDIN')

    def add_person_account_edge(self, name: str, account: str):
        if account not in self._internal_graph.nodes:
            self.add_node(account, kind='ACCOUNT')

        if (name, account) in self._internal_graph.edges:
            logging.warning(f"Edge ({name}, {account}) already "
                            "exists in the graph!")
        self.add_edge(name, account, kind='ONACCOUNT')

    def _node_type_valid(self, potential_node: str) -> bool:
        return potential_node in self.NODETYPES

    def _edge_type_valid(self, potential_edge: str) -> bool:
        return potential_edge in self.EDGETYPES


def import_graph_from_graphml_file(filename: Path):
    graphml_graph = nx.read_graphml(filename)
    g = ConnectionGraph()
    g._internal_graph = graphml_graph
    return g


def export_graph_to_graphml_file(g: ConnectionGraph, path: Path):
    nx.write_graphml(g._internal_graph, path)

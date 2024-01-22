import logging
import networkx as nx
from pathlib import Path

# TODO: Update search with word2vec to consider approximate matches that include the entire skillset as well.


class ConnectionGraph:
    """
    A class representing a connection graph.

    Attributes:
        _internal_graph (nx.DiGraph): The internal directed graph representing the connections.
        NODETYPES (list): The valid types of nodes in the graph.
        EDGETYPES (list): The valid types of edges in the graph.
        NODESIZE (dict): The default size of nodes in the graph.
        NODECOLORS (dict): The default colors of nodes based on their types.

    Methods:
        __init__(self, graph_attributes: dict = {}): Initializes a new ConnectionGraph instance.
        graph(self): Returns the graph attribute of the internal graph.
        nodes(self): Returns the nodes attribute of the internal graph.
        edges(self): Returns the edges attribute of the internal graph.
        clear(self): Clears the internal graph.
        add_node(self, label: str, kind: str, keys: dict = {}) -> None: Adds a node to the graph.
        add_edge(self, origin_node: str, endpoint_node: str, kind: str, keys: dict = {}) -> None: Adds an edge to the graph.
        add_person(self, name: str, place: str = "", org: str = "", account: str = "", skills: str = ""): Adds a person node to the graph with optional connections to place, organization, and account nodes.
        add_person_org_edge(self, name: str, org: str): Adds an association edge between a person and an organization.
        add_person_place_edge(self, name: str, place: str): Adds a based-in edge between a person and a place.
        add_person_account_edge(self, name: str, account: str): Adds an on-account edge between a person and an account.
        _node_type_valid(self, potential_node: str) -> bool: Checks if a potential node type is valid.
        _edge_type_valid(self, potential_edge: str) -> bool: Checks if a potential edge type is valid.
    """

    _internal_graph: nx.DiGraph

    NODETYPES = ["PERSON", "ORGANIZATION", "PLACE", "ACCOUNT"]
    EDGETYPES = ["ASSOCWITH", "BASEDIN", "ONACCOUNT"]
    NODESIZE = {"size": 10.0}
    NODECOLORS = {
        "PERSON": {"r": 217, "g": 125, "b": 216},
        "ORGANIZATION": {"r": 140, "g": 185, "b": 0},
        "PLACE": {"r": 0, "g": 199, "b": 255},
        "ACCOUNT": {"r": 255, "g": 122, "b": 69},
    }

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
        """
        Clears the internal graph.
        """
        self._internal_graph.clear()

    def add_node(self, label: str, kind: str, keys: dict = {}) -> None:
        """
        Adds a node to the graph.

        Args:
            label (str): The label of the node.
            kind (str): The kind of the node.
            keys (dict, optional): Additional properties of the node. Defaults to {}.

        Returns:
            None
        """
        logging.info(f"Adding node '{label}' of kind {kind}.")
        if self._node_type_valid(kind):
            self._internal_graph.add_node(
                label, label=label, kind=kind, **(keys | self.NODECOLORS[kind] | self.NODESIZE)
            )
        else:
            logging.error(
                "Attempted to add unknown node " f"type '{
                    kind}'. Doing nothing."
            )

    def add_edge(
        self, origin_node: str, endpoint_node: str, kind: str, keys: dict = {}
    ) -> None:
        """
        Adds an edge between two nodes in the graph.

        Parameters:
        - origin_node (str): The origin node of the edge.
        - endpoint_node (str): The endpoint node of the edge.
        - kind (str): The kind of the edge.
        - keys (dict): Additional key-value pairs to be associated with the edge.

        Returns:
        None
        """
        logging.info(
            f"Adding edge ({origin_node}, " f"{
                endpoint_node}) of kind '{kind}'."
        )
        if self._edge_type_valid(kind):
            self._internal_graph.add_edge(
                origin_node, endpoint_node, label=kind, kind=kind, **keys
            )
        else:
            logging.error(
                "Attempted to add unknown edge " f"type '{
                    kind}'. Doing nothing."
            )

    def add_person(
        self,
        name: str,
        role: str = "",
        place: str = "",
        org: str = "",
        account: str = "",
        skills: str = "",
    ):
        """
        Add a person to the graph.

        Args:
            name (str): The name of the person.
            place (str, optional): The place associated with the person. Defaults to "".
            org (str, optional): The organization associated with the person. Defaults to "".
            account (str, optional): The account associated with the person. Defaults to "".
            skills (str, optional): The skills of the person. Defaults to "".
        """
        if name in self._internal_graph.nodes:
            logging.warning("Node '{name}' already exists in the graph!")
        self.add_node(name, kind="PERSON", keys={"skills": skills, "role": role})

        if place:
            self.add_person_place_edge(name, place)

        if org:
            self.add_person_org_edge(name, org)

        if account:
            self.add_person_account_edge(name, account)

    def search_for_person_with_skill(self, skill: str):
        """
        Searches for persons in the graph who have a specific skill.

        Parameters:
        - skill (str): The skill to search for.

        Returns:
        - matching_persons (dict): A dictionary containing the matching persons as keys and their corresponding attributes as values.
        """
        matching_persons = dict(
            filter(
                lambda x: (
                    x[0] if isinstance(x[1], dict) and x[1].get('kind') == 'PERSON' and skill.lower() in x[1].get('skills', '').lower().split(',')
                    else False
                ),
                self._internal_graph.nodes(data=True)
            )
        )
        neighbor_nodes = {}
        for node_id in matching_persons:
            neighbor_nodes[node_id] = self._internal_graph[node_id]  # self._internal_graph.neighbors(node_id)
        return matching_persons, neighbor_nodes

    def add_person_org_edge(self, name: str, org: str):
        """
        Adds an edge between a person and an organization in the graph.

        Args:
            name (str): The name of the person.
            org (str): The name of the organization.

        Returns:
            None
        """
        if org not in self._internal_graph.nodes:
            self.add_node(org, kind="ORGANIZATION")
        if (name, org) in self._internal_graph.edges:
            logging.warning(
                f"Edge ({name}, {org}) already exists in the graph!")
        self.add_edge(name, org, kind="ASSOCWITH")

    def add_person_place_edge(self, name: str, place: str):
        """
        Adds an edge between a person and a place in the graph.

        Args:
            name (str): The name of the person.
            place (str): The name of the place.

        Returns:
            None
        """
        if place not in self._internal_graph.nodes:
            self.add_node(place, kind="PLACE")

        if (name, place) in self._internal_graph.edges:
            logging.warning(
                f"Edge ({name}, {place}) already exists in the graph!")
        self.add_edge(name, place, kind="BASEDIN")

    def add_person_account_edge(self, name: str, account: str):
        """
        Adds an edge between a person and their account in the graph.

        Args:
            name (str): The name of the person.
            account (str): The account associated with the person.

        Returns:
            None
        """
        if account not in self._internal_graph.nodes:
            self.add_node(account, kind="ACCOUNT")

        if (name, account) in self._internal_graph.edges:
            logging.warning(
                f"Edge ({name}, {account}) already exists in the graph!")
        self.add_edge(name, account, kind="ONACCOUNT")

    def _node_type_valid(self, potential_node: str) -> bool:
        """
        Checks if the given potential_node is a valid node type.

        Args:
            potential_node (str): The potential node type to check.

        Returns:
            bool: True if the potential_node is a valid node type, False otherwise.
        """
        return potential_node in self.NODETYPES

    def _edge_type_valid(self, potential_edge: str) -> bool:
        """
        Check if the given potential_edge is a valid edge type.

        Args:
            potential_edge (str): The potential edge type to check.

        Returns:
            bool: True if the potential_edge is a valid edge type, False otherwise.
        """
        return potential_edge in self.EDGETYPES


def import_graph_from_graphml_file(filename: Path):
    """
    Imports a graph from a GraphML file.

    Args:
        filename (Path): The path to the GraphML file.

    Returns:
        ConnectionGraph: The imported graph.
    """
    graphml_graph = nx.read_graphml(filename)
    g = ConnectionGraph()
    g._internal_graph = graphml_graph
    return g


def export_graph_to_graphml_file(g: ConnectionGraph, path: Path):
    """
    Export the connection graph to a GraphML file.

    Args:
        g (ConnectionGraph): The connection graph to export.
        path (Path): The path to save the GraphML file.

    Returns:
        None
    """
    nx.write_graphml(g._internal_graph, path)

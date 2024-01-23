from pathlib import Path
from pequena_arana.connection_graph import (
    ConnectionGraph,
    export_graph_to_graphml_file,
    import_graph_from_graphml_file,
)


def test_add_node():
    """
    Test function to verify the 'add_node' method of ConnectionGraph class.

    It checks if a node is successfully added to the graph.
    """
    graph = ConnectionGraph()
    graph.add_node("node1", "PERSON")
    assert "node1" in graph.nodes


def test_add_edge():
    """
    Test function to verify the 'add_edge' method of ConnectionGraph class.

    It checks if an edge is successfully added between two nodes in the graph.
    """
    graph = ConnectionGraph()
    graph.add_node("node1", "PERSON")
    graph.add_node("node2", "PERSON")
    graph.add_edge("node1", "node2", "ASSOCWITH")
    assert ("node1", "node2") in graph.edges


def test_add_person():
    """
    Test function to verify the 'add_person' method of ConnectionGraph class.

    It checks if a person node is successfully added to the graph along with its associated attributes.
    """
    graph = ConnectionGraph()
    graph.add_person(
        "John Doe",
        place="New York",
        org="Company",
        account="john.doe@example.com",
        skills="Python",
    )
    assert "John Doe" in graph.nodes
    assert ("John Doe", "New York") in graph.edges
    assert ("John Doe", "Company") in graph.edges
    assert ("John Doe", "john.doe@example.com") in graph.edges


def test_import_export_graph():
    """
    Test function to verify the import and export functionality of the graph.

    It checks if a graph can be successfully exported to a GraphML file and then imported back.
    """
    graph = ConnectionGraph()
    graph.add_node("node1", "PERSON")
    graph.add_node("node2", "PERSON")
    graph.add_edge("node1", "node2", "ASSOCWITH")

    filename = Path("/tmp/graph.graphml")
    export_graph_to_graphml_file(graph, filename)
    imported_graph = import_graph_from_graphml_file(filename)

    assert imported_graph.nodes == graph.nodes
    assert imported_graph.edges == graph.edges


def test_search_for_person_with_skill():
    """
    Test function to verify the 'search_for_person_with_skill' method of ConnectionGraph class.

    It checks if the method returns the correct records of persons with a specific skill.
    """
    graph = ConnectionGraph()
    graph.add_person(
        "John Doe", place="New York", org="Company", account="", skills="Python"
    )
    records, _ = graph.search_for_person_with_skill("Python")
    assert "John Doe" in records

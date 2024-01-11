from pathlib import Path
from social_graph_tool.connection_graph import (
    ConnectionGraph,
    export_graph_to_graphml_file,
    import_graph_from_graphml_file,
)


def test_add_node():
    graph = ConnectionGraph()
    graph.add_node("node1", "PERSON")
    assert "node1" in graph.nodes


def test_add_edge():
    graph = ConnectionGraph()
    graph.add_node("node1", "PERSON")
    graph.add_node("node2", "PERSON")
    graph.add_edge("node1", "node2", "ASSOCWITH")
    assert ("node1", "node2") in graph.edges


def test_add_person():
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
    graph = ConnectionGraph()
    graph.add_node("node1", "PERSON")
    graph.add_node("node2", "PERSON")
    graph.add_edge("node1", "node2", "ASSOCWITH")

    filename = Path("/tmp/graph.graphml")
    export_graph_to_graphml_file(graph, filename)
    imported_graph = import_graph_from_graphml_file(filename)

    assert imported_graph.nodes == graph.nodes
    assert imported_graph.edges == graph.edges

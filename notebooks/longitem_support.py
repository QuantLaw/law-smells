import networkx as nx
import regex
from quantlaw.utils.networkx import hierarchy_graph

## Globals ##
chapter_regex = r"\w*\s*\bBuch\b|\[?CHAPTER|\[?Chapter|\[?Chap\."
title_regex = r"\[?TITLE|\[?Title"
chapter_regex = regex.compile(chapter_regex)
title_regex = regex.compile(title_regex)

## Graph Contraction ##
def quotient_graph_with_merge(
    G, self_loops=False, heading_regex=r"\w*\s*\bBuch\b|\[?CHAPTER|\[?Chapter|\[?Chap\."
):
    heading_regex = regex.compile(heading_regex)
    hG = hierarchy_graph(G)

    # build a new MultiDiGraph
    nG = nx.MultiDiGraph()
    nodes_mapping = {}

    for node_id, node_attrs in G.nodes(data=True):

        if is_node_contracted(hG, node_id, heading_regex):
            merge_parent = get_merge_parent(hG, node_id, heading_regex)
            nodes_mapping[node_id] = merge_parent
        else:
            nG.add_node(node_id, **node_attrs)
            nodes_mapping[node_id] = node_id

    nodes_in_nG = set(nG.nodes)

    for e_source, e_target, e_data in G.edges(data=True):
        if e_data["edge_type"] in {"reference", "authority"}:
            # get source and target of edge in quotient graph
            source = nodes_mapping[e_source]
            target = nodes_mapping[e_target]
            assert source in nodes_in_nG, source
            assert target in nodes_in_nG, target
            if self_loops or source != target:  # skip loops, if deactivated
                nG.add_edge(source, target, **e_data)
        else:
            # add containment edge if target is still in quotient graph
            if e_target in nG:
                assert e_source in nodes_in_nG, e_source
                nG.add_edge(e_source, e_target, **e_data)

    nG.graph["name"] = f'{G.graph["name"]}_merged_quotient_graph'

    return nG, nodes_mapping


def get_merge_parent(G, node, heading_regex):
    """
    Gets the first predecessor that is not contracted
    """
    if not is_node_contracted(G, node, heading_regex):
        return node

    parents = list(G.predecessors(node))
    assert len(parents) == 1
    return get_merge_parent(G, parents[0], heading_regex)


def is_root_node(G, node):
    """
    Helper for is_node_contracted
    """
    return G.in_degree(node) == 0


def is_child_of_root_node(G, node):
    """
    Helper for is_node_contracted
    """
    parent = list(G.predecessors(node))[0]
    return G.in_degree(parent) == 0


def get_parent_nodes(G, n):
    """
    get parents of a node ordered root first
    """
    parents = list(G.predecessors(n))
    if parents:
        assert len(parents) == 1
        return get_parent_nodes(G, parents[0]) + parents
    else:
        return []


def get_mapped_chapter_book(G, node, heading_regex):
    for n in get_parent_nodes(G, node) + [node]:
        if n == "root":
            continue
        heading = G.nodes[n].get("heading")
        if heading:
            if heading_regex.match(heading):
                return n
    return None


def parent_without_chapters_books(G, node, heading_regex):
    (parent,) = list(G.predecessors(node))
    for _, successors in nx.bfs_successors(G, parent):
        for successor in successors:
            heading = G.nodes[successor].get("heading")
            if heading:
                if heading_regex.match(heading):
                    return False
    return True


def contracted_below_chapter_book(G, node, heading_regex):
    mapped_node = get_mapped_chapter_book(G, node, heading_regex)

    if mapped_node == node:
        return False
    elif mapped_node:
        return True
    elif parent_without_chapters_books(G, node, heading_regex):
        return True
    else:  # chapter below or no chapter or book in branch
        return False


def is_node_contracted(G, node, heading_regex):
    if is_root_node(G, node) or is_child_of_root_node(G, node):
        return False
    else:
        return contracted_below_chapter_book(G, node, heading_regex)


## Further helper functions ##
def normalize_heading(heading):
    return heading.replace("TITLE", "Title").replace("CHAPTER", "Chapter")


def is_node_of_type(node, ntype):
    if ntype in ["seqitem", "chapter", "title"]:
        return "type" in node and node["type"] == ntype
    else:
        raise ValueError(f"Unsupported compare_type: {ntype}")


def group_items_by(
    G, item_type, group_by, group_by_filter=lambda x: True, max_groups=None
):
    """
    For all nodes of type group_by (e.g., all titles), find all children of
    type item_type that belong to them and create a dictionary of that
    information (list of maps, and each map is a map from a group node id to
    all children node ids).

    parent_filter can be used in prototyping, for example to only allow a
    single node or title with ID 5 and so on
    """
    # 1. Find all groups (e.g., all titles)
    result = dict()
    mapping_attribute = f"{group_by}_mapping"
    groups = list(
        set(
            [
                y[mapping_attribute]
                for x, y in G.nodes(data=True)
                if "type" in y and y["type"] == group_by and group_by_filter(x)
            ]
        )
    )

    # Optionally filter groups
    if max_groups is not None:
        groups = groups[:max_groups]

    # Build up statistics for all groups

    for group in groups:
        result[group] = [
            x
            for x, y in G.nodes(data=True)
            if is_node_of_type(y, item_type)
            and mapping_attribute in y
            and y[mapping_attribute] == group
        ]

    return result


def cm2inch(value):
    return value / 2.54

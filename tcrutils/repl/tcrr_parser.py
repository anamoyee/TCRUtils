import re

from .tcrr_nodes import DisposableNode, Node, UnknownNode


def get_nodes_by_name_from_root_nodes(
	root_nodes: tuple[Node],
	name: str,
	*names: str,
) -> tuple[Node]:
	maching_nodes = []

	for node in root_nodes:
		if isinstance(node, str):
			# c.warn("Ignoring isinstance(node, str)==True in get_nodes_by_name_from_root_nodes")
			continue

		if re.match(name, node.name) is None:
			continue

		maching_nodes.append(node)

	if not names:
		return tuple(maching_nodes)

	return get_nodes_by_name_from_root_nodes([child for node in maching_nodes for child in node.children], *names)


def parse_and_submit_nodes(
	input_str: str,
	nodes: tuple["Node | str", ...],
	_root_nodes: tuple[Node, ...] = None,
) -> tuple[Node]:
	if _root_nodes is None:
		_root_nodes = nodes  # No need to copy i tihnk?

	for node in nodes:
		groups = node.match(input_str)

		if groups is None:
			continue

		node_text, rest = groups

		node_text = node_text
		rest = rest

		node.submit(node_text)

		if rest:
			node_children = [
				x
				for y in (
					get_nodes_by_name_from_root_nodes(
						_root_nodes,
						*[f"^{y}$" for y in x.split("/")],
					)
					if isinstance(x, str)
					else (x,)
					for x in node.children
				)
				for x in y
			]

			rest = parse_and_submit_nodes(rest, node_children, _root_nodes)

			return (node, *rest)

		return (node,)

	return (UnknownNode(unknown_text=input_str),)

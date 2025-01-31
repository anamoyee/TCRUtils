import fnmatch

from ..console import console as c
from . import nodes as m_nodes


def get_nodes_by_name_from_root_nodes(
	root_nodes: tuple["m_nodes.Node"],
	name: str,
	*names: str,
) -> tuple["m_nodes.Node"]:
	maching_nodes = []

	for node in root_nodes:
		if isinstance(node, str):
			# c.warn("Ignoring isinstance(node, str)==True in get_nodes_by_name_from_root_nodes")
			continue

		if not fnmatch.fnmatch(node.name, name):
			continue

		maching_nodes.append(node)

	if not names:
		return tuple(maching_nodes)

	return get_nodes_by_name_from_root_nodes([child for node in maching_nodes for child in node.children], *names)


def parse_and_submit_nodes(
	input_str: str,
	nodes: tuple["m_nodes.Node | str", ...],
	_root_nodes: tuple["m_nodes.Node", ...] = None,
) -> tuple["m_nodes.Node"]:
	if _root_nodes is None:
		_root_nodes = nodes  # No need to copy i tihnk?

	for node in nodes:
		groups = node.match(input_str)

		if groups is None:
			continue

		if len(groups) == 2:
			groups = (*groups, False)

		node_text, rest, incomplete = groups

		node = node.copy()

		node.submit(node_text)

		node_children = [
			z
			for y in (
				(
					# get_nodes_by_name_from_root_nodes(
					# 	_root_nodes,
					# 	*x.split("/"),
					# )
					node.resolve_path(x) if isinstance(x, str) else (x,)
				)
				for x in node.children
			)
			for z in y
		]

		if rest:
			rest = parse_and_submit_nodes(rest, node_children, _root_nodes)
		elif any(node_children_irrefutable := [x for x in node_children if isinstance(x, m_nodes.IrrefutableNode)]):
			rest = parse_and_submit_nodes(rest, node_children_irrefutable, ())
		else:
			rest = ()

		if incomplete:
			incomplete = (m_nodes.IncompleteNode(unknown_text="?"),)
		else:
			incomplete = ()

		return (node, *incomplete, *rest)

	return (m_nodes.UnknownNode(unknown_text=input_str),)

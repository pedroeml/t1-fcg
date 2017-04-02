from graph.edge import Edge


class Node:
    def __init__(self, item):
        """

        :param item:
        :param edges:
        :type edges: dict
        """
        self.item = item
        self.edges = {}

    def add_edge(self, node, weight):
        """

        :param node:
        :type node: Node
        :param weight:
        :return:
        """
        try:    # try to find the edge between self and node
            edge = self.find_edge(node)
        except KeyError:    # there is no edge between them
            self.edges[node.item] = Edge(self, node, weight)    # then create one
        else:
            edge.change_weight(weight)    # change its weight

    def remove_edge(self, node):
        self.edges.pop(node.item)

    def find_edge(self, node):
        """

        :param node:
        :return:
        :rtype: Edge
        """
        return self.edges[node.item]

    def get_edges(self):
        """

        :return: [Edge]
        :rtype: list
        """
        return self.edges.values()

    def get_sorted_edges(self):
        """
        
        :return: [Edge]
        :rtype: list
        """
        return sorted(self.get_edges())

    def change_edge_weight(self, node, weight):
        self.find_edge(node).change_weight(weight)

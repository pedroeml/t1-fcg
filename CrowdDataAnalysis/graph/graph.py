from graph.node import Node


class Graph:

    def __init__(self, nodes={}):
        self.nodes = nodes

    def add_node(self, item):
        node = Node(item)
        self.nodes[item] = node

    def find_node(self, item):
        """
        
        :param item: 
        :return: 
        :rtype: Node
        """
        return self.nodes[item]

    def add_edge(self, item_a, item_b, weight):
        node_a = self.find_node(item_a)
        node_b = self.find_node(item_b)

        node_a.add_edge(node_b, weight)

    def change_edge_weight(self, item_a, item_b, weight):
        node_a = self.find_node(item_a)
        node_b = self.find_node(item_b)

        node_a.change_edge_weight(node_b, weight)

    def get_nodes(self):
        """
        
        :return: 
        :rtype: list
        """
        return self.nodes.values()

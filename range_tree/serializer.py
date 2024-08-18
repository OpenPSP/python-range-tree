import orjson

from .avl_tree import RangeNode, RangeTree


class RangeTreeJSONSerializer:
    """
    Utility class for serializing and deserializing a RangeTree to and from JSON files
    using orjson for improved performance.
    """

    @staticmethod
    def serialize(tree, file_path):
        """
        Serializes the given RangeTree to a JSON file using ujson.

        Args:
            tree (RangeTree): The tree to serialize.
            file_path (str): The path where the serialized tree will be saved.
        """

        def node_to_dict(node):
            """
            Recursively converts a RangeNode and its children into a dictionary
            that can be serialized to JSON.

            Args:
                node (RangeNode): The node to convert to a dictionary.

            Returns:
                dict: A dictionary representation of the node, including its children.
            """
            if not node:
                return None
            return {
                "start": node.start,
                "end": node.end,
                "max": node.max,
                "height": node.height,
                "key": node.key,
                "left": node_to_dict(node.left),  # Recursively convert the left child
                "right": node_to_dict(
                    node.right
                ),  # Recursively convert the right child
            }

        # Convert the entire tree starting from the root into a dictionary
        tree_dict = {"root": node_to_dict(tree.root)}

        # Serialize the dictionary to a JSON file
        with open(file_path, "wb") as f:
            f.write(orjson.dumps(tree_dict))

    @staticmethod
    def deserialize(file_path):
        """
        Deserializes the RangeTree from a JSON file using ujson.

        Args:
            file_path (str): The path from where the serialized tree will be loaded.

        Returns:
            RangeTree: The deserialized tree, reconstructed from the JSON data.
        """

        def dict_to_node(node_dict):
            """
            Recursively converts a dictionary representation of a node back into a RangeNode.

            Args:
                node_dict (dict): The dictionary representing a RangeNode.

            Returns:
                RangeNode: The reconstructed RangeNode with its children.
            """
            if not node_dict:
                return None

            # Reconstruct the node from the dictionary
            node = RangeNode(node_dict["start"], node_dict["end"], node_dict["key"])
            node.max = node_dict["max"]
            node.height = node_dict["height"]
            node.left = dict_to_node(
                node_dict["left"]
            )  # Recursively reconstruct the left child
            node.right = dict_to_node(
                node_dict["right"]
            )  # Recursively reconstruct the right child
            return node

        # Load the JSON data from the file
        with open(file_path, "rb") as f:
            tree_dict = orjson.loads(f.read())

        # Create a new RangeTree and set its root to the reconstructed tree
        tree = RangeTree()
        tree.root = dict_to_node(tree_dict["root"])
        return tree

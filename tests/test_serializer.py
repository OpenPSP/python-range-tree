import tempfile

import pytest

from range_tree.avl_tree import RangeTree
from range_tree.serializer import RangeTreeJSONSerializer


def test_serialization_with_tempfile():
    # Create a RangeTree and insert intervals with associated keys
    tree = RangeTree()
    tree.insert(10, 20, "key1")
    tree.insert(15, 25, "key2")

    # Use a temporary file for serialization
    with tempfile.NamedTemporaryFile(delete=True) as temp_file:
        # Serialize the tree to the temporary file
        RangeTreeJSONSerializer.serialize(tree, temp_file.name)

        # Deserialize the tree from the temporary file
        restored_tree = RangeTreeJSONSerializer.deserialize(temp_file.name)

        # Verify that the restored tree works as expected
        assert restored_tree.search(12) == (10, 20, "key1")
        assert restored_tree.search(15) == (10, 20, "key1")
        assert restored_tree.search(21) == (15, 25, "key2")

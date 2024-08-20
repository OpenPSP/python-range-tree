import xml.etree.ElementTree as ET
from typing import Dict, Any

import orjson

from avl_range_tree.avl_tree import RangeTree


def test_insert_single_interval():
    tree = RangeTree()
    tree.insert(10, 20, "key1")
    assert tree.search(15) == (10, 20, "key1")
    assert tree.search(25) is None
    assert tree.search(5) is None


def test_insert_multiple_intervals():
    tree = RangeTree()
    tree.insert(10, 20, "key1")
    tree.insert(21, 25, "key2")
    tree.insert(30, 40, "key3")
    assert tree.search(18) == (10, 20, "key1")
    assert tree.search(35) == (30, 40, "key3")
    assert tree.search(5) is None


def test_overlapping_intervals_with_same_size():
    tree = RangeTree()
    tree.insert(10, 20, "key1")
    tree.insert(15, 25, "key2")
    tree.insert(20, 30, "key3")
    assert tree.search(15) == (15, 25, "key2")
    assert tree.search(22) == (15, 25, "key2")
    assert tree.search(12) == (10, 20, "key1")
    assert tree.search(18) == (15, 25, "key2")
    assert tree.search(26) == (20, 30, "key3")


def test_overlapping_intervals_with_different_sizes():
    tree = RangeTree()
    tree.insert(10, 20, "key1")
    tree.insert(15, 26, "key2")
    tree.insert(20, 30, "key3")
    assert tree.search(15) == (10, 20, "key1")  # Smallest containing interval
    assert tree.search(22) == (20, 30, "key3")
    assert tree.search(12) == (10, 20, "key1")
    assert tree.search(18) == (10, 20, "key1")


def test_non_overlapping_intervals():
    tree = RangeTree()
    tree.insert(10, 20, "key1")
    tree.insert(30, 40, "key2")
    tree.insert(50, 60, "key3")
    assert tree.search(15) == (10, 20, "key1")
    assert tree.search(35) == (30, 40, "key2")
    assert tree.search(55) == (50, 60, "key3")
    assert tree.search(25) is None
    assert tree.search(45) is None


def test_search_no_intervals():
    tree = RangeTree()
    assert tree.search(15) is None


def test_large_intervals():
    tree = RangeTree()
    tree.insert(1, 1000, "key1")
    tree.insert(2000, 3000, "key2")
    tree.insert(4000, 5000, "key3")
    assert tree.search(500) == (1, 1000, "key1")
    assert tree.search(2500) == (2000, 3000, "key2")
    assert tree.search(4500) == (4000, 5000, "key3")
    assert tree.search(3500) is None


def test_insert_and_search_minimal_overlapping_intervals():
    tree = RangeTree()
    tree.insert(10, 20, "key1")
    tree.insert(12, 18, "key2")
    tree.insert(14, 16, "key3")
    tree.insert(11, 19, "key4")
    assert tree.search(15) == (
        14,
        16,
        "key3",
    )  # Smallest interval that contains the point
    assert tree.search(13) == (12, 18, "key2")
    assert tree.search(17) == (12, 18, "key2")
    assert tree.search(21) is None


def test_insert_with_identical_intervals():
    tree = RangeTree()
    tree.insert(10, 20, "key1")
    tree.insert(10, 20, "key2")
    tree.insert(10, 20, "key3")
    tree.insert(10, 20, "key4")
    tree.insert(10, 20, "key5")
    assert tree.search(15) == (
        10,
        20,
        "key2",
    )  # The nodes are inserted on the right and we do two rotations
    assert tree.search(25) is None
    assert tree.search(5) is None


def test_insert_and_search_boundary_conditions():
    tree = RangeTree()
    tree.insert(10, 20, "key1")
    tree.insert(15, 25, "key2")
    tree.insert(30, 40, "key3")
    assert tree.search(10) == (10, 20, "key1")  # Exact boundary match
    assert tree.search(20) == (
        15,
        25,
        "key2",
    )  # Right boundary matches the root which is (15, 25)
    assert tree.search(30) == (30, 40, "key3")  # Exact boundary match
    assert tree.search(40) == (
        30,
        40,
        "key3",
    )  # Right boundary should include the interval


def test_complex_intervals_with_gaps():
    tree = RangeTree()
    tree.insert(1, 5, "key1")
    tree.insert(10, 15, "key2")
    tree.insert(20, 25, "key3")
    tree.insert(30, 35, "key4")
    assert tree.search(0) is None
    assert tree.search(6) is None
    assert tree.search(16) is None
    assert tree.search(36) is None


def test_insert_and_search_negative_intervals():
    tree = RangeTree()
    tree.insert(-20, -10, "key1")
    tree.insert(-15, -5, "key2")
    tree.insert(-30, -25, "key3")
    assert tree.search(-15) == (-20, -10, "key1")
    assert tree.search(-28) == (-30, -25, "key3")
    assert tree.search(-5) == (-15, -5, "key2")
    assert tree.search(0) is None


def test_insert_and_search_mixed_positive_negative_intervals():
    tree = RangeTree()
    tree.insert(-20, -10, "key1")
    tree.insert(0, 10, "key2")
    tree.insert(15, 25, "key3")
    assert tree.search(-15) == (-20, -10, "key1")
    assert tree.search(5) == (0, 10, "key2")
    assert tree.search(20) == (15, 25, "key3")
    assert tree.search(-5) is None
    assert tree.search(30) is None


def test_edge_case_single_point_interval():
    tree = RangeTree()
    tree.insert(10, 10, "key1")
    assert tree.search(10) == (10, 10, "key1")
    assert tree.search(9) is None
    assert tree.search(11) is None


def test_tree_size():
    # Create an empty RangeTree
    tree = RangeTree()

    # Initially, the tree should have size 0
    assert len(tree) == 0

    # Insert the first interval
    tree.insert(10, 20, "key1")
    assert len(tree) == 1  # Size should now be 1

    # Insert a second interval
    tree.insert(15, 25, "key2")
    assert len(tree) == 2  # Size should now be 2

    # Insert a third interval
    tree.insert(30, 40, "key3")
    assert len(tree) == 3  # Size should now be 3

    # Insert another interval with the same start as an existing one
    tree.insert(15, 35, "key4")
    assert len(tree) == 4  # Size should now be 4

    # Insert another interval with a new range
    tree.insert(5, 15, "key5")
    assert len(tree) == 5  # Size should now be 5

    # Insert another interval that should increase the tree height and trigger a rotation
    tree.insert(50, 60, "key6")
    assert len(tree) == 6  # Size should now be 6


def test_in_order_traversal():
    # Create an empty RangeTree
    tree = RangeTree()

    # Insert intervals into the tree
    intervals = [
        (10, 20, "key1"),
        (5, 15, "key2"),
        (15, 25, "key3"),
        (3, 8, "key4"),
        (12, 18, "key5"),
        (1, 4, "key6"),
        (8, 12, "key7"),
        (20, 30, "key8"),
        (25, 35, "key9"),
        (2, 6, "key10"),
    ]

    for start, end, key in intervals:
        tree.insert(start, end, key)

    # Expected in-order traversal (sorted by start value)
    expected_in_order = [
        (1, 4, "key6"),
        (2, 6, "key10"),
        (3, 8, "key4"),
        (5, 15, "key2"),
        (8, 12, "key7"),
        (10, 20, "key1"),
        (12, 18, "key5"),
        (15, 25, "key3"),
        (20, 30, "key8"),
        (25, 35, "key9"),
    ]

    # Get the in-order traversal from the tree
    result = list(tree.in_order_traversal(tree.root))

    # Check if the in-order traversal is as expected
    assert result == expected_in_order, f"Expected {expected_in_order}, but got {result}"


def test_in_order_traversal():
    tree = RangeTree()

    # Insert intervals into the tree
    intervals = [
        (10, 20, "key1"),
        (5, 15, "key2"),
        (15, 25, "key3"),
        (3, 8, "key4"),
        (12, 18, "key5"),
        (1, 4, "key6"),
        (8, 12, "key7"),
        (20, 30, "key8"),
        (25, 35, "key9"),
        (2, 6, "key10"),
    ]

    for start, end, key in intervals:
        tree.insert(start, end, key)

    # Expected in-order traversal (sorted by start value)
    expected_in_order = [
        (1, 4, "key6"),
        (2, 6, "key10"),
        (3, 8, "key4"),
        (5, 15, "key2"),
        (8, 12, "key7"),
        (10, 20, "key1"),
        (12, 18, "key5"),
        (15, 25, "key3"),
        (20, 30, "key8"),
        (25, 35, "key9"),
    ]

    # Get the in-order traversal from the tree
    result = list(tree.in_order_traversal(tree.root))

    # Check if the in-order traversal is as expected
    assert result == expected_in_order, f"Expected {expected_in_order}, but got {result}"


def test_pre_order_traversal():
    tree = RangeTree()

    # Insert intervals into the tree
    intervals = [
        (10, 20, "key1"),
        (5, 15, "key2"),
        (15, 25, "key3"),
        (3, 8, "key4"),
        (12, 18, "key5"),
        (1, 4, "key6"),
        (8, 12, "key7"),
        (20, 30, "key8"),
        (25, 35, "key9"),
        (2, 6, "key10"),
    ]

    for start, end, key in intervals:
        tree.insert(start, end, key)

    # Expected pre-order traversal
    expected_pre_order = [
        (10, 20, "key1"),
        (3, 8, "key4"),
        (1, 4, "key6"),
        (2, 6, "key10"),
        (5, 15, "key2"),
        (8, 12, "key7"),
        (15, 25, "key3"),
        (12, 18, "key5"),
        (20, 30, "key8"),
        (25, 35, "key9"),
    ]

    # Get the pre-order traversal from the tree
    result = list(tree.pre_order_traversal(tree.root))

    # Check if the pre-order traversal is as expected
    assert result == expected_pre_order, f"Expected {expected_pre_order}, but got {result}"


def test_post_order_traversal():
    tree = RangeTree()

    # Insert intervals into the tree
    intervals = [
        (10, 20, "key1"),
        (5, 15, "key2"),
        (15, 25, "key3"),
        (3, 8, "key4"),
        (12, 18, "key5"),
        (1, 4, "key6"),
        (8, 12, "key7"),
        (20, 30, "key8"),
        (25, 35, "key9"),
        (2, 6, "key10"),
    ]

    for start, end, key in intervals:
        tree.insert(start, end, key)

    # Expected post-order traversal
    expected_post_order = [
        (2, 6, "key10"),
        (1, 4, "key6"),
        (8, 12, "key7"),
        (5, 15, "key2"),
        (3, 8, "key4"),
        (12, 18, "key5"),
        (25, 35, "key9"),
        (20, 30, "key8"),
        (15, 25, "key3"),
        (10, 20, "key1"),
    ]

    # Get the post-order traversal from the tree
    result = list(tree.post_order_traversal(tree.root))

    # Check if the post-order traversal is as expected
    assert result == expected_post_order, f"Expected {expected_post_order}, but got {result}"


def test_serialization():
    # Create a RangeTree and insert intervals with associated keys
    tree = RangeTree()
    tree.insert(10, 20, "key1")
    tree.insert(15, 25, "key2")

    # Serialize the tree to a JSON string
    json_string = tree.serialize()

    # Deserialize the tree from the JSON string
    restored_tree = RangeTree.deserialize(json_string)
    assert len(restored_tree) == 2

    # Verify that the restored tree works as expected
    assert restored_tree.search(12) == (10, 20, "key1")
    assert restored_tree.search(15) == (10, 20, "key1")
    assert restored_tree.search(21) == (15, 25, "key2")


def test_custom_serialization_json():
    def json_serializer(data: Dict[str, Any]) -> str:
        return orjson.dumps(data).decode("utf-8")

    def json_deserializer(data: str) -> Dict[str, Any]:
        return orjson.loads(json_string)

    # Create a RangeTree and insert intervals with associated keys
    tree = RangeTree()
    tree.insert(10, 20, "key1")
    tree.insert(5, 15, "key2")
    tree.insert(15, 25, "key3")
    tree.insert(3, 8, "key4")
    tree.insert(12, 18, "key5")
    tree.insert(1, 4, "key6")
    tree.insert(8, 12, "key7")
    tree.insert(20, 30, "key8")
    tree.insert(25, 35, "key9")
    tree.insert(2, 6, "key10")

    # Serialize the tree to a JSON string
    json_string = tree.serialize(json_serializer)

    # Deserialize the tree from the JSON string
    restored_tree = RangeTree.deserialize(json_string, json_deserializer)
    assert len(restored_tree) == 10

    # Expected in-order traversal (sorted by start value)
    expected_in_order = [
        (1, 4, "key6"),
        (2, 6, "key10"),
        (3, 8, "key4"),
        (5, 15, "key2"),
        (8, 12, "key7"),
        (10, 20, "key1"),
        (12, 18, "key5"),
        (15, 25, "key3"),
        (20, 30, "key8"),
        (25, 35, "key9"),
    ]

    # Get the in-order traversal from the tree
    result = list(tree.in_order_traversal(tree.root))

    # Check if the in-order traversal is as expected
    assert result == expected_in_order, f"Expected {expected_in_order}, but got {result}"


def test_custom_serialization_xml():
    # Example custom serializer (using a simple XML format)
    def xml_serializer(data: Dict[str, Any]) -> str:
        root = ET.Element("RangeTree")

        def build_xml_node(data, parent):
            for key, value in data.items():
                if isinstance(value, dict):
                    child = ET.SubElement(parent, key)
                    build_xml_node(value, child)
                else:
                    child = ET.SubElement(parent, key)
                    child.text = str(value)

        build_xml_node(data, root)
        return ET.tostring(root, encoding='unicode')

    # Example custom deserializer (parsing the simple XML format)
    def xml_deserializer(data: str) -> Dict[str, Any]:
        def parse_xml_element(element) -> Dict[str, Any]:
            node_dict = {}

            for child in element:
                print(child.tag)
                if len(child):  # If the child has children, recursively parse it
                    node_dict[child.tag] = parse_xml_element(child)
                else:
                    # Handle "None" values explicitly and convert the text to int if it's a number
                    if child.text == "None":
                        node_dict[child.tag] = None
                    elif child.text.isdigit():  # Convert the text to int if it's a number, otherwise leave it as a string
                        node_dict[child.tag] = int(child.text)
                    else:
                        node_dict[child.tag] = child.text

            return node_dict

        root = ET.fromstring(data)
        return parse_xml_element(root)

    # Create a RangeTree and insert intervals with associated keys
    tree = RangeTree()

    tree.insert(10, 20, "key1")
    tree.insert(5, 15, "key2")
    tree.insert(15, 25, "key3")
    tree.insert(3, 8, "key4")
    tree.insert(12, 18, "key5")
    tree.insert(1, 4, "key6")
    tree.insert(8, 12, "key7")
    tree.insert(20, 30, "key8")
    tree.insert(25, 35, "key9")
    tree.insert(2, 6, "key10")

    # Serialize the tree to a JSON string
    xml_string = tree.serialize(xml_serializer)

    print(xml_string)

    # Deserialize the tree from the JSON string
    restored_tree = RangeTree.deserialize(xml_string, xml_deserializer)
    assert len(restored_tree) == 10

    # Verify that the restored tree works as expected

    # Expected in-order traversal (sorted by start value)
    expected_in_order = [
        (1, 4, "key6"),
        (2, 6, "key10"),
        (3, 8, "key4"),
        (5, 15, "key2"),
        (8, 12, "key7"),
        (10, 20, "key1"),
        (12, 18, "key5"),
        (15, 25, "key3"),
        (20, 30, "key8"),
        (25, 35, "key9"),
    ]

    # Get the in-order traversal from the tree
    result = list(tree.in_order_traversal(tree.root))

    # Check if the in-order traversal is as expected
    assert result == expected_in_order, f"Expected {expected_in_order}, but got {result}"

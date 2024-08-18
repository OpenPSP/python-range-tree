import pytest

from range_tree.avl_tree import RangeTree


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

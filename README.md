# Augmented AVL Tree for Interval Search

## Overview

This project implements an augmented AVL tree (a self-balancing binary search tree) in Python, designed specifically for storing and querying intervals efficiently. The tree allows you to insert intervals (with associated keys) and quickly search for the smallest interval containing a given point. This implementation is particularly useful for tasks like BIN (Bank Identification Number) range searches, where each interval represents a range of possible values.

## Features

- **Self-Balancing Tree**: The tree remains balanced after each insertion, ensuring that operations like search, insert, and delete remain efficient.
- **Interval Queries**: Efficiently find the smallest interval that contains a given point.
- **Pure Python Implementation**: The core logic is implemented purely in Python, making it easy to understand and modify.

## Installation

### Using `pip`

1. Ensure you have Python 3.9 or higher installed.
2. Install the package using `pip`:

   ```sh
   pip install avl_range_tree
   ```

### Building from Source

If you'd like to build the package from source:

1. Clone the repository:

    ```sh
    git clone git@github.com:mcoira/python-range-tree.git
    cd python-range-tree/
    ```
   
2. Install the package:

    ```sh
    pip install .
    ```

## Usage

### Importing the Tree

```python
from avl_range_tree.avl_tree import RangeTree
```

### Inserting Intervals

Each interval is defined by a start value, an end value, and a key (a unique identifier for that interval).

```python
tree = RangeTree()
tree.insert(123456000000000000, 123456999999999999, "key1")
tree.insert(987654000000000000, 987654999999999999, "key2")
```

### Searching for Intervals

To search for the smallest interval containing a given point:

```python
search_value = int(str(12345678).ljust(16, '0'))  # Convert 123456 to 1234567800000000
result = tree.search(search_value)

if result:
    start, end, key = result
    print(f"Found interval: [{start}, {end}] with key: {key}")
else:
    print("No interval found containing the point.")
```

### Example Output

```shell
Found interval: [123456000000000000, 123456999999999999] with key: key1
```

## Use Cases

### 1. BIN Range Lookup for Financial Transactions

In financial systems, BIN ranges are used to identify the issuing bank for credit and debit cards and some of the card's features. This tree can efficiently store and query BIN ranges, ensuring quick lookups during transaction processing.

### 2. IP Address Range Search

This implementation can also be adapted to store and search IP address ranges, allowing for quick identification of network blocks.

### 3. Date Range Queries

You can store and search for date ranges, which can be useful in applications like booking systems, where you need to check if a date falls within a certain range.

## Performance

Thanks to the self-balancing nature of AVL trees, this implementation is highly efficient for both insertion and search operations. Unlike Red-Black trees, which are approximately balanced, AVL trees maintain strict balance, ensuring the tree's height is minimized. This strict balancing results in more rotations during insertion, making AVL trees slightly more expensive to build. However, this additional overhead pays off during queries, as the tree's height is kept to a minimum, improving search performance.

This characteristic is particularly beneficial in scenarios like BIN number management, where data is periodically updated but queried frequently. In such cases, the AVL tree offers a superior balance between build time and query performance, ensuring that the time complexity for operations remains O(log n + m), where n is the number of elements in the tree, and m is the number of overlapping intervals that contain the point.

## License

This project is licensed under the MIT License. See the LICENSE file for details.


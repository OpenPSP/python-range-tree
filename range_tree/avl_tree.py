class RangeNode:
    """
    Represents a single node in the AVL tree.

    Attributes:
        start (int): The start value of the interval.
        end (int): The end value of the interval.
        max (int): The maximum end value in the subtree rooted at this node.
        height (int): The height of the node in the AVL tree.
        left (RangeNode): The left child node.
        right (RangeNode): The right child node.
        key (str): The unique key associated with the interval.
    """

    def __init__(self, start, end, key):
        """
        Initializes an RangeNode with a given interval.

        Args:
            start (int): The start value of the interval.
            end (int): The end value of the interval.
            key (str): The unique key associated with the interval.
        """
        self.start = start
        self.end = end
        self.max = end
        self.height = 1
        self.left = None
        self.right = None
        self.key = key


class RangeTree:
    """
    An augmented AVL tree for storing and querying intervals.

    This tree is self-balancing and allows efficient insertion and
    querying of intervals, with the ability to find the smallest interval
    that contains a given point.

    Attributes:
        root (RangeNode): The root of the AVL tree.
    """

    def __init__(self):
        """Initializes an empty RangeTree."""
        self.root = None

    def get_height(self, node):
        """
        Returns the height of a given node.

        Args:
            node (RangeNode): The node for which to get the height.

        Returns:
            int: The height of the node, or 0 if the node is None.
        """
        if not node:
            return 0
        return node.height

    def get_max(self, node):
        """
        Returns the maximum end value in the subtree rooted at a given node.

        Args:
            node (RangeNode): The node for which to get the maximum end value.

        Returns:
            int: The maximum end value in the subtree, or negative infinity if the node is None.
        """
        if not node:
            return float("-inf")
        return node.max

    def get_balance(self, node):
        """
        Computes the balance factor of a node.

        The balance factor is the difference between the heights of the left and right subtrees.

        Args:
            node (RangeNode): The node for which to get the balance factor.

        Returns:
            int: The balance factor, or 0 if the node is None.
        """
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def left_rotate(self, x):
        """
        Performs a left rotation on the subtree rooted at the given node.

        This operation is used to rebalance the tree when it becomes right-heavy.

        Args:
            z (RangeNode): The root of the subtree to rotate.

        Returns:
            RangeNode: The new root of the rotated subtree.
        """
        z = x.right
        T1 = z.left

        # Perform rotation
        z.left = x
        x.right = T1

        # Update heights
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))

        # Update max values
        x.max = max(x.end, self.get_max(x.left), self.get_max(x.right))
        z.max = max(z.end, self.get_max(z.left), self.get_max(z.right))

        return z

    def right_rotate(self, x):
        """
        Performs a right rotation on the subtree rooted at the given node.

        This operation is used to rebalance the tree when it becomes left-heavy.

        Args:
            x (RangeNode): The root of the subtree to rotate.

        Returns:
            RangeNode: The new root of the rotated subtree.
        """
        z = x.left
        T2 = z.right

        # Perform rotation
        z.right = x
        x.left = T2

        # Update heights
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))

        # Update max values
        x.max = max(x.end, self.get_max(x.left), self.get_max(x.right))
        z.max = max(z.end, self.get_max(z.left), self.get_max(z.right))

        return z

    def insert_node(self, node, start, end, key):
        """
        Recursively inserts a new interval into the subtree rooted at the given node.

        This function ensures the AVL tree properties are maintained by performing rotations as needed.

        Args:
            node (RangeNode): The root of the subtree where the interval should be inserted.
            start (int): The start value of the interval.
            end (int): The end value of the interval.
            key (str): The key associated with the interval.

        Returns:
            RangeNode: The root of the subtree after insertion.
        """
        # Base case: empty subtree
        if not node:
            return RangeNode(start, end, key)

        # Recursively insert into the left or right subtree
        if start < node.start:
            node.left = self.insert_node(node.left, start, end, key)
        else:
            node.right = self.insert_node(node.right, start, end, key)

        # Update max value
        node.max = max(node.end, self.get_max(node.left), self.get_max(node.right))

        # Update height
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

        # Get the balance factor to check whether this node became unbalanced
        balance = self.get_balance(node)

        # If the node is unbalanced, then there are 4 cases
        # you can find more information at https://youtu.be/m50vMHEfxKE

        # Left Left Case
        if balance > 1 and start < node.left.start:
            return self.right_rotate(node)

        # Right Right Case
        if (
            balance < -1 and start >= node.right.start
        ):  # if we insert several times the same range, it always goes to the right, so we need to rebalance when start = node.right.start
            return self.left_rotate(node)

        # Left Right Case
        if balance > 1 and start > node.left.start:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # Right Left Case
        if balance < -1 and start < node.right.start:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def insert(self, start, end, key):
        """
        Inserts a new interval into the AVL tree.

        Args:
            start (int): The start value of the interval.
            end (int): The end value of the interval.
            key (str): The key associated with the interval.
        """
        self.root = self.insert_node(self.root, start, end, key)

    def search_min_range(self, node, point):
        """
        Recursively searches for the smallest interval that contains a given point
        in the subtree rooted at the given node.

        The root node has priority over the subtrees if they have the same size.

        Args:
            node (IntervalNode): The root of the subtree to search.
            point (int): The point to find an interval for.

        Returns:
            IntervalNode: The node representing the smallest interval containing
            the point, or None if no such interval exists.
        """
        if not node:
            return None

        # Check if the current node's interval contains the point
        if node.start <= point <= node.end:
            min_node = node
            left_node = self.search_min_range(node.left, point)

            # Check if a smaller interval exists in the left subtree
            if left_node and (
                left_node.end - left_node.start < min_node.end - min_node.start
            ):
                min_node = left_node

            # Only search the right subtree if there's a chance to find a smaller interval
            if node.right and point <= self.get_max(node.right):
                right_node = self.search_min_range(node.right, point)

                # Check if a smaller interval exists in the right subtree
                if right_node and (
                    right_node.end - right_node.start < min_node.end - min_node.start
                ):
                    min_node = right_node

            return min_node
        elif point < node.start:
            # The point is less than the current node's start, so we should search the left subtree
            return self.search_min_range(node.left, point)
        else:
            # The point is greater than the current node's end, so we should search the right subtree
            # Only if the point is within the max range of the right subtree
            if node.right and point <= self.get_max(node.right):
                return self.search_min_range(node.right, point)
        return None

    def search(self, point):
        """
        Searches for the smallest interval that contains a given point in the entire tree.

        Args:
            point (int): The point to find an interval for.

        Returns:
            tuple: A tuple (start, end) representing the smallest interval containing the point, or None if no such interval exists.
        """
        node = self.search_min_range(self.root, point)
        if node:
            return (node.start, node.end, node.key)
        return None

    def in_order_traversal(self, node):
        """
        In-order traversal of the tree, which prints nodes in ascending order of start values.

        Args:
            node (IntervalNode): The current node to start the traversal from.
        """
        if node:
            self.in_order_traversal(node.left)
            print(
                f"Interval: [{node.start}, {node.end}], Key: {node.key}, Max: {node.max}, Height: {node.height}"
            )
            self.in_order_traversal(node.right)

    def pre_order_traversal(self, node):
        """
        Pre-order traversal of the tree, which prints nodes in the order they are processed.

        Args:
            node (IntervalNode): The current node to start the traversal from.
        """
        if node:
            print(
                f"Interval: [{node.start}, {node.end}], Key: {node.key}, Max: {node.max}, Height: {node.height}"
            )
            self.pre_order_traversal(node.left)
            self.pre_order_traversal(node.right)

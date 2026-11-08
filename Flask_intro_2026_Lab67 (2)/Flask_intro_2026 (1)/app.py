from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


# HOME AND OTHER PAGES

@app.route("/")
def home():
    return render_template("index.html", title="Home")


@app.route("/profile")
def profile():
    return render_template("profile.html", title="Profile")


@app.route("/works")
def works():
    return render_template("works.html", title="Works")


@app.route("/contacts")
def contacts():
    return render_template("contacts.html", title="Contacts")


@app.route("/uppercase")
def uppercase():
    return render_template("uppercase.html", title="To Uppercase")


@app.route("/circle")
def circle():
    return render_template("circle.html", title="Area of a Circle")


@app.route("/triangle")
def triangle():
    return render_template("triangle.html", title="Area of a Triangle")


@app.route("/linked-list")
def linked_list():
    return render_template("linked_list.html", title="Linked List Operations")


@app.route("/infix-postfix")
def infix_postfix():
    return render_template("infix_postfix.html", title="Infix to Postfix")


@app.route("/stack")
def stack():
    return render_template("stack.html", title="Stack Operations")


@app.route("/queue-deque")
def queue_deque():
    return render_template("queue_deque.html", title="Queues and Deques")


@app.route("/quick-sort")
def quick_sort():
    return render_template("quick_sort.html", title="Quick Sort")


# ==================================
# BINARY TREE
# ==================================

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class BinarySearchTree:

    # SORTING RULE: NUMBERS FIRST, THEN LETTERS
    def sort_key(self, key):
        value = str(key).strip()

        try:
            number = float(value)

            if number == float("inf") or number == float("-inf"):
                raise ValueError

            return (0, number)

        except ValueError:
            return (1, value.casefold())

    # INSERT
    def insert(self, root, key):
        if root is None:
            return Node(key)

        if self.sort_key(key) < self.sort_key(root.key):
            root.left = self.insert(root.left, key)

        elif self.sort_key(key) > self.sort_key(root.key):
            root.right = self.insert(root.right, key)

        return root

    # SEARCH
    def search(self, root, key):
        if root is None:
            return None

        if self.sort_key(key) == self.sort_key(root.key):
            return root

        if self.sort_key(key) < self.sort_key(root.key):
            return self.search(root.left, key)

        return self.search(root.right, key)

    # POSTORDER TRAVERSAL
    def post_traversal(self, start, traversal):
        if start:
            self.post_traversal(start.left, traversal)
            self.post_traversal(start.right, traversal)
            traversal.append(start.key)

        return traversal

    # FIND SMALLEST NODE
    def min_value(self, root):
        current = root

        while current.left:
            current = current.left

        return current

    # DELETE NODE
    def delete_node(self, root, key):
        if root is None:
            return root

        if self.sort_key(key) < self.sort_key(root.key):
            root.left = self.delete_node(root.left, key)

        elif self.sort_key(key) > self.sort_key(root.key):
            root.right = self.delete_node(root.right, key)

        else:
            if root.left is None:
                return root.right

            elif root.right is None:
                return root.left

            successor = self.min_value(root.right)
            root.key = successor.key
            root.right = self.delete_node(
                root.right, successor.key
            )

        return root


# CREATE TREE
tree = BinarySearchTree()
root = None


# CONVERT TREE TO JSON
def tree_to_dict(node):
    if node is None:
        return None

    return {
        "key": node.key,
        "left": tree_to_dict(node.left),
        "right": tree_to_dict(node.right)
    }


# GET AND VALIDATE INPUT
def get_tree_key():
    data = request.get_json(silent=True) or {}
    key = str(data.get("key", "")).strip()

    if not key:
        return None

    return key


# BINARY TREE PAGE
@app.route("/binary-tree")
def binary_tree():
    return render_template("binary_tree.html", title="Binary Tree")


# INSERT
@app.route("/binary-tree/insert", methods=["POST"])
def insert_value():
    global root

    key = get_tree_key()

    if key is None:
        return jsonify({"message": "Please enter a value."}), 400

    if tree.search(root, key):
        return jsonify({
            "message": "Value already exists.",
            "tree": tree_to_dict(root)
        })

    root = tree.insert(root, key)

    return jsonify({
        "message": f"{key} inserted successfully!",
        "tree": tree_to_dict(root)
    })


# SEARCH
@app.route("/binary-tree/search", methods=["POST"])
def search_value():
    key = get_tree_key()

    if key is None:
        return jsonify({"message": "Please enter a value."}), 400

    found = tree.search(root, key)

    return jsonify({
        "message": f"{key} found in the tree!"
        if found else f"{key} not found."
    })


# DELETE
@app.route("/binary-tree/delete", methods=["POST"])
def delete_value():
    global root

    key = get_tree_key()

    if key is None:
        return jsonify({"message": "Please enter a value."}), 400

    if tree.search(root, key) is None:
        return jsonify({
            "message": f"{key} does not exist.",
            "tree": tree_to_dict(root)
        })

    root = tree.delete_node(root, key)

    return jsonify({
        "message": f"{key} deleted successfully!",
        "tree": tree_to_dict(root)
    })


# POSTORDER TRAVERSAL
@app.route("/binary-tree/postorder")
def postorder():
    traversal = tree.post_traversal(root, [])

    return jsonify({"traversal": traversal})


# CLEAR TREE
@app.route("/binary-tree/clear", methods=["POST"])
def clear_tree():
    global root
    root = None

    return jsonify({
        "message": "Tree cleared successfully!",
        "tree": None
    })

# RUN FLASK APP
if __name__ == "__main__":
    app.run(debug=True)

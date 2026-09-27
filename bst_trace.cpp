#include <iostream>
#include <vector>

struct Node {
    int value;
    Node* left;
    Node* right;
    Node(int val) : value(val), left(nullptr), right(nullptr) {}
};

class BST {
private:
    Node* root;

    void printPath(const std::vector<int>& path) {
        std::cout << " [Camino: ";
        for (size_t i = 0; i < path.size(); ++i) {
            std::cout << path[i] << (i + 1 < path.size() ? " -> " : "");
        }
        std::cout << "]";
    }

    Node* insertRecursive(Node* node, int val, std::vector<int>& path) {
        if (node == nullptr) {
            std::cout << "Insertado " << val;
            printPath(path);
            std::cout << std::endl;
            return new Node(val);
        }
        path.push_back(node->value);
        if (val < node->value) {
            node->left = insertRecursive(node->left, val, path);
        } else if (val > node->value) {
            node->right = insertRecursive(node->right, val, path);
        }
        return node;
    }

    Node* findMin(Node* node) {
        while (node->left != nullptr) node = node->left;
        return node;
    }

    Node* deleteRecursive(Node* node, int val, std::vector<int>& path, bool& found) {
        if (node == nullptr) return nullptr;

        path.push_back(node->value);

        if (val < node->value) {
            node->left = deleteRecursive(node->left, val, path, found);
        } else if (val > node->value) {
            node->right = deleteRecursive(node->right, val, path, found);
        } else {
            found = true;
            if (node->left == nullptr) {
                Node* temp = node->right;
                delete node;
                return temp;
            } else if (node->right == nullptr) {
                Node* temp = node->left;
                delete node;
                return temp;
            }
            Node* temp = findMin(node->right);
            node->value = temp->value;
            bool dummyFound = false;
            std::vector<int> dummyPath;
            node->right = deleteRecursive(node->right, temp->value, dummyPath, dummyFound);
        }
        return node;
    }

    void inorderRecursive(Node* node) {
        if (node == nullptr) return;
        inorderRecursive(node->left);
        std::cout << node->value << " ";
        inorderRecursive(node->right);
    }

    void preorderRecursive(Node* node) {
        if (node == nullptr) return;
        std::cout << node->value << " ";
        preorderRecursive(node->left);
        preorderRecursive(node->right);
    }

    void postorderRecursive(Node* node) {
        if (node == nullptr) return;
        postorderRecursive(node->left);
        postorderRecursive(node->right);
        std::cout << node->value << " ";
    }

public:
    BST() : root(nullptr) {}

    void insert(int val) {
        std::vector<int> path;
        root = insertRecursive(root, val, path);
    }

    bool search(int val) {
        std::vector<int> path;
        Node* curr = root;
        while (curr != nullptr) {
            path.push_back(curr->value);
            if (curr->value == val) {
                std::cout << "Busqueda de " << val << ": ENCONTRADO";
                printPath(path);
                std::cout << std::endl;
                return true;
            }
            curr = (val < curr->value) ? curr->left : curr->right;
        }
        std::cout << "Busqueda de " << val << ": NO ENCONTRADO";
        printPath(path);
        std::cout << std::endl;
        return false;
    }

    void remove(int val) {
        std::vector<int> path;
        bool found = false;
        root = deleteRecursive(root, val, path, found);
        if (found) {
            std::cout << "Eliminado " << val;
            printPath(path);
            std::cout << std::endl;
        } else {
            std::cout << "No se pudo eliminar " << val << " (no existe)" << std::endl;
        }
    }

    void inorder() {
        std::cout << "Inorden:  ";
        inorderRecursive(root);
        std::cout << std::endl;
    }

    void preorder() {
        std::cout << "Preorden: ";
        preorderRecursive(root);
        std::cout << std::endl;
    }

    void postorder() {
        std::cout << "Postorden: ";
        postorderRecursive(root);
        std::cout << std::endl;
    }
};

int main() {
    BST tree;

    std::cout << "=== INSERCIONES ===" << std::endl;
    tree.insert(8);
    tree.insert(3);
    tree.insert(10);
    tree.insert(1);
    tree.insert(6);
    tree.insert(14);
    tree.insert(4);
    tree.insert(9);

    std::cout << "\n=== BUSQUEDA ===" << std::endl;
    tree.search(9);

    std::cout << "\n=== ELIMINACIONES ===" << std::endl;
    tree.remove(1);
    tree.remove(4);
    tree.remove(6);

    std::cout << "\n=== RECORRIDOS FINALES ===" << std::endl;
    tree.inorder();
    tree.preorder();
    tree.postorder();

    return 0;
}
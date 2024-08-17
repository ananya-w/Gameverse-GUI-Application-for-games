import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

# Decision Tree Classifier code here...
import numpy as np
import matplotlib.pyplot as plt

class Node:
    def __init__(self, feature_index=None, threshold=None, left=None, right=None, value=None):
        self.feature_index = feature_index
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value  # For leaf nodes, it stores the class label

class CARTDecisionTreeClassifier:
    def __init__(self, max_depth=None):
        self.max_depth = max_depth

    def fit(self, X, y):
        self.n_classes = len(np.unique(y))
        self.n_features = X.shape[1]
        self.tree = self._grow_tree(X, y)

    def _grow_tree(self, X, y, depth=0):
        n_samples, n_features = X.shape
        n_samples_per_class = [np.sum(y == i) for i in range(self.n_classes)]
        majority_class = np.argmax(n_samples_per_class)

        # Stopping criteria
        if (self.max_depth is not None and depth >= self.max_depth) or np.all(y == y[0]):
            return Node(value=majority_class)

        # Find the best split
        best_gini = np.inf
        best_feature_index = None
        best_threshold = None
        for feature_index in range(n_features):
            thresholds = np.unique(X[:, feature_index])
            for threshold in thresholds:
                left_indices = np.where(X[:, feature_index] <= threshold)[0]
                right_indices = np.where(X[:, feature_index] > threshold)[0]
                gini = self._gini_impurity(y[left_indices], y[right_indices])
                if gini < best_gini:
                    best_gini = gini
                    best_feature_index = feature_index
                    best_threshold = threshold

        # Split the data
        left_indices = np.where(X[:, best_feature_index] <= best_threshold)[0]
        right_indices = np.where(X[:, best_feature_index] > best_threshold)[0]
        left_subtree = self._grow_tree(X[left_indices, :], y[left_indices], depth + 1)
        right_subtree = self._grow_tree(X[right_indices, :], y[right_indices], depth + 1)

        return Node(feature_index=best_feature_index, threshold=best_threshold, left=left_subtree, right=right_subtree)

    def _gini_impurity(self, left_y, right_y):
        n_left = len(left_y)
        n_right = len(right_y)
        n_total = n_left + n_right
        p_left = np.sum(left_y == np.argmax(np.bincount(left_y))) / n_left if n_left > 0 else 0
        p_right = np.sum(right_y == np.argmax(np.bincount(right_y))) / n_right if n_right > 0 else 0
        gini = 1.0 - (p_left ** 2 + (1 - p_left) ** 2) - (p_right ** 2 + (1 - p_right) ** 2)
        return gini

    def _predict_sample(self, x, tree):
        if tree.value is not None:
            return tree.value
        feature_value = x[tree.feature_index]
        if feature_value <= tree.threshold:
            return self._predict_sample(x, tree.left)
        else:
            return self._predict_sample(x, tree.right)

    def predict(self, X):
        predictions = []
        for x in X:
            predictions.append(self._predict_sample(x, self.tree))
        return np.array(predictions)

    def visualize_tree(self, X, y):
        fig, ax = plt.subplots(figsize=(10, 6))
        text_pos = {}
        self._visualize_tree_recursive(ax, X, y, self.tree, text_pos)
        plt.show()

    def _visualize_tree_recursive(self, ax, X, y, node, text_pos, depth=0, position=(0, 0), parent_node=None, split_text=None):
        if node.value is not None:
            ax.text(position[0], position[1], f'Class: {node.value}\nCount: {np.sum(y == node.value)}', fontsize=12, ha='center', bbox=dict(facecolor='lightgray', edgecolor='black', boxstyle='round,pad=0.5'))
            return

        feature_index = node.feature_index
        threshold = node.threshold

        if depth not in text_pos:
            text_pos[depth] = {}

        if parent_node is not None:
            if parent_node.left == node:
                text_pos[depth][position] = (position[0] - 0.05, position[1] - 0.1)
            else:
                text_pos[depth][position] = (position[0] + 0.05, position[1] - 0.1)

        left_indices = np.where(X[:, feature_index] <= threshold)[0]
        right_indices = np.where(X[:, feature_index] > threshold)[0]
        
        ax.text(position[0], position[1], f'X[{feature_index}] <= {threshold}\nGini: {self._gini_impurity(y[left_indices], y[right_indices]):.2f}', fontsize=10, ha='center')

        left_subtree = node.left
        right_subtree = node.right

        if left_subtree is not None:
            ax.plot([position[0], position[0] - 0.2], [position[1] - 0.2, position[1] - 0.4], 'k-')
            self._visualize_tree_recursive(ax, X, y, left_subtree, text_pos, depth + 1, (position[0] - 0.2, position[1] - 0.4), node, 'left')

        if right_subtree is not None:
            ax.plot([position[0], position[0] + 0.2], [position[1] - 0.2, position[1] - 0.4], 'k-')
            self._visualize_tree_recursive(ax, X, y, right_subtree, text_pos, depth + 1, (position[0] + 0.2, position[1] - 0.4), node, 'right')

# Function to input custom data
def input_custom_data(n_features):
    custom_data = []
    print("Enter values for each feature:")
    for i in range(n_features):
        while True:
            try:
                val = float(input(f"Feature {i+1}: "))
                break
            except ValueError:
                print("Please enter a valid numerical value.")
        custom_data.append(val)
    return np.array(custom_data).reshape(1, -1)

# Example usage:
X_train = np.array([
    [2.0, 2.0, 3.0],  # Sample 1 with three features
    [2.0, 3.0, 4.0],  # Sample 2 with three features
    [3.0, 2.0, 5.0],  # Sample 3 with three features
    # Add more samples with three features
])

y_train = np.array([0, 0, 0, 1, 1, 1])
tree = CARTDecisionTreeClassifier(max_depth=2)
tree.fit(X_train, y_train)

# Input custom data
custom_data = input_custom_data(X_train.shape[1])

# Predict using the tree
prediction = tree.predict(custom_data)
print("Prediction:", prediction)

# Visualize the tree
tree.visualize_tree(X_train, y_train)

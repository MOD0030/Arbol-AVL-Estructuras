import sys

# Clase que representa un nodo del árbol AVL
class Node:
    def __init__(self, value):
        self.value = value          # Valor del nodo
        self.left = None            # Hijo izquierdo
        self.right = None           # Hijo derecho
        self.height = 1             # Altura del nodo (1 por ser hoja inicialmente)

# Retorna la altura de un nodo (0 si es None)
def getHeight(node):
    if not node:
        return 0
    return node.height

# Calcula el balance del nodo: altura derecha - izquierda
def getBalance(node): 
    if not node:
        return 0
    return getHeight(node.right) - getHeight(node.left)

# Actualiza la altura del nodo en base a sus hijos
def updateHeight(node):
    if node:
        node.height = 1 + max(getHeight(node.left), getHeight(node.right))

# Rotación simple a la derecha
def rotate_right(y):
    x = y.left                     # 'x' será la nueva raíz del subárbol
    if not x:
        return y                   # No se puede rotar si no hay hijo izquierdo

    T2 = x.right                   # 'T2' se mueve al hijo izquierdo de 'y'

    x.right = y                    # Realiza la rotación
    y.left = T2

    updateHeight(y)               # Actualiza alturas
    updateHeight(x)

    return x                      # Retorna la nueva raíz del subárbol

# Rotación simple a la izquierda
def rotate_left(x):
    y = x.right                    # 'y' será la nueva raíz del subárbol
    if not y:
        return x                   # No se puede rotar si no hay hijo derecho

    T2 = y.left                    # 'T2' se mueve al hijo derecho de 'x'

    y.left = x                     # Realiza la rotación
    x.right = T2

    updateHeight(x)               # Actualiza alturas
    updateHeight(y)

    return y                      # Retorna la nueva raíz del subárbol

# Clase principal del árbol AVL
class AVLTree:
    def __init__(self):
        self.root = None           # Árbol inicialmente vacío

    # Inserta un valor en el árbol
    def insert(self, value):
        self.root = self._insert_recursive(self.root, value)

    # Inserción recursiva con rebalanceo
    def _insert_recursive(self, node, value):
        if not node:
            return Node(value)     # Inserta nuevo nodo si no existe

        if value < node.value:
            node.left = self._insert_recursive(node.left, value)
        elif value > node.value:
            node.right = self._insert_recursive(node.right, value)
        else:
            return node            # No se permiten duplicados

        updateHeight(node)         # Actualiza altura tras inserción

        balance = getBalance(node) # Obtiene el balance del nodo

        # Casos de rotación para rebalancear

        # Izquierda Izquierda
        if balance > 1 and getBalance(node.left) >= 0:
            return rotate_right(node)

        # Izquierda Derecha
        elif balance > 1 and getBalance(node.left) < 0:
            node.left = rotate_left(node.left)
            return rotate_right(node)

        # Derecha Derecha
        elif balance < -1 and getBalance(node.right) <= 0:
            return rotate_left(node)

        # Derecha Izquierda
        elif balance < -1 and getBalance(node.right) > 0:
            node.right = rotate_right(node.right)
            return rotate_left(node)

        return node  # Retorna el nodo sin rotación si está balanceado

    # Recorrido inorden del árbol
    def inorder(self, node):
        if node:
            self.inorder(node.left)
            print(node.value, end=" ")
            self.inorder(node.right)

    # Encuentra el nodo con valor mínimo (usado en eliminación)
    def _min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    # Elimina un valor del árbol
    def delete(self, value):
        self.root = self._delete_recursive(self.root, value)

    # Eliminación recursiva con rebalanceo
    def _delete_recursive(self, node, value):
        if not node:
            return node

        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            # Nodo con un solo hijo o sin hijos
            if not node.left:
                temp = node.right
                node = None
                return temp
            elif not node.right:
                temp = node.left
                node = None
                return temp

            # Nodo con dos hijos: obtiene el sucesor inorden
            temp = self._min_value_node(node.right)
            node.value = temp.value
            node.right = self._delete_recursive(node.right, temp.value)

        if not node:
            return node

        updateHeight(node)
        balance = getBalance(node)

        # Casos de rebalanceo

        # Izquierda Izquierda
        if balance > 1 and getBalance(node.left) >= 0:
            return rotate_right(node)

        # Izquierda Derecha
        elif balance > 1 and getBalance(node.left) < 0:
            node.left = rotate_left(node.left)
            return rotate_right(node)

        # Derecha Derecha
        elif balance < -1 and getBalance(node.right) <= 0:
            return rotate_left(node)

        # Derecha Izquierda
        elif balance < -1 and getBalance(node.right) > 0:
            node.right = rotate_right(node.right)
            return rotate_left(node)

        return node



# Crear el árbol AVL e insertar elementos
avl = AVLTree()
values_to_insert = [10, 20, 30, 40, 50, 25]

for val in values_to_insert:
    avl.insert(val)

# Mostrar el árbol en orden (de menor a mayor)
print("Recorrido Inorden del Árbol AVL:")
avl.inorder(avl.root)

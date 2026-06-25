class NodoABB:
    def __init__(self, partida):
        self.partida = partida # recibe y almacena referencia a un objeto Partida (datos)
        self.type = partida.difficulty
        self.left = None # referencia al nodo hijo izquierdo
        self.right = None # referencia al nodo hijo derecho

    def get_time(self):
        return self.partida.time

class ABB:
    def __init__(self):
        self.root = None # referencia del nodo raíz, inicialmente no hay raíz
    
    def insertar_nodo(self,partida):
        self.root = self.insertar_nodo(partida, self.root)

    # esta lógica debe ser recursiva, el dato    
    # que sirve para el ordenamiento es el tiempo que tardó en completar la partida.
    # Note que los nodos tipo NodoABB se crean dentro de este método, así se mantiene
    # la implementación del árbol encapsulada en la clase ABB    
    def insertar_nodo(self, partida, node):
        if (node == None):
            return NodoABB(partida)

        if(partida.time > node.get_time()):
            node.right = self.insertar_nodo(partida, node.right)
        elif(partida.time < node.get_time()):
            node.left = self.insertar_nodo(partida,node.left)
        return
    
    # esta lógica debe ser recursiva, el recorrido es
    # en-orden para que las partidas se desplieguen en forma ascendente (de menor a
    # mayor). Dentro de este método se llama a get_partida para obtener los datos que
    # se van a desplegar de la partida
    def recorrer_arbol(self):
        rt = self.root        
        self.recorrer_arbol()
        return

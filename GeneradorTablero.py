import random
import copy

class GeneradorSudoku:
    def __init__(self):
        # Inicializamos un tablero vacío (9x9 lleno de ceros)
        self.tablero = [[0 for _ in range(9)] for _ in range(9)]
        
    def generar_tablero_completo(self):
        """Llena el tablero respetando todas las reglas del Sudoku usando Backtracking."""
        celda_vacia = self._buscar_celda_vacia()
        if not celda_vacia:
            return True
            
        fila, col = celda_vacia
        numeros = list(range(1, 10))
        random.shuffle(numeros)

        for num in numeros:
            if self._es_valido(fila, col, num):
                self.tablero[fila][col] = num

                if self.generar_tablero_completo():
                    return True
                
                self.tablero[fila][col] = 0

        return False  

    def _buscar_celda_vacia(self):
        """Devuelve las coordenadas (fila, col) de la primera celda con 0."""
        for f in range(9):
            for c in range(9):
                if self.tablero[f][c] == 0:
                    return f, c
        return None

    def _es_valido(self, fila, col, num):
        """Verifica si un número puede ser colocado en la posición indicada."""
        if num in self.tablero[fila]:
            return False

        # Validar Columna
        if num in [self.tablero[f][col] for f in range(9)]:
            return False

        box_fila = (fila // 3) * 3
        box_col = (col // 3) * 3
        for f in range(box_fila, box_fila + 3):
            for c in range(box_col, box_col + 3):
                if self.tablero[f][c] == num:
                    return False

        return True

    def crear_tablero_juego(self,tablero_resuelto, dificultad="facil"):
        """
        Toma una matriz de 9x9 resuelta y devuelve una nueva matriz 
        con casillas en -1 según el nivel de dificultad.
        """
        tablero_juego = copy.deepcopy(tablero_resuelto)
        
        dificultades = {
            "facil": random.randint(36, 41),       # ~42 pistas visibles
            "intermedio": random.randint(46, 49),  # ~33 pistas visibles
            "dificil": random.randint(53, 57)      # ~26 pistas visibles
        }
        
        dificultad = dificultad.lower()
        if dificultad not in dificultades:
            dificultad = "facil"
            
        casillas_a_borrar = dificultades[dificultad]
        
        borradas = 0
        while borradas < casillas_a_borrar:
            fila = random.randint(0, 8)
            col = random.randint(0, 8)
            
            if tablero_juego[fila][col] != -1:
                tablero_juego[fila][col] = -1  # Establecemos la casilla en blanco
                borradas += 1
                
        return tablero_juego

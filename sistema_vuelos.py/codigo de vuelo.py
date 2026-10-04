import heapq
import time
import os

class GrafoVuelos:
    def __init__(self):
        self.grafo = {}

    def cargar_desde_archivo(self, ruta_archivo):
        if not os.path.exists(ruta_archivo):
            print(f"Error: El archivo {ruta_archivo} no existe.")
            return False
        
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            for linea in f:
                linea = linea.strip()
                if linea and not linea.startswith('#'):
                    partes = linea.split(',')
                    if len(partes) == 3:
                        origen, destino, costo = partes[0].strip(), partes[1].strip(), float(partes[2].strip())
                        self.agregar_vuelo(origen, destino, costo)
        return True

    def agregar_vuelo(self, origen, destino, costo):
        if origen not in self.grafo:
            self.grafo[origen] = []
        if destino not in self.grafo:
            self.grafo[destino] = []
        self.grafo[origen].append((destino, costo))

    def mostrar_reporteria(self):
        print("\n" + "="*50)
        print("          REPORTE DE LA RED DE VUELOS")
        print("="*50)
        total_rutas = 0
        for origen, conexiones in self.grafo.items():
            print(f"\nAeropuerto Origen: [{origen}]")
            if not conexiones:
                print("  └── Sin vuelos salientes registrados.")
            for dest, costo in conexiones:
                print(f"  └── Destino: {dest:<12} | Costo: ${costo:.2f}")
                total_rutas += 1
        print("-" * 50)
        print(f"Total de Aeropuertos (Nodos): {len(self.grafo)}")
        print(f"Total de Rutas (Aristas): {total_rutas}")
        print("="*50 + "\n")

    def buscar_vuelo_mas_barato(self, origen, destino):
        if origen not in self.grafo or destino not in self.grafo:
            return None, float('inf')

        distancias = {nodo: float('inf') for nodo in self.grafo}
        predecesores = {nodo: None for nodo in self.grafo}
        distancias[origen] = 0
        
        pq = [(0, origen)]

        while pq:
            costo_actual, nodo_actual = heapq.heappop(pq)

            if costo_actual > distancias[nodo_actual]:
                continue

            if nodo_actual == destino:
                break

            for vecino, peso in self.grafo[nodo_actual]:
                distancia = costo_actual + peso
                if distancia < distancias[vecino]:
                    distancias[vecino] = distancia
                    predecesores[vecino] = nodo_actual
                    heapq.heappush(pq, (distancia, vecino))

        ruta = []
        curr = destino
        if distancias[destino] == float('inf'):
            return None, float('inf')

        while curr is not None:
            ruta.append(curr)
            curr = predecesores[curr]
        ruta.reverse()

        return ruta, distancias[destino]

if __name__ == "__main__":
    red = GrafoVuelos()
    
    if red.cargar_desde_archivo("vuelos.txt"):
        red.mostrar_reporteria()
        
        origen_p = "Quito"
        destino_p = "Galapagos"
        
        inicio = time.perf_counter()
        ruta_optima, costo_total = red.buscar_vuelo_mas_barato(origen_p, destino_p)
        fin = time.perf_counter()
        
        tiempo_ejecucion_ms = (fin - inicio) * 1000

        print(f"BÚSQUEDA DE RUTA OPTIMA: {origen_p} -> {destino_p}")
        if ruta_optima:
            print(f"Ruta más barata encontrada: {' -> '.join(ruta_optima)}")
            print(f"Costo total del trayecto: ${costo_total:.2f}")
        else:
            print("No existe una ruta disponible entre las ciudades especificadas.")
        
        print(f"Tiempo de ejecución del algoritmo: {tiempo_ejecucion_ms:.4f} ms")
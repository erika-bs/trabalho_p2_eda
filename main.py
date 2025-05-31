import openrouteservice
import os
from dotenv import load_dotenv
import folium
import heapq
from itertools import permutations

load_dotenv()
API_KEY = os.getenv("ORS_API_KEY")
client = openrouteservice.Client(key=API_KEY)

enderecos = {
    "Jacarepaguá (sede)": [-43.3856, -22.9195],
    "Guanabara 1": [-43.4668, -22.8787], 
    "Guanabara 2": [-43.3601, -23.0036],
    "Guanabara 3": [-43.2530, -22.8608], 
    "Guanabara 4": [-43.3653, -22.8809],
    "Guanabara 5": [-43.5700, -22.8855], 
    "Guanabara 6": [-43.2825, -22.8884],
    "Guanabara 7": [-43.3197, -22.8382], 
    "Guanabara 8": [-43.3063, -22.8532],
    "Guanabara 9": [-43.4207, -22.8849], 
    "Guanabara 10": [-43.2522, -22.9195],
    "Prezunic 1": [-43.2525, -22.9190], 
    "Prezunic 2": [-43.1829, -22.9507],
    "Prezunic 3": [-43.1931, -22.9308], 
    "Prezunic 4": [-43.2730, -22.8940],
    "Prezunic 5": [-43.2333, -22.9320], 
    "Prezunic 6": [-43.5555, -22.8800],
    "Prezunic 7": [-43.4560, -23.0122], 
    "Prezunic 8": [-43.4032, -22.9435],
    "Prezunic 9": [-43.2097, -22.8102], 
    "Prezunic 10": [-43.3011, -22.7859],
    "Supermarket 1": [-43.1862, -22.9500], 
    "Supermarket 2": [-43.1912, -22.9647],
    "Supermarket 3": [-43.2331, -22.9335], 
    "Supermarket 4": [-43.5706, -22.8893],
    "Supermarket 5": [-43.3391, -22.8730], 
    "Supermarket 6": [-43.3811, -22.8095],
    "Supermarket 7": [-43.1860, -22.9125], 
    "Supermarket 8": [-43.2023, -22.8980],
    "Supermarket 9": [-43.2522, -22.9195], 
    "Supermarket 10": [-43.2754, -22.8890],
    "Zona Sul 1": [-43.2236, -22.9816], 
    "Zona Sul 2": [-43.2110, -22.9853],
    "Zona Sul 3": [-43.1910, -22.9640], 
    "Zona Sul 4": [-43.1821, -22.9321],
    "Zona Sul 5": [-43.1865, -22.9491]
}

def calcular_distancia(coord1, coord2):
    rota = client.directions([coord1, coord2], profile='driving-car')
    return rota['routes'][0]['summary']['distance'] / 1000

def construir_grafo(locais):
    grafo = {l: {} for l in locais}
    for origem in locais:
        for destino in locais:
            if origem != destino:
                dist = calcular_distancia(enderecos[origem], enderecos[destino])
                grafo[origem][destino] = round(dist, 2)
    return grafo

def dijkstra(grafo, inicio):
    distancias = {no: float('inf') for no in grafo}
    distancias[inicio] = 0
    caminho = {no: None for no in grafo}
    fila = [(0, inicio)]

    while fila:
        dist_atual, atual = heapq.heappop(fila)

        for vizinho, peso in grafo[atual].items():
            nova_dist = dist_atual + peso
            if nova_dist < distancias[vizinho]:
                distancias[vizinho] = nova_dist
                caminho[vizinho] = atual
                heapq.heappush(fila, (nova_dist, vizinho))

    return distancias, caminho

def reconstruir_caminho(caminho, destino):
    rota = []
    atual = destino
    while caminho[atual] is not None:
        rota.append((caminho[atual], atual))
        atual = caminho[atual]
    rota.reverse()
    return rota

def desenhar_mapa(rotas, coord):
    mapa = folium.Map(location=coord["Jacarepaguá (sede)"][::-1], zoom_start=11)

    folium.Marker(
        location=coord["Jacarepaguá (sede)"][::-1],
        popup="Jacarepaguá (sede)",
        icon=folium.Icon(icon="building", prefix="fa", color="orange")
    ).add_to(mapa)

    for nome, pos in coord.items():
        if nome == "Jacarepaguá (sede)":
            continue

        if "Prezunic" in nome:
            cor = "gray"
        elif "Zona Sul" in nome:
            cor = "red"
        elif "Supermarket" in nome:
            cor = "green"
        elif "Guanabara" in nome:
            cor = "blue"
        else:
            cor = "lightgray"

        folium.Marker(
            location=pos[::-1],
            popup=nome,
            icon=folium.Icon(icon="shopping-cart", prefix="fa", color=cor)
        ).add_to(mapa)

    for origem, destino in rotas:
        rota = client.directions([coord[origem], coord[destino]], profile='driving-car', format='geojson')
        folium.GeoJson(rota, name=f"{origem} - {destino}").add_to(mapa)

    mapa.save("rota.html")
    print("Mapa salvo como: rota.html")


if __name__ == "__main__":
    print("\nLojas disponíveis:")
    for nome in enderecos:
        if nome != "Jacarepaguá (sede)":
            print(f" - {nome}")

    lojas = input("\nDigite até 3 lojas para entrega (separadas por vírgula):\n> ").split(",")
    lojas = [loja.strip() for loja in lojas if loja.strip() in enderecos and loja.strip() != "Jacarepaguá (sede)"]

    if not lojas or len(lojas) > 3:
        print("Entrada inválida. Escolha de 1 a 3 lojas.")
        exit()

    pontos = ["Jacarepaguá (sede)"] + lojas
    grafo = construir_grafo(pontos)

    melhor_rota = []
    menor_distancia = float('inf')

    for ordem in permutations(lojas):
        rota_atual = []
        distancia_total = 0
        ponto_atual = "Jacarepaguá (sede)"

        for loja in ordem:
            distancias, caminhos = dijkstra(grafo, ponto_atual)
            rota = reconstruir_caminho(caminhos, loja)
            rota_atual.extend(rota)
            distancia_total += distancias[loja]
            ponto_atual = loja

        distancias,caminhos = dijkstra(grafo,ponto_atual)
        rota_volta = reconstruir_caminho(caminhos,"Jacarepaguá (sede)")
        rota_atual.extend(rota_volta)
        distancia_total += distancias["Jacarepaguá (sede)"]

        if distancia_total < menor_distancia:
            menor_distancia = distancia_total
            melhor_rota = rota_atual

    print("\nRota otimizada:")
    for origem, destino in melhor_rota:
        print(f"{origem} → {destino} = {grafo[origem][destino]} km")
    print(f"\nDistância total: {round(menor_distancia, 2)} km")

    desenhar_mapa(melhor_rota, {p: enderecos[p] for p in pontos})

import openrouteservice
import os
from dotenv import load_dotenv
import folium
import heapq
from itertools import permutations
from enderecos import enderecos

load_dotenv()
API_KEY = os.getenv("ORS_API_KEY")
client = openrouteservice.Client(key=API_KEY)


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
    mapa = folium.Map(location=coord["Jacarepaguá (sede)"][::-1], zoom_start=11,tiles=None)

    folium.TileLayer(
        tiles = 'OpenStreetMap',
        name = 'Lojas',
        control=True
    ).add_to(mapa)

    folium.Marker(
        location=coord["Jacarepaguá (sede)"][::-1],
        popup="Jacarepaguá (sede)",
        icon=folium.Icon(icon="building", prefix="fa", color="orange")
    ).add_to(mapa)

    grupos = {
        "Prezunic": folium.FeatureGroup(name="Prezunic",show=True),
        "Zona Sul": folium.FeatureGroup(name="Zona Sul",show=True),
        "Supermarket": folium.FeatureGroup(name="Supermarket",show=True),
        "Guanabara":folium.FeatureGroup(name="Guanabara",show=True)
    }

    for nome, pos in coord.items():
        if nome == "Jacarepaguá (sede)":
            continue

        if "Prezunic" in nome:
            cor = "gray"
            grupo = grupos["Prezunic"]
        elif "Zona Sul" in nome:
            cor = "red"
            grupo = grupos["Zona Sul"]
        elif "Supermarket" in nome:
            cor = "green"
            grupo = grupos["Supermarket"]
        elif "Guanabara" in nome:
            cor = "blue"
            grupo = grupos["Guanabara"]
        else:
            cor = "lightgray"
            grupo = None

        if grupo:
            folium.Marker(
                location=pos[::-1],
                popup=nome,
                icon=folium.Icon(icon="shopping-cart",prefix="fa",color=cor)
            ).add_to(grupo)

    for grupo in grupos.values():
        grupo.add_to(mapa)

    visitados = ["Jacarepaguá (sede)"]

    for origem, destino in rotas:
        if destino not in visitados:
            visitados.append(destino)

        rota = client.directions([coord[origem], coord[destino]], profile='driving-car', format='geojson')
        cor = "blue" if destino != "Jacarepaguá (sede)" else "red"
        folium.GeoJson(rota, name=f"{origem} - {destino}", style_function=lambda x, c=cor: {"color": c, "weight": 4},control=False).add_to(mapa)

    for i, nome in enumerate(visitados[1:],start=1):
        folium.map.Marker(
            coord[nome][::-1],
            icon=folium.DivIcon(html=f"""
                                <div style="
                                background-color:#FF5722;
                                color:white;
                                font-size:14pt;
                                border-radius:50%;
                                width:30px;
                                height:30px;
                                display:flex;
                                align-items:center;
                                justify-content:center;
                                border-shadow:0 0 3px rgba(0,0,0,0.5);">
                                
                                <b>{i}</b>
                                
                                </div>
                                """)
        ).add_to(mapa)

    folium.LayerControl().add_to(mapa)
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
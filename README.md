## Sistema de Rotas para Entregas - Distribuidora de Vinhos

Este projeto em Python simula o planejamento de rotas de uma distribuidora de vinhos, cuja sede fica em Jacarepaguá - RJ. 

A empresa realiza em média até 3 entregas por dia, e o sistema permite selecionar quais lojas irão receber as mercadorias. 

Com base nas distâncias reais entre os pontos, a melhor rota é calculada automaticamente e exibida em um mapa.

## O que o sistema faz

- Permite que você escolha até 3 lojas para fazer entrega no dia
- Calcula a melhor ordem de visita usando o algoritmo de Dijkstra
- Gera um mapa com a rota (arquivo `rota.html`)

## Bibliotecas utilizadas

O projeto utiliza as seguintes bibliotecas Python:

- `openrouteservice` – para calcular a distância real entre os pontos usando a API do ORS
- `folium` – para gerar um mapa com a rota traçada
- `python-dotenv` – para carregar a chave da API do `.env`
- `requests` – usada internamente para as requisições à API
- `heapq` – módulo da biblioteca padrão do Python utilizado para implementar fila de prioridade no algoritmo de Dijkstra


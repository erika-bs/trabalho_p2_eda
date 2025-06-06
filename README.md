## Sistema de Rotas para Entregas - Distribuidora de Vinhos

Este projeto em Python simula o planejamento de rotas de uma distribuidora de vinhos, cuja sede fica em Jacarepaguá - RJ. 

A empresa realiza em média até 3 entregas por dia, geralmente 3 vezes na semana, e o sistema permite selecionar quais lojas irão receber as mercadorias. 

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
- `os` – Módulo padrão utilizado para acessar variáveis de ambiente, como a chave da API
- `heapq` – módulo da biblioteca padrão do Python utilizado para implementar fila de prioridade no algoritmo de Dijkstra
- `itertools` – Módulo padrão usado para gerar todas as permutações possíveis de visitas às lojas

## 🛠️ Como rodar

### Clone o repositório:
git clone https://github.com/erika-bs/trabalho_p2_eda.git

### Abra seu repositório
cd atividade_p2_eda

### Abra o código no VsCode
code .

### Abra o Terminal do VsCode e crie o ambiente virtual
python -m venv venv

### Ative a venv
venv\Scripts\activate

### Instale as dependências
pip install -r requirements.txt

### Rode o script
python main.py

### Abra o arquivo rota.html para visualizar o mapa

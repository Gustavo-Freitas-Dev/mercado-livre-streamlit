import requests
from bs4 import BeautifulSoup
from utils import limpar_dados
from time import sleep
import re

def requisicao(session, url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.RequestException:
        return None

def buscar_url_proxima_pagina(soup):
    proxima = soup.find('li', class_='andes-pagination__button--next')
    if proxima:
        link = proxima.find('a')
        return link['href'] if link and link.has_attr('href') else None
    return None

def extrair_preco_numerico(preco_str):
    preco_limpo = preco_str.replace(".", "").replace(",", "")
    preco_digitos = re.sub(r'[^\d]', '', preco_limpo)
    return int(preco_digitos) if preco_digitos else float('inf')

def raspagem(produto, paginas=5):
    dados = []
    url = f'https://lista.mercadolivre.com.br/{produto}'
    pagina_atual = 0
    session = requests.Session()

    while url and pagina_atual < paginas:
        print(f"🔍 Raspando página {pagina_atual + 1} - {url}")
        soup = requisicao(session, url)
        if not soup:
            print("❌ Erro ao carregar a página.")
            break

        cards = soup.find_all('li', class_='ui-search-layout__item')
        for card in cards:
            titulo_elem = card.find('a', class_='poly-component__title')
            preco_elem = card.find('span', class_='andes-money-amount__fraction')
            preco_centavos = card.find('span', class_='andes-money-amount__cents')

            titulo = limpar_dados(titulo_elem)
            preco = f"R$ {limpar_dados(preco_elem)}"
            if preco_centavos:
                preco += f",{limpar_dados(preco_centavos)}"
            else:
                preco += f",00" 

            preco_numerico = extrair_preco_numerico(preco)

            link = titulo_elem['href'] if titulo_elem and titulo_elem.has_attr('href') else "Sem link"
            dados.append({"Título": titulo, "Preço": preco, "Link": link, "Preço númerico": preco_numerico})

        pagina_atual += 1
        url = buscar_url_proxima_pagina(soup)

        if url:
            sleep(1)  # evita bloqueio e respeita o site

    return dados


if __name__ == "__main__":
    termo = "PS5" 
    produtos = raspagem(termo, paginas=2)
    ordenados = sorted(produtos, key=lambda x:x ["Preço númerico"])
    
    for produtos in ordenados:
        print(produtos['Título'])
        print(produtos['Preço'])
        print(produtos['Link'])
        print('---'*30)


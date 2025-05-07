def limpar_dados(texto):
    return texto.get_text(strip=True) if texto else "Não disponível"

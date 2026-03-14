import re
from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()

SEFAZ_URL = "http://nfce.sefaz.ce.gov.br/nfce/api/notasFiscal/qrcodev3/"


def buscar_nota(chave, versao="3", ambiente="1"):

    payload = {
        "chave_acesso": chave,
        "versao_qrcode": versao,
        "tipo_ambiente": ambiente
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json;charset=utf-8",
        "Referer": "http://nfce.sefaz.ce.gov.br/pages/ShowNFCe.html"
    }

    r = requests.post(SEFAZ_URL, json=payload, headers=headers)
    data = r.json()

    html = data["xml"]

    soup = BeautifulSoup(html, "html.parser")

    produtos = []
    cupom = {}

    mercado = soup.select_one(".txtTopo").text.strip() if soup.select_one(".txtTopo") else "Desconecido"
    enderecos = soup.select(".text")
    endereco = enderecos[1].text.strip() if enderecos else "Desconecido"
    info = soup.select_one("#infos li").get_text(" ", strip=True)
    match = re.search(r"\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}", info)
    data_emissao = match.group(0) if match else "Desconhecido"

    cupom["mercado"] = mercado
    cupom["endereco"] = endereco
    cupom["data_emissao"] = data_emissao
    
    cupom["subtotal"] = 0.0
    cupom["desconto"] = 0.0
    cupom["total"] = 0.0

    for div in soup.select("#totalNota > div"):
        label = div.select_one("label")
        valor = div.select_one(".totalNumb")

        if not label or not valor:
            continue

        texto = label.text.strip()
        numero = valor.text.replace("R$", "").replace(".", "").replace(",", ".").strip()

        try:
            numero = float(numero)
        except:
            continue

        if "Valor total" in texto:
            cupom["subtotal"] = numero

        elif "Descontos" in texto:
            cupom["desconto"] = numero

        elif "Valor a pagar" in texto:
            cupom["total"] = numero

    if cupom["subtotal"] == 0.0:
        cupom["subtotal"] = cupom["total"] + cupom["desconto"]


    for item in soup.select("#tabResult tr"):

        nome = item.select_one(".txtTit")
        cod = item.select_one(".RCod")
        qtd = item.select_one(".Rqtd")
        unit = item.select_one(".RUN")
        preco = item.select_one(".RvlUnit")
        total = item.select_one(".valor")

        if nome and qtd and preco:
            name = nome.text.title().strip()
            qtd_text = qtd.text.replace("Qtde.:", "").strip().replace(",", ".")
            preco_text = preco.text.replace("Vl. Unit.:", "").replace(".", "").replace(",", ".").strip()
            total_text = total.text.strip().replace("R$", "").replace(".", "").replace(",", ".").strip()
            codigo = cod.text.split(":")[1].replace(")", "").strip() if cod else None
            unidade = unit.text.split(":")[1].strip() if unit else None
            
            produtos.append({
                "name": name,
                "code": codigo,
                "quantity": float(qtd_text),
                "unit": unidade,
                "price": float(preco_text),
                "totalValue": float(total_text)
            })

    return produtos, cupom


@app.get("/nota/{chave}")
def consultar_nota(chave: str):

    produtos, cupom = buscar_nota(chave)

    return {
        "chave": chave,
        "produtos": produtos,
        "cupom": cupom
    }
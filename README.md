# 🧾 API de Cupom Fiscal

API REST para leitura e extração de dados de cupons fiscais eletrônicos (NFC-e) do Ceará. Consulte informações de produtos, valores e estabelecimento através da chave de acesso da nota fiscal.

## 📋 Sobre o Projeto

Esta API permite consultar cupons fiscais eletrônicos emitidos no Ceará através da chave de acesso de 44 dígitos. Ela busca os dados na SEFAZ-CE e retorna de forma estruturada:

- 🏪 **Dados do estabelecimento** (nome e endereço)
- 📅 **Data e hora de emissão**
- 🛒 **Lista de produtos** com código, nome, quantidade, preço unitário e total
- 💰 **Valores do cupom** (subtotal, descontos e total)

## 🚀 Tecnologias

- **FastAPI** - Framework web moderno e rápido
- **BeautifulSoup4** - Parser de HTML para extração de dados
- **Requests** - Cliente HTTP para comunicação com SEFAZ
- **Python 3.13+**

## 📦 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/api-cupom.git
cd api-cupom
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

## 🔧 Como Usar

### Executar localmente
```bash
uvicorn api:app --reload
```

A API estará disponível em: `http://localhost:8000`

### Acessar a documentação interativa

FastAPI gera documentação automática e interativa. Acesse:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

Em produção, substitua pelo seu domínio: `https://seu-projeto.vercel.app/docs`

### Fazer uma consulta
```bash
curl http://localhost:8000/nota/23260311497712000346651050000140211138967393
```

## 📡 Endpoints

### `GET /nota/{chave}`

Consulta um cupom fiscal pela chave de acesso.

**Parâmetros:**
- `chave` (string, obrigatório): Chave de acesso de 44 dígitos da NFC-e

**Exemplo de resposta:**
```json
{
  "chave": "23260311497712000346651050000140211138967393",
  "produtos": [
    {
      "name": "Arroz Branco 5Kg",
      "code": "7891234567890",
      "quantity": 2.0,
      "unit": "UN",
      "price": 15.90,
      "totalValue": 31.80
    },
    {
      "name": "Feijao Preto 1Kg",
      "code": "7891234567891",
      "quantity": 1.5,
      "unit": "KG",
      "price": 8.50,
      "totalValue": 12.75
    }
  ],
  "cupom": {
    "mercado": "Supermercado Exemplo Ltda",
    "endereco": "Rua Exemplo, 123 - Centro - Fortaleza/CE",
    "data_emissao": "14/03/2026 10:30:45",
    "subtotal": 44.55,
    "desconto": 0.0,
    "total": 44.55
  }
}
```

## ☁️ Deploy na Vercel

Este projeto está configurado para deploy serverless na Vercel.

### Passo a passo:

1. **Instale a CLI da Vercel**
```bash
npm install -g vercel
```

2. **Faça login**
```bash
vercel login
```

3. **Deploy**
```bash
vercel --prod
```

Sua API estará disponível em: `https://seu-projeto.vercel.app`

### Deploy via GitHub

1. Conecte seu repositório no [vercel.com](https://vercel.com)
2. A cada push, a Vercel fará deploy automático! 🎉

## 🔍 Como Obter a Chave de Acesso

A chave de acesso de 44 dígitos pode ser encontrada:
- No QR Code do cupom fiscal
- No corpo do cupom impresso
- Na URL do QR Code após escanear

Exemplo de QR Code da NFC-e:
```
http://nfce.sefaz.ce.gov.br/pages/ShowNFCe.html?p=23260311497712000346651050000140211138967393|2|1|1|...
```
A chave é o primeiro parâmetro após `?p=`

## 🛠️ Estrutura do Projeto

```
api-cupom/
├── api.py              # Código principal da API
├── requirements.txt    # Dependências Python
├── vercel.json        # Configuração Vercel
├── .gitignore         # Arquivos ignorados pelo Git
└── README.md          # Este arquivo
```

## 📝 Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Enviar pull requests

## ⚠️ Aviso Legal

Esta API utiliza dados públicos disponibilizados pela SEFAZ-CE. Use de forma responsável e de acordo com os termos de uso da SEFAZ.

---

Desenvolvido com ❤️ usando FastAPI

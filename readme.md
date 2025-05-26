# API CRECI DF / bug

Esta API foi desenvolvida para facilitar a obtenção de informações de regularidade de corretores utilizando o número CRECI. Ela interage com a API do CRECI DF para validar a certidão de regularidade de um corretor específico.

## Funcionalidades

- **Consulta de Informações de Corretor**: A rota `/creci_info/` permite buscar informações de um corretor utilizando o seu número CRECI.

## Requisitos

- Python 3.7 ou superior
- `pip` para gerenciamento de pacotes

## Iniciando a API

### 1. Clone o Repositório

```sh
git clone https://github.com/josuejuca/api-crecidf.git
cd api-crecidf
```

### 2. Instale as Dependências

Certifique-se de que você está no diretório raiz do projeto, onde o arquivo `requirements.txt` está localizado, e execute:

```sh
pip install -r requirements.txt
```

### 3. Inicie a API

Navegue até a pasta onde o arquivo `main.py` está localizado (se o arquivo se chama `main.py`):

```sh
cd app/
```

Inicie a API com o comando abaixo:

```sh
uvicorn api:app --reload
```

> O parâmetro `--reload` permite que o servidor recarregue automaticamente sempre que houver alterações no código.

### 4. Acesse a API

Abra o navegador ou use uma ferramenta como `curl` ou `Postman` para acessar:

[http://127.0.0.1:8000](http://127.0.0.1:8000)

## Documentação da API

Uma vez que a API esteja rodando, você pode acessar a documentação automática gerada pelo Swagger UI em:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Redoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)


## Exemplo de Requisição

Para consultar informações de um corretor, faça uma requisição `POST` para o endpoint `/creci_info/` com o número CRECI no corpo da requisição:

```sh
curl -X 'POST' \
  'http://127.0.0.1:8000/creci_info/?creci_number={CRECI}' \
  -H 'accept: application/json' \
  -d ''
```

## Licença

Este projeto é distribuído sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Contato

Para mais informações ou dúvidas, entre em contato:

- **Autor**: Josue Juca
- **Email**: [josuejuca19@gmail.com](mailto:josuejuca19@gmail.com)

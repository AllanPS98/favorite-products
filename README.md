# Favorite Products

API RESTful para gerenciamento de produtos favoritos de clientes.

## 🚀 Tecnologias Utilizadas

* **Python** – Linguagem principal
* **FastAPI** – Framework web
* **SQLAlchemy** – ORM para banco de dados
* **Alembic** – Migrations para banco de dados
* **Docker & Docker Compose** – Para containerização e desenvolvimento

## 🛠️ Instalação

Clone o repositório:

```bash
git clone https://github.com/AllanPS98/favorite-products.git
cd favorite-products
```

Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## 🐳 Rodando com Docker

Use o `docker-compose` para subir o ambiente:

```bash
docker-compose up --build
```

OBS: crie um `.env`

```bash
DB_HOST="db"
MODE="app"
```

O serviço ficará disponível em `http://localhost:8000`.

## 🧪 Testes

Para rodar os testes automatizados:

```bash
pytest
```

OBS: Quando for rodar os testes, no `.env` mude o campo `DB_HOST="localhost"` e `MODE="test"`

## 🔧 Como Usar Sem o Docker Compose

1. Inicie o servidor local:

```bash
dotenv run -- python src/main.py
```

- OBS: O banco do docker compose deve estar rodando e no `.env` mude o campo `DB_HOST="localhost"`.

2. Acesse a documentação interativa no navegador:

[http://localhost:8000/docs](http://localhost:8000/docs)

3. Crie seu usuário e faça a autenticação pelo `Authorize` no canto superior direito da tela. Insira o email e a senha. Os outros campos não precisa preencher. Depois, clique em `Authorize` no final do formulário. 

4. Para tornar um usuário `admin`, mude o campo `MODE` no `.env` para `test` e use a rota `v1/customers/to-admin` e insira o email do seu usuário. Com o modo teste ativado, você terá acesso de admin a todas as rotas. 

    4.1. Ou simplesmente mude a role do usuário para `admin` direto no banco de dados.

## 🛠️ Contribuindo

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Faça commit das alterações (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request
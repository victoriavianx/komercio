# 🪙 Komercio

Komercio é um projeto que simula a API para um site de compra e venda.

## 💻 Desenvolvimento

A API foi desenvolvida com Django Rest Framework, conectada com banco de dados PostgreSQL e tendo seu deploy feito no Heroku através do pacote gunicorn. O projeto Komercio foi um avanço na criação de views para as rotas com _Generic API Views_ e nas validações com _ModelSerializer_ e _Mixins_, além disso foi trabalhado o conceito de permissões e autenticação de usuários.

## 📓 Documentação da API

→ <a href="https://komercio-api.herokuapp.com/api/docs/">Link da Documentação</a>

## 📝 Features

- Cadastro de Usuário (Administrador, Vendedor ou Usuário comum)
- Listagem de Usuário pelo mais recente
- Atualização de Usuário
- Desativação de Usuário feito somente por Administrador
- Login
- Criação de Produto por usuário Vendedor
- Listagem de Produtos
- Atualização/Deleção feito somente pelo Vendedor do produto

## ⚙ Tecnologias

![Python](https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Heroku](https://img.shields.io/badge/Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white)

## 🧐 Como utilizar

### Requisitos

- Python a partir da versão 3.10.4
- Gerenciador de pacotes PIP
- Banco de dados PostgreSQL

### Instalação

1. Crie um banco de dados chamado komercio com PostgreSQL

2. Ao clonar o repositório, crie um ambiente virtual VENV na pasta do projeto com:

`python -m venv venv`

3. Rode o seguinte comando para ativar o ambiente virtual:
- _Linux_: `source venv/bin/activate`
- _Windows_: `.\venv\Scripts\activate`

4. Instale as dependências do projeto utilizando o PIP:

`pip install -r requirements.txt`

5. Crie um arquivo na raiz do projeto chamado `.env` e faça as configurações das variáveis de ambiente conforme o que está disposto no `.env.example` do projeto:

```
SECRET_KEY=
POSTGRES_PASSWORD=
POSTGRES_USER=
POSTGRES_DB=
```

6. Para rodar as migrações do banco de dados utilize o comando abaixo:

`python manage.py migrate`

7. Para o rodar o projeto localmente:

`python manage.py runserver`

## 🚧 Testes

Os testes foram escritos para verificar as Models e os relacionamentos entre elas.

Para rodar os testes, utilize o comando: `python manage.py test <nome_do_pacote>.tests`

<hr />

_Obrigada por chegar até aqui!_

Feito com ❤️ por [Victoria](https://github.com/victoriavianx)

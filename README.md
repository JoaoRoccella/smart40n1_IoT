# Persistência de Dados para a bancada Smart 4.0 N1 (IoT)
 
Este repositório contém o código para a persistência de dados coletados pela bancada Smart 4.0 N1, utilizando um banco de dados MySQL. O objetivo é armazenar e gerenciar os dados de sensores e dispositivos conectados à bancada, facilitando a análise e o monitoramento em tempo real.

## Estrutura do Projeto

- `models/database.py`: Contém a classe `Database` que gerencia a conexão com o banco de dados MySQL e fornece métodos para executar consultas SQL.
- `data/smart40n1.sql`: Script SQL para criar as tabelas necessárias no banco de dados.

## Requisitos

- Python 3.x
- MySQL Server
- Biblioteca `mysql-connector-python`
- Biblioteca `python-dotenv`

## Configuração do Ambiente

1. Clone este repositório:
```bash
git clone <url_do_repositorio>
cd smart40n1_IoT
```
2. Instale as dependências:
```bash
pip install -r requirements.txt
```
3. Configure as variáveis de ambiente criando um arquivo `.env` na raiz do projeto com as informações do arquivo modelo `.env.example`.

4. Crie o banco de dados e as tabelas executando o script SQL:
```bash
mysql -u seu_usuario -p seu_banco_de_dados < data/smart40n1.sql
```

## Uso

A bancada Smart 4.0 N1 enviará dados para um broker MQTT, que serão capturados pelo serviço mqtt_handler.py e armazenados no banco de dados MySQL utilizando a classe `Database` da camada de modelos.




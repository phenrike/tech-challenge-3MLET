
# Tech Challenge - API de Vitivinicultura

Este repositório contém o projeto desenvolvido como parte do **Tech Challenge**, uma atividade integradora que visa aplicar os conhecimentos adquiridos em diversas disciplinas. O objetivo é criar uma **API REST em Python** que consulta e disponibiliza os dados de vitivinicultura da **Embrapa**. Futuramente, essa API alimentará um modelo de **Machine Learning**, focado na análise e processamento de dados.

## Tecnologias Usadas 🛠️

- **Python 3.12** 🐍
- **Flask** 🌐
- **PostgreSQL** 🐘
- **Docker** 🐳 (**necessário para rodar o projeto**)
- **GitHub Actions** 🚀 
- **JWT** 🔑
- **Azure** ☁️

## Ambiente Necessário ⚙️

- **Python 3.12.7**: Instale a versão mais recente do Python [aqui](https://www.python.org/downloads/).
- **PostgreSQL**: Banco de dados para armazenar e consultar os dados. Instale-o [aqui](https://www.postgresql.org/download/).
- **Docker**: Necessário para rodar o projeto, criando e gerenciando containers da API e do banco de dados. Instale-o [aqui](https://www.docker.com/products/docker-desktop).
- **Git**: Para controle de versão e gerenciamento do repositório. Instale-o [aqui](https://git-scm.com/).

## Funcionalidades

- Consultas aos dados da Embrapa, incluindo:
  - Produção
  - Processamento
  - Comercialização
  - Importação
  - Exportação
- API documentada para facilitar o uso e integração.
- Suporte à autenticação JWT.
- Planejamento da arquitetura para ingestão de dados e deploy da API.
- MVP disponível com deploy em ambiente compartilhável.

## Objetivos do Projeto

1. **Criar uma API REST em Python** que consulte dados diretamente do site da Embrapa.
2. **Documentar a API** para facilitar sua integração por outros desenvolvedores.
3. **Implementar autenticação** (opcional, recomendada JWT) para proteger as rotas da API.
4. **Desenhar a arquitetura do projeto**, incluindo um plano de deploy e ingestão dos dados até a integração com um futuro modelo de Machine Learning.
5. **Deploy do MVP**, com um link compartilhável e um repositório no GitHub.
6. **Vídeo de 5 minutos**, apresentando o desenvolvimento do projeto e os resultados.

## Como Executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/phenrike/tech-challenge-3MLET.git
   ```

2. **Executar a API e o banco de dados (necessário Docker instalado)**:

   - Para a versão mais recente do Docker (recomendada):

     ```bash
     cd ./tech-challenge-3MLET/
     cd ./docker/
     docker compose up --build -d
     ```

   - Para a versão legada do Docker (se você ainda estiver usando `docker-compose`):

     ```bash
     cd ./tech-challenge-3MLET/
     cd ./docker/
     docker-compose up --build -d
     ```

3. **Acessar a API no navegador**:
<http://127.0.0.1:8080/apidocs/>

4. **Parar a execução da API e do banco de dados**:

   - Para a versão mais recente do Docker (recomendada):

     ```bash
     docker compose down
     ```

   - Para a versão legada do Docker:

     ```bash
     docker-compose down
     ```

5. **Parar a execução da API e do banco de dados e excluir os volumes**:

    - Para parar e excluir os volumes adicione o parâmetro "-v":

        ```bash
        docker compose down -v
        ```
_________________________________________________________________________________________

## Documentação da API

Esta API não consulta dados diretamente no site do Embrapa, ela possui um job que é executado diariamente e faz o download dos arquivos .csv disponibilizados pela empresa e os importa para um banco de dados local. Por tanto, caso tenha alguma atualização no site, ela estará disponibilizada no dia seguinte após a sincronização.

### **Endpoint: Registro de usuário**

Somente usuários cadastrados no banco de dados podem acessar a API.

**Requisição:**

- URL: `api/register`
- Método: POST
- Parâmetros:
  - `username`: Nome do usuário.
  - `password`: Senha do usuário.

**Resposta:**

- Código `201` - 	User successfully registered and saved in the database

### **Endpoint: Autenticação**

A autenticação na API é feita através de JWT (Jason Web Token).

**Requisição:**

- URL: `api/login`
- Método: POST
- Parâmetros:
  - `username`: Nome do usuário.
  - `password`: Senha do usuário.

**Resposta:**

- Código `200` - login successful and jwt generated
- Código `401`- Invalid username or password

### **Endpoint: Comercialização**

Este endpoint permite a pesquisa de dados comerciais baseados em ano ou produto.

**Requisição:**

- URL: `api/comercializacao`
- Método: GET
- Parâmetros:
  - `ano`: Ano de comercialização.
  - `produto`: Produto comercializado.

**Resposta:**

- Código `200` - Data returned successfully
- Código `400` - You must provide a year or a product
- Código `401`- Unauthorized

### **Endpoint: Produção**

Este endpoint permite a pesquisa de dados de produção baseados em ano ou produto.

**Requisição:**

- URL: `api/producao`
- Método: GET
- Parâmetros:
  - `ano`: Ano de produção.
  - `produto`: Produto produzido.

**Resposta:**

- Código `200` - Data returned successfully
- Código `400` - You must provide a year or a product
- Código `401`- Unauthorized

### **Endpoint: Processamento**

Este endpoint permite a pesquisa de dados do processamento baseados em ano, tipo da uva ou tipo de cultivo.

**Requisição:**

- URL: `api/processamento`
- Método: GET
- Parâmetros:
  - `ano`: Ano de processamento.
  - `tipo_uva`: Tipo de uva processada.
  - `tipo_cultivo`: Tipo de cultivo processado.

**Resposta:**

- Código `200` - Data returned successfully
- Código `400` - You must provide a year or a product
- Código `401`- Unauthorized

### **Endpoint: Tipos Processamento**

Este endpoint permite a pesquisa dos tipos de uvas processadas no endpoint de processamento.

**Requisição:**

- URL: `api/tipos_processamento`
- Método: GET

**Resposta:**

- Código `200` - Data returned successfully
- Código `401`- Unauthorized

### **Endpoint: Importação**

Este endpoint permite a pesquisa de dados importados baseados em ano, país e tipo de produto.

**Requisição:**

- URL: `api/importacao`
- Método: GET
- Parâmetros:
  - `ano`: Ano da importação.
  - `pais`: País de importação.
  - `tipo_prod`: Tipo de produto importado.

**Resposta:**

- Código `200` - Data returned successfully
- Código `400` - You must provide a year or a product
- Código `401`- Unauthorized

### **Endpoint: Exportação**

Este endpoint permite a pesquisa de dados exportados baseados em ano, país e tipo de produto.

**Requisição:**

- URL: `api/exportacao`
- Método: GET
- Parâmetros:
  - `ano`: Ano da exportação.
  - `pais`: País de exportação.
  - `tipo_prod`: Tipo de produto exportado.

**Resposta:**

- Código `200` - Data returned successfully
- Código `400` - You must provide a year or a product
- Código `401`- Unauthorized

### **Endpoint: Tipos Importação e Exportação**

Este endpoint permite a pesquisa dos tipos de uvas importadas/exportadas no endpoint de importação/exportação.

**Requisição:**

- URL: `api/tipos_importacao_exportacao`
- Método: GET

**Resposta:**

- Código `200` - Data returned successfully
- Código `401`- Unauthorized

_________________________________________________________
## Integrantes

1. Paulo Henrique Piaunios dos Santos  
2. Letícia Miranda  
3. Diogo Octaviano Jesse  
4. João Paulo Gonçalves Ribeiro  
5. Thadeu Pereira de Alencar Soares  

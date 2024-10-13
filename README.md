
# Tech Challenge - API de Vitivinicultura

Este repositório contém o projeto desenvolvido como parte do **Tech Challenge**, uma atividade integradora que visa aplicar os conhecimentos adquiridos em diversas disciplinas. O objetivo é criar uma **API REST em Python** que consulta e disponibiliza os dados de vitivinicultura da **Embrapa**. Futuramente, essa API alimentará um modelo de **Machine Learning**, focado na análise e processamento de dados.

## Tecnologias Usadas 🛠️

- **Python 3.12.7** 🐍
- **Flask** 🌐
- **PostgreSQL** 🐘
- **Docker** 🐳 (**necessário para rodar o projeto**)
- **GitHub Actions** 🚀 
- **JWT** 🔑

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
   ```bash
   cd ./docker/
   docker-compose up --build -d
   ```

3. **Acessar a API no navegador**:
<http://127.0.0.1:5000/apidocs/>

4. Parar a execução da API e do banco de dados:
   ```bash
   docker-compose down
   ```

## Integrantes

1. Paulo Henrique Piaunios dos Santos  
2. Letícia Miranda  
3. Diogo Octaviano Jesse  
4. João Paulo Gonçalves Ribeiro  
5. Thadeu Pereira de Alencar Soares  

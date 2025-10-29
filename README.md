# webscraper

Implementado de acordo com a especificação entregue para o Desafio Técnioc - Melhorias Estruturais

## Requisitos
- Necessário uma instalação do Docker e Docker Compose na máquina

## Setup

- Antes de tudo, crie um arquivo `.env` na raiz do repositório com os dados necessários
- Como esse repositório é para testes, pode-se copiar diratamente do arquivo `.env.exemplo`

```bash
cp .env.exemplo .env
```
- Faça o build da imagem Python utilizada nos serviços 'worker' e 'scraper-api', execute

```bash
docker compose build
```

### RabbitMQ e Redis
- Inicie-os em um terminal isolado com o comando

```bash
docker compose up rabbitmq redis
```
- __OBS__: Esses dois serviços utilizam volumes docker. Caso seja necessário limpar seu armazenamento, pare os serviços e execute

```bash
docker volume rm redis_data rabbitmq_data
```

### Api webscraper
- Para iniciar a API

```bash
docker compose up scraper-api
```

### Workers
- Para inicar um número N de workers, execute o seguinte comando (em meus testes fiz com N=3 workers)
```bash
docker compose up --no-deps --scale worker=N worker
```

## Ferramentas

- Documentação da API se encontra na URL `http://localhost:8000/docs`, foram definidos os mesmos endpoints da especificação
- Managment do RabbitMQ na URL `http://localhost:15672/`, com usuário e senha sendo o mesmo do arquivo `.env`

## Observações
- No endpoint GET /results/{taskId}, não foi especificado explicitamente o que poderia ser usado de {taskId}, então foi utilizado o CNPJ pois é uma chave única que pode ser utilizada para buscar o cache no Redis sem conflitos
- Foi utilizado o flake8 para garantir que o código siga o padrão PEP8. Ao construir a imagem, o flake8 é rodado para verificar se há algum arquivo fora do padrão. Utilizo também o executável `black`que formata os arquivos automaticamente para o PEP8, utilizei ele regularmente enquato estava desevolvendo, o que deixou todos os arquivos padronizados
- Fiz uma aplicação maior e mais estruturada afim de mostrar meus conhecimentos em construir aplicações Python. Ao mesmo tempo não tive todo o tempo que gostaria para implementar os testes unitários da aplicação, mesmo estando familiarizado em fazê-los

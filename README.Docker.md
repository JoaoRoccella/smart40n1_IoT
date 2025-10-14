### Construindo e executando sua aplicação

Para iniciar sua aplicação, execute:
`docker compose up --build`

A aplicação estará disponível em http://localhost:8000.

### Deploy da aplicação na nuvem

Primeiro, construa sua imagem:
`docker build -t meuapp .`

Se a arquitetura do seu ambiente de nuvem for diferente da sua máquina local (por exemplo, você usa Mac M1 e a nuvem é amd64), construa a imagem para a plataforma correta:
`docker build --platform=linux/amd64 -t meuapp .`

Depois, envie a imagem para o seu registro:
`docker push meu-registro.com/meuapp`

Consulte a documentação do Docker para mais detalhes sobre build e push:
https://docs.docker.com/go/get-started-sharing/

### Referências
* [Guia Python no Docker](https://docs.docker.com/language/python/)
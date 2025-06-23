```markdown
# Manual de Deploy no Coolify

## 1. Introdução ao Coolify

### O que é o Coolify?

Coolify é uma plataforma de auto-hospedagem (self-hosted PaaS) de código aberto que simplifica a implantação e o gerenciamento de suas aplicações, bancos de dados e serviços em seus próprios servidores. Ele oferece uma alternativa a serviços de nuvem como Heroku, Vercel ou Railway, permitindo maior controle sobre sua infraestrutura e dados.

### Principais Funcionalidades

*   **Qualquer Linguagem/Framework:** Suporte para diversas tecnologias via Buildpacks (Nixpacks, Dockerfile, etc.).
*   **Qualquer Servidor:** Implante em VPS, servidores dedicados, Raspberry Pi, ou qualquer máquina Linux com acesso SSH.
*   **Deploy via Git:** Integração com GitHub, GitLab, Bitbucket e Gitea.
*   **Bancos de Dados Gerenciados:** Crie e gerencie bancos de dados populares com facilidade.
*   **Serviços One-Click:** Implante serviços como WordPress, Ghost, Plausible Analytics com poucos cliques.
*   **SSL Automático:** Certificados SSL gratuitos via Let's Encrypt.
*   **Backups Automáticos:** Configure backups para bancos de dados e para a própria instância Coolify.
*   **Variáveis de Ambiente Seguras:** Gerenciamento fácil de configurações e segredos.
*   **Monitoramento Básico:** Acompanhe o status dos seus recursos.
*   **Proxy Reverso Integrado:** Traefik configurado automaticamente para roteamento e SSL.
*   **Escalabilidade Horizontal:** Suporte a múltiplos servidores.

### Coolify Cloud vs. Auto-hospedado

*   **Coolify Cloud:**
    *   Serviço pago gerenciado pela equipe Coolify.
    *   Não requer instalação ou manutenção da plataforma Coolify em si.
    *   Ideal para quem quer focar apenas na implantação das aplicações.
*   **Auto-hospedado:**
    *   Gratuito (você paga apenas pelos seus servidores).
    *   Controle total sobre a instalação e configuração do Coolify.
    *   Requer que você instale e mantenha a plataforma Coolify.

Este manual foca na versão **Auto-hospedada** do Coolify.

## 2. Pré-requisitos de Instalação (Auto-hospedado)

Antes de instalar o Coolify em seu servidor, garanta que os seguintes requisitos são atendidos:

### Requisitos do Servidor

*   **Acesso SSH:** Acesso root ou um usuário com permissões sudo e autenticação por chave SSH.
*   **Sistema Operacional (64-bit):**
    *   Debian-based (Debian, Ubuntu)
    *   Redhat-based (CentOS, Fedora, AlmaLinux, Rocky Linux)
    *   SUSE-based (SLES, openSUSE)
    *   Arch Linux
    *   Alpine Linux
    *   Raspberry Pi OS (64-bit)
*   **Arquitetura:** AMD64 ou ARM64.
*   **Hardware Mínimo:**
    *   CPU: 2 cores
    *   RAM: 2 GB
    *   Disco: 30 GB de espaço livre
    *   *Recomendação:* Para múltiplas aplicações ou aplicações mais pesadas, utilize especificações superiores.
*   **Observação:** É recomendado usar um servidor "limpo" para evitar conflitos com aplicações existentes.

### Dependências

*   **Docker Engine:** Versão 24 ou superior. O script de instalação rápida geralmente cuida disso, mas para alguns SOs (como AlmaLinux), pode ser necessário instalar o Docker manualmente antes.
    *   *Atenção:* Docker instalado via Snap **não** é suportado.
*   **curl:** Geralmente pré-instalado na maioria das distribuições Linux.

## 3. Instalando o Coolify (Auto-hospedado)

Existem duas formas principais de instalar o Coolify:

### Método Rápido (Script de Instalação - Recomendado)

Este é o método mais simples. Conecte-se ao seu servidor via SSH como root (ou um usuário com `sudo`) e execute o comando:

```bash
curl -fsSL https://cdn.coollabs.io/coolify/install.sh | sudo bash
```

O script irá:
*   Instalar ferramentas essenciais (curl, wget, git, jq, openssl).
*   Instalar o Docker Engine (se não presente ou versão incompatível).
*   Configurar o Docker.
*   Criar os diretórios necessários em `/data/coolify`.
*   Configurar chaves SSH para gerenciamento do servidor.
*   Instalar e iniciar o Coolify.

Após a conclusão, o script exibirá a URL para acessar sua instância Coolify (ex: `http://SEU_IP_DO_SERVIDOR:8000`).

### Método Manual (Passo a Passo)

Para usuários avançados que desejam maior controle:

1.  **Prepare o Servidor:**
    *   Garanta que o Docker Engine (v24+) e `curl` estão instalados.
    *   Configure o acesso SSH com chave pública para o usuário root no `~/.ssh/authorized_keys`.

2.  **Crie os Diretórios:**
    ```bash
    sudo mkdir -p /data/coolify/{source,ssh,applications,databases,backups,services,proxy,webhooks-during-maintenance}
    sudo mkdir -p /data/coolify/ssh/{keys,mux}
    sudo mkdir -p /data/coolify/proxy/dynamic
    ```

3.  **Gere e Adicione a Chave SSH para o Coolify:**
    ```bash
    sudo ssh-keygen -f /data/coolify/ssh/keys/id.root@coolify -t ed25519 -N '' -C root@coolify
    sudo cat /data/coolify/ssh/keys/id.root@coolify.pub | sudo tee -a /root/.ssh/authorized_keys
    sudo chmod 600 /root/.ssh/authorized_keys
    ```

4.  **Baixe os Arquivos de Configuração:**
    ```bash
    sudo curl -fsSL https://cdn.coollabs.io/coolify/docker-compose.yml -o /data/coolify/source/docker-compose.yml
    sudo curl -fsSL https://cdn.coollabs.io/coolify/docker-compose.prod.yml -o /data/coolify/source/docker-compose.prod.yml
    sudo curl -fsSL https://cdn.coollabs.io/coolify/.env.production -o /data/coolify/source/.env
    sudo curl -fsSL https://cdn.coollabs.io/coolify/upgrade.sh -o /data/coolify/source/upgrade.sh
    ```

5.  **Defina Permissões:**
    ```bash
    sudo chown -R 9999:root /data/coolify # O ID 9999 pode variar dependendo do usuário 'coolify' dentro do container
    sudo chmod -R 700 /data/coolify
    ```
    *Nota: Verifique o ID de usuário correto para o Coolify se encontrar problemas de permissão.*

6.  **Gere Valores para o .env:**
    (Execute estes comandos **apenas uma vez** na instalação inicial)
    ```bash
    sudo sed -i "s|APP_ID=.*|APP_ID=$(openssl rand -hex 16)|g" /data/coolify/source/.env
    sudo sed -i "s|APP_KEY=.*|APP_KEY=base64:$(openssl rand -base64 32)|g" /data/coolify/source/.env
    sudo sed -i "s|DB_PASSWORD=.*|DB_PASSWORD=$(openssl rand -base64 32)|g" /data/coolify/source/.env
    sudo sed -i "s|REDIS_PASSWORD=.*|REDIS_PASSWORD=$(openssl rand -base64 32)|g" /data/coolify/source/.env
    sudo sed -i "s|PUSHER_APP_ID=.*|PUSHER_APP_ID=$(openssl rand -hex 32)|g" /data/coolify/source/.env
    sudo sed -i "s|PUSHER_APP_KEY=.*|PUSHER_APP_KEY=$(openssl rand -hex 32)|g" /data/coolify/source/.env
    sudo sed -i "s|PUSHER_APP_SECRET=.*|PUSHER_APP_SECRET=$(openssl rand -hex 32)|g" /data/coolify/source/.env
    ```

7.  **Crie a Rede Docker:**
    ```bash
    sudo docker network create --attachable coolify
    ```

8.  **Inicie o Coolify:**
    ```bash
    cd /data/coolify/source
    sudo docker compose --env-file .env -f docker-compose.yml -f docker-compose.prod.yml up -d --pull always --remove-orphans --force-recreate
    ```

### Primeiros Passos Após a Instalação

1.  **Acesse a UI:** Abra o endereço fornecido pelo script de instalação (ou `http://SEU_IP_DO_SERVIDOR:8000`) no seu navegador.
2.  **Crie a Conta Admin:** A primeira tela será para registrar o usuário administrador. **Faça isso imediatamente** para proteger sua instância.

## 4. Conceitos Fundamentais do Coolify

*   **Servidores:** Máquinas (localhost ou remotas) onde seus recursos serão implantados. Coolify precisa de acesso SSH a elas.
*   **Projetos:** Agrupadores lógicos para seus recursos. Um projeto pode conter várias aplicações e bancos de dados.
*   **Ambientes:** Subdivisões dentro de um projeto (ex: `production`, `staging`, `development`). Cada ambiente pode ter configurações e variáveis diferentes.
*   **Recursos:**
    *   **Aplicações:** Seu código, seja um backend, frontend ou site estático.
    *   **Bancos de Dados:** Instâncias de bancos de dados como PostgreSQL, MySQL, etc.
    *   **Serviços:** Aplicações pré-configuradas (one-click services) como WordPress, Ghost, etc.
*   **Build Packs:** Mecanismos que o Coolify usa para construir e empacotar sua aplicação em uma imagem Docker.
    *   **Nixpacks:** Tenta detectar automaticamente a linguagem e framework do seu projeto e constrói a imagem. Ideal para muitos casos comuns (Node.js, Python, Ruby, PHP, Go, Rust, etc.).
    *   **Static:** Para sites estáticos simples (HTML, CSS, JS).
    *   **Dockerfile:** Permite que você forneça seu próprio `Dockerfile` para controle total sobre o processo de build.
    *   **Docker Compose:** Para implantar aplicações que já possuem um `docker-compose.yml`, ideal para setups multi-container.
*   **Proxy (Traefik):** Coolify utiliza o Traefik como proxy reverso padrão. Ele gerencia o roteamento de tráfego para suas aplicações, lida com SSL e permite configurações avançadas.

## 5. Configurando Servidores no Coolify

### Adicionando um Novo Servidor

1.  No dashboard do Coolify, vá para "Servers".
2.  Clique em "Add a new Server".
3.  **Nome:** Um nome descritivo para o servidor.
4.  **IP Address or Domain:** O endereço IP ou domínio do servidor.
5.  **User:** O usuário para conexão SSH (geralmente `root` ou um usuário com `sudo`).
6.  **Port:** A porta SSH (padrão 22).
7.  **Private Key:** Selecione uma chave SSH previamente adicionada ao Coolify ou adicione uma nova. Esta chave pública correspondente deve estar no arquivo `~/.ssh/authorized_keys` do usuário no servidor de destino.
    *   Coolify pode gerar um par de chaves para você, exibindo a chave pública a ser adicionada ao servidor.
8.  Clique em "Connect". Coolify tentará validar a conexão.

### Configurações do Servidor

Após adicionar um servidor, você pode configurá-lo:

*   **Wildcard Domain:** Defina um domínio curinga (ex: `*.meuservidor.com`). Se configurado, Coolify gerará automaticamente subdomínios para suas aplicações (ex: `app1.meuservidor.com`). Se não, usará `sslip.io`.
*   **Proxy Type:**
    *   **Traefik (padrão):** Recomendado. Coolify gerenciará o Traefik.
    *   **None/Custom:** Se você deseja gerenciar seu próprio proxy manualmente.
*   **Disk Cleanup threshold:** Porcentagem de uso do disco que, ao ser atingida, dispara uma limpeza automática (remove imagens Docker não utilizadas, etc.).

### Gerenciamento de Múltiplos Servidores

*   Coolify pode gerenciar múltiplos servidores a partir de uma única instância.
*   Cada servidor executa seu próprio proxy (Traefik).
*   O tráfego para uma aplicação em um servidor secundário vai diretamente para esse servidor, não passando pelo servidor principal do Coolify.
*   **Importante:** O DNS do seu domínio/subdomínio deve apontar para o IP do servidor onde a aplicação específica está implantada.

## 6. Implantando Aplicações

### Conectando Repositórios Git

1.  Vá para "Sources" no Coolify e adicione sua conta GitHub, GitLab ou outro provedor Git.
    *   **GitHub App (Recomendado):** Instale o App do Coolify no seu GitHub para fácil acesso aos repositórios.
    *   **Deploy Key:** Para repositórios privados sem usar o App, você pode adicionar uma chave de deploy.
2.  Crie um novo "Project" e dentro dele, um "Environment" (ex: `production`).
3.  No ambiente, clique em "Add Resource" e escolha "Application".
4.  **Source:** Selecione o provedor Git e o repositório.
5.  **Branch:** Escolha a branch para deploy.

### Usando Build Packs

Ao configurar a aplicação, você escolherá um Build Pack:

*   **Nixpacks (Build Automático):**
    *   Coolify (via Nixpacks) tentará detectar a linguagem/framework.
    *   **Install Command:** (Opcional) Comando para instalar dependências (ex: `npm install`, `pip install -r requirements.txt`).
    *   **Build Command:** (Opcional) Comando para construir a aplicação (ex: `npm run build`).
    *   **Start Command:** Comando para iniciar a aplicação (ex: `npm start`, `python app.py`).
    *   **Root Directory:** (Opcional) Se seu código não está na raiz do repositório.

*   **Static Sites:**
    *   Similar ao Nixpacks, mas otimizado para sites estáticos.
    *   Configure o **Publish Directory** (geralmente `build`, `dist`, `public`, `_site`).

*   **Dockerfile (Build Personalizado):**
    *   **Dockerfile Location:** Caminho para seu `Dockerfile` no repositório (padrão: `./Dockerfile`).
    *   **Docker Build Context:** Caminho para o contexto de build (padrão: `.`).
    *   Coolify executará `docker build` usando seu Dockerfile.

*   **Docker Compose (Aplicações Multi-container):**
    *   **Docker Compose Location:** Caminho para seu `docker-compose.yml` (ou similar) no repositório.
    *   **Docker Compose File (Content):** Você pode colar o conteúdo do seu compose diretamente se não estiver no repositório.
    *   Coolify usará `docker compose up -d` com o arquivo fornecido.
    *   *Nota:* Variáveis de ambiente definidas no Coolify podem ser referenciadas no seu `docker-compose.yml` (ex: `${MY_VARIABLE}`).

### Configurando Variáveis de Ambiente

Na aba "Environment Variables" da sua aplicação:

*   **Adicionar Variável:** Chave (ex: `DATABASE_URL`) e Valor.
*   **Build Variable:** Marque esta caixa se a variável for necessária durante o processo de build (será injetada no ambiente de build).
*   **Is Secret?** Marque para que o valor não seja exibido na UI após salvo e para evitar que seja logado.
*   **Shared Variables:**
    *   **Team:** `{{team.NOME_VARIAVEL}}`
    *   **Project:** `{{project.NOME_VARIAVEL}}`
    *   **Environment:** `{{environment.NOME_VARIAVEL}}`
    *   Estas variáveis são definidas nos níveis correspondentes (Team, Project settings, Environment settings).
*   **Predefined Variables:** Coolify injeta automaticamente variáveis como:
    *   `COOLIFY_FQDN`: Domínio(s) completo(s) da aplicação.
    *   `COOLIFY_URL`: URL(s) da aplicação.
    *   `COOLIFY_BRANCH`: Branch do deploy.
    *   `SOURCE_COMMIT`: Hash do commit.
    *   `PORT`: Primeira porta exposta (se não definida manualmente).
    *   `HOST`: `0.0.0.0` (se não definida manualmente).

### Definindo Domínios e URLs

Na aba "Configuration" da sua aplicação:

*   **FQDN (Fully Qualified Domain Name):** Insira o(s) domínio(s) pelos quais sua aplicação será acessível (ex: `https://minhaapp.com, https://www.minhaapp.com`).
    *   Coolify automaticamente solicitará certificados SSL para estes domínios.
    *   Certifique-se de que os registros DNS para estes domínios apontam para o IP do servidor onde a aplicação está implantada.
*   Você pode especificar uma porta se o proxy precisar mapear para uma porta específica no container: `https://minhaapp.com:80` (embora o Traefik geralmente detecte isso da configuração de portas).

### Configurando Portas e Exposição

Na aba "Configuration":

*   **Ports (Exposes):** A(s) porta(s) que seu container expõe (ex: `3000`, `8080`). O Traefik usará a primeira porta listada para rotear o tráfego do FQDN, a menos que especificado de outra forma.
*   **Ports (Mappings):** (Menos comum para aplicações web padrão, mais para bancos de dados ou serviços específicos) Mapeia portas do host para o container.

### Armazenamento Persistente (Volumes)

Na aba "Storages":

*   **Path in Container:** O caminho dentro do container que precisa ser persistido (ex: `/app/data`, `/var/lib/mysql`).
*   **Path on Host (Optional):** O caminho no servidor host onde os dados serão armazenados. Se deixado em branco, Coolify gerencia um volume Docker nomeado.
*   Essencial para bancos de dados ou qualquer aplicação que precise manter dados entre reinicializações/deploys.

### Health Checks

Na aba "Health Checks":

*   Configure verificações de saúde para que o Coolify (e o Docker) saibam se sua aplicação está rodando corretamente.
*   **Path:** Endpoint HTTP para verificar (ex: `/health`, `/status`).
*   **Port:** Porta para a verificação.
*   **Interval, Retries, Timeout:** Configurações para a frequência e tolerância da verificação.

### Deployments (Rollbacks, Logs de Deploy)

*   Após configurar, clique em "Deploy".
*   A aba "Deployments" mostrará o progresso e os logs do build e deploy.
*   Se um deploy falhar ou você precisar reverter, você pode selecionar um deploy anterior bem-sucedido e clicar em "Redeploy".

## 7. Gerenciando Bancos de Dados

### Criando Novos Bancos de Dados

1.  No seu "Project" > "Environment", clique em "Add Resource".
2.  Escolha o tipo de banco de dados (PostgreSQL, MySQL, MariaDB, MongoDB, Redis, etc.).
3.  Configure o nome, usuário, senha e versão (se aplicável).
4.  **Public Port (Optional):** Defina uma porta se desejar acessar o banco de dados externamente (fora da rede Docker do servidor). **Cuidado com a segurança!**
5.  Clique em "Create".

### Conectando Aplicações a Bancos de Dados

Após criar um banco de dados, o Coolify fornecerá as variáveis de ambiente de conexão (Host, Porta, Usuário, Senha, Nome do Banco).

*   **Host:** Geralmente o nome do serviço Docker do banco de dados (ex: `meu-postgres-123`). Coolify facilita isso mostrando o nome do serviço.
*   **Porta:** A porta interna do banco de dados na rede Docker (ex: `5432` para PostgreSQL).

Adicione estas informações como variáveis de ambiente na sua aplicação.

### Configurando SSL para Bancos de Dados

Alguns bancos de dados suportados pelo Coolify (como PostgreSQL) podem ter SSL configurado para conexões. Verifique a documentação específica do banco de dados no Coolify para detalhes.

### Backups Agendados e Restauração

Na configuração do seu banco de dados, vá para a aba "Backups":

*   **Scheduled Backup:** Ative e defina uma expressão cron para a frequência do backup (ex: `0 2 * * *` para diariamente às 2 da manhã).
    *   Coolify também suporta strings simples como `daily`, `weekly`, `monthly`.
*   **Storage:** Escolha onde os backups serão armazenados:
    *   **Local:** No servidor onde o banco de dados está rodando.
    *   **S3 Compatible:** Configure um destino S3 (AWS S3, MinIO, Cloudflare R2, etc.) nas configurações do Coolify ("Destinations" > "S3 Storages") e selecione-o aqui.
*   **Restauração:** Backups concluídos aparecerão na lista. Você pode selecionar um backup e clicar em "Restore" (siga as instruções, pode envolver downtime).

## 8. Utilizando Serviços One-Click

Coolify oferece um catálogo de serviços populares que podem ser implantados com configuração mínima:

1.  No seu "Project" > "Environment", clique em "Add Resource".
2.  Selecione "Service".
3.  Escolha o serviço desejado na lista (ex: WordPress, Ghost, Plausible Analytics, Uptime Kuma).
4.  Siga as instruções específicas para o serviço (geralmente envolve definir um domínio e, opcionalmente, conectar a um banco de dados existente ou criar um novo).
5.  Configure variáveis de ambiente, se necessário.
6.  Clique em "Deploy".

## 9. Rede e Domínios

### Configuração de DNS para Aplicações

*   Para cada FQDN que você configurar para suas aplicações ou serviços, você precisa criar um registro DNS (geralmente um `A` record ou `CNAME`) no seu provedor de DNS.
*   O registro `A` deve apontar para o endereço IP público do servidor onde a aplicação está hospedada.
*   Se estiver usando um subdomínio e o domínio principal já aponta para um IP, um `CNAME` pode ser usado para apontar para o domínio principal ou outro FQDN gerenciado pelo Coolify.

### Gerenciamento de Domínios e Subdomínios

*   Adicione FQDNs na configuração da sua aplicação/serviço.
*   Para wildcard SSL, configure um "Wildcard Domain" nas configurações do servidor.

### SSL Automático com Let's Encrypt

*   Se o Traefik estiver habilitado (padrão), Coolify automaticamente tentará obter e renovar certificados SSL da Let's Encrypt para os FQDNs configurados.
*   Isso requer que o DNS esteja configurado corretamente e propagado, e que as portas 80 e 443 do servidor estejam acessíveis publicamente para o desafio de validação da Let's Encrypt.

### Usando Certificados SSL Personalizados

Se você tiver seus próprios certificados SSL:

1.  Vá para as configurações do Servidor > Proxy.
2.  Na seção de configuração dinâmica do Traefik, você pode adicionar a configuração para usar seus certificados. Consulte a [documentação do Traefik sobre TLS](https://doc.traefik.io/traefik/routing/routers/#tls) e [provedores de certificado](https://doc.traefik.io/traefik/https/tls/#providers) para a sintaxe correta.
    *   Isso geralmente envolve montar os arquivos do certificado (chain e private key) no container do Traefik e referenciá-los na configuração dinâmica.

### Configurações de Proxy (Traefik)

O Traefik é poderoso e altamente configurável. Coolify gerencia a configuração básica. Para customizações:

*   **Local:** Configurações do Servidor > Proxy > Dynamic Proxy Configuration (YAML).
*   **Autenticação Básica:**
    ```yaml
    http:
      middlewares:
        my-basic-auth:
          basicAuth:
            users:
              - "user:hashedpassword" # Gerar com htpasswd
      routers:
        my-app-router:
          rule: "Host(`minhaapp.com`)"
          service: "minhaapp-service-id" # Encontre o ID do serviço na UI do Coolify
          entryPoints:
            - "websecure"
          middlewares:
            - "my-basic-auth"
          tls:
            certResolver: "letsencrypt"
    ```
    *Adapte `my-app-router`, `Host`, `service` e o nome do middleware.*

*   **Redirecionamentos:**
    ```yaml
    http:
      middlewares:
        redirect-to-www:
          redirectRegex:
            regex: "^https://example.com/(.*)"
            replacement: "https://www.example.com/${1}"
            permanent: true
      routers:
        router-non-www:
          rule: "Host(`example.com`)"
          service: "noop@internal" # Serviço dummy para aplicar middleware
          entryPoints:
            - "websecure"
          middlewares:
            - "redirect-to-www"
          tls:
            certResolver: "letsencrypt"
    ```

*   **Load Balancing:** O Traefik faz load balancing automaticamente se sua aplicação Docker Compose define múltiplas réplicas de um serviço. Para aplicações não-compose, você precisaria configurar instâncias separadas e usar a configuração dinâmica do Traefik para definir um serviço com múltiplos servidores.

Consulte a [documentação oficial do Traefik](https://doc.traefik.io/traefik/) para opções avançadas.

## 10. Monitoramento e Manutenção

### Monitoramento de Recursos do Servidor

*   **Coolify UI:** O dashboard do servidor no Coolify mostra uso de CPU, memória e disco.
*   **Sentinel (Opcional):** Para monitoramento mais detalhado, você pode instalar o Coolify Sentinel no servidor (disponível nas configurações do servidor no Coolify).

### Logs da Aplicação e do Sistema

*   **Logs de Deploy:** Visíveis na aba "Deployments" da sua aplicação/serviço.
*   **Logs de Runtime:**
    *   Clique no ícone de logs ao lado do status da sua aplicação/serviço para ver os logs do container em tempo real.
    *   **Drain Logs:** Na configuração da aplicação, você pode configurar um "Log Drain" para enviar logs para um serviço de agregação externo (ex: Papertrail, Logtail).

### Configurando Notificações

Vá para "Settings" (Configurações da instância Coolify) > "Notifications":

*   Configure canais de notificação (Email, Discord, Telegram, etc.).
*   Coolify enviará alertas sobre:
    *   Deploys bem-sucedidos ou falhos.
    *   Status de containers (paradas inesperadas).
    *   Status de backups.
    *   Alto uso de disco.

### Atualizando o Coolify

1.  Vá para "Settings" na sua instância Coolify.
2.  Se uma atualização estiver disponível, um botão "Update Available" aparecerá.
3.  Clique para iniciar o processo de atualização. É recomendado fazer um backup da instância Coolify antes de grandes atualizações.

### Backup e Restauração da Instância Coolify

A própria instância Coolify (suas configurações, metadados de aplicações, etc.) é armazenada em um banco de dados PostgreSQL.

*   **Backup:**
    1.  Vá para "Settings" > "Instance Backup".
    2.  Configure a frequência e o destino do backup (Local ou S3).
    *   *Isso faz backup da configuração do Coolify, não dos dados das suas aplicações implantadas (para isso, configure backups por recurso).*
*   **Restauração:**
    1.  Em caso de falha, instale uma nova instância Coolify na mesma versão (ou mais nova) da qual o backup foi feito.
    2.  Copie o arquivo de backup do PostgreSQL para o novo servidor.
    3.  Pare a nova instância Coolify: `cd /data/coolify/source && sudo docker compose down`
    4.  Restaure o dump do PostgreSQL usando `pg_restore`. O nome do banco de dados padrão é `coolify`.
        Exemplo (adapte usuário, host, nome do dump):
        ```bash
        sudo docker exec -i $(sudo docker ps -f name=coolify-db -q) pg_restore -U coolify -d coolify --clean < /caminho/para/seu/backup.dmp
        ```
    5.  Inicie o Coolify: `sudo docker compose up -d`

## 11. Recursos Avançados

### Uso da API Coolify para Automação

Coolify possui uma API RESTful que pode ser usada para automatizar tarefas.

1.  Em "Settings" > "API Tokens", gere um token de API.
2.  Consulte a seção "API Reference" na documentação oficial do Coolify (`https://coolify.io/docs/api-reference/`) para endpoints e exemplos.
    *   Você pode listar, criar, deletar aplicações, bancos de dados, disparar deploys, etc.

### Webhooks

*   **Incoming Webhooks:** Para cada aplicação, você pode configurar um webhook de deploy. Chamar este webhook (com um `POST` request) acionará um novo deploy da branch configurada.
*   **Outgoing Webhooks/Notifications:** Configure nas "Settings" para notificar sistemas externos sobre eventos de deploy.

### Gerenciamento de Times e Permissões

Se você trabalha em equipe:

1.  Vá para "Teams" (no menu principal ou em "Settings").
2.  Convide membros para sua equipe.
3.  Atribua permissões (ex: Admin, Member, Viewer) para controlar o acesso a projetos e recursos.

## 12. Solução de Problemas Comuns

*   **Problemas de Instalação:**
    *   Verifique os logs do script de instalação.
    *   Certifique-se de que o Docker está rodando e os requisitos foram atendidos.
    *   Problemas de permissão em `/data/coolify`.
*   **Erros de Deploy:**
    *   **Bad Gateway (502):**
        *   Aplicação não iniciou corretamente (verifique logs da aplicação).
        *   Porta errada configurada em "Ports (Exposes)".
        *   Health check falhando.
        *   Problemas de rede no servidor ou configuração de proxy.
    *   **Falha no Build:** Verifique os logs de build para erros de compilação, dependências faltando, etc.
*   **Problemas de Conexão com Servidor:**
    *   Chave SSH incorreta ou não adicionada ao `authorized_keys`.
    *   Firewall bloqueando a porta SSH.
    *   Servidor offline.
*   **Falhas de SSL/Certificado:**
    *   DNS não propagado corretamente (use `dig NOME_DO_DOMINIO` para verificar).
    *   Portas 80/443 bloqueadas por firewall, impedindo a validação da Let's Encrypt.
    *   Limites de taxa da Let's Encrypt (comum em testes excessivos).
    *   Wildcard SSL não funcionando: verifique a configuração do provedor DNS para o desafio `DNS-01` se estiver usando wildcard com Traefik e Let's Encrypt (requer configuração adicional no Traefik e no provedor DNS).

Consulte a seção "Troubleshoot" da [documentação oficial do Coolify](https://coolify.io/docs/troubleshoot/overview) para mais detalhes.

## 13. Apêndice

### Comandos Úteis (no servidor Coolify)

*   **Verificar status dos containers Coolify:**
    ```bash
    cd /data/coolify/source
    sudo docker compose ps
    ```
*   **Ver logs de um container Coolify (ex: coolify-db):**
    ```bash
    sudo docker logs coolify-db # Substitua pelo nome do container
    ```
*   **Parar Coolify:**
    ```bash
    cd /data/coolify/source
    sudo docker compose down
    ```
*   **Iniciar Coolify:**
    ```bash
    cd /data/coolify/source
    sudo docker compose up -d
    ```
*   **Forçar recriação dos containers Coolify (útil após algumas alterações manuais ou problemas):**
    ```bash
    cd /data/coolify/source
    sudo docker compose up -d --force-recreate
    ```

### Referências da Documentação Oficial

*   **Documentação Principal:** [https://coolify.io/docs/](https://coolify.io/docs/)
*   **GitHub:** [https://github.com/coollabsio/coolify](https://github.com/coollabsio/coolify)
*   **Discord (Comunidade e Suporte):** Link disponível no site do Coolify.

---

Este manual fornece uma visão geral abrangente. Para detalhes específicos e atualizações, sempre consulte a documentação oficial do Coolify.
```

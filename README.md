# Epic Games Free Game Monitor RPA

Este projeto é um RPA (Robotic Process Automation) desenvolvido em Python que monitora diariamente a Epic Games Store para identificar os jogos gratuitos da semana, envia uma notificação por e-mail com detalhes e screenshot, e agenda automaticamente a próxima verificação com base na data de expiração da oferta.

## 🚀 Funcionalidades

- **Monitoramento Automático:** Acessa a página de jogos grátis da Epic Games.
- **Detecção Inteligente:** Identifica o jogo, data de validade e tira um screenshot do card da oferta.
- **Notificação Rica:** Envia e-mail com o nome do jogo, prazo e a imagem do jogo incorporada.
- **Agendamento Dinâmico:** Se auto-configura no GitHub Actions para rodar 10 minutos após o fim da promoção atual, garantindo que você seja um dos primeiros a saber do próximo jogo.
- **Agendamento Fixo:** Executa diariamente às 09:00 (Brasília) como garantia.

## 🛠️ Arquitetura

O projeto foi refatorado seguindo princípios de **Clean Code** e padrões de projeto voltados para RPA:

- **`src/config.py`**: Centraliza todas as configurações e variáveis de ambiente.
- **`src/pages/`**: Implementa o padrão **Page Object Model (POM)**, encapsulando a lógica de interação com a página (Playwright).
- **`src/services/`**: Serviços responsáveis pela composição e envio de e-mails (MIME Multipart) e gerenciamento de workflow.
- **`main.py`**: Orquestrador que conecta todos os módulos.

## 📋 Pré-requisitos

- Python 3.10+
- Conta no Gmail (para envio de e-mail)
- Repositório no GitHub (para execução automática via Actions)

## 🔧 Instalação Local

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/seu-repo.git
   cd seu-repo
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

3. Configure as variáveis de ambiente:
   - Crie um arquivo `.env` na raiz do projeto (copie de `.env.example`).
   - Preencha com suas credenciais:
     ```env
     EMAIL_ADDRESS=seu_email@gmail.com
     EMAIL_PASSWORD=sua_senha_de_aplicativo
     EMAIL_RECIPIENT=email_destino@dominio.com
     ```
   > **Nota:** Nunca comite o arquivo `.env` com suas senhas reais!

4. Execute:
   ```bash
   python main.py
   ```

## ⚙️ Configuração no GitHub Actions

O workflow já está configurado em `.github/workflows/epic_games_check.yml`.

1. Vá em **Settings > Secrets and variables > Actions** no seu repositório.
2. Adicione os segredos:
   - `EMAIL_ADDRESS`: Seu e-mail (remetente).
   - `EMAIL_PASSWORD`: Senha de aplicativo do e-mail.
   - `EMAIL_RECIPIENT`: E-mail que receberá a notificação.

## 📦 Estrutura de Arquivos

```
├── .env.example          # Modelo de variáveis de ambiente
├── config.py             # Configurações
├── main.py               # Ponto de entrada
├── requirements.txt      # Dependências
├── src/
│   ├── pages/            # Page Objects
│   └── services/         # Serviços (E-mail, Workflow)
└── .github/workflows/    # Configuração do CI/CD
```

## 📄 Licença

Este projeto é de código aberto. Sinta-se à vontade para usar e modificar.

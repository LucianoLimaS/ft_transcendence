# ft_transcendence

## Resumo
Este projeto consiste na criação de um site para jogar Pong contra outros jogadores, com uma interface de usuário agradável e suporte para jogos multiplayer online em tempo real. É uma oportunidade de aplicar e expandir seus conhecimentos em desenvolvimento web, segurança, e outras áreas da ciência da computação.

## Requisitos Técnicos Mínimos
- **Frontend**: Desenvolvido em JavaScript puro (vanilla).
- **Backend**: Opcional, mas se utilizado deve ser desenvolvido em Ruby puro, a menos que o módulo Framework seja utilizado.
- **Compatibilidade**: O site deve ser compatível com a versão mais recente do Google Chrome.
- **Aplicação de Página Única (SPA)**: O site deve ser uma aplicação de página única.
- **Lançamento**: Deve ser possível iniciar tudo com um único comando via Docker, usando `docker-compose up --build`.

## Funcionalidades Obrigatórias
- **Jogo Pong**: Usuários poderão participar de um jogo Pong ao vivo contra outro jogador diretamente no site.
- **Torneios**: Sistema de torneio que permite que múltiplos jogadores joguem uns contra os outros em uma ordem definida.
- **Registro de Jogadores**: Sistema de registro de jogadores com inserção de alias para participar dos torneios.
- **Sistema de Matchmaking**: Organização de partidas entre os jogadores inscritos no torneio.

## Preocupações de Segurança
- **Senhas**: Qualquer senha armazenada deve ser criptografada.
- **Proteção**: O site deve ser protegido contra injeções SQL/XSS e deve utilizar HTTPS para todas as conexões.
- **Validação**: Validação de formulários e entradas do usuário é obrigatória.
- **Gerenciamento de Credenciais**: Credenciais, chaves de API e variáveis de ambiente devem ser armazenadas localmente em um arquivo `.env` e ignoradas pelo Git.

## Módulos Disponíveis
Para completar o projeto com 100% de pontuação, é necessário implementar pelo menos 7 módulos principais. Alguns exemplos de módulos incluem:

- **Web**:
  - Uso de um Framework como backend (Django).
  - Integração de Blockchain para armazenamento de pontuação em Ethereum.

- **Gerenciamento de Usuários**:
  - Autenticação padrão e gestão de usuários.
  - Autenticação remota via OAuth 2.0.

- **Experiência de Jogabilidade**:
  - Jogadores remotos.
  - Suporte para múltiplos jogadores.

- **Cibersegurança**:
  - Implementação de WAF/ModSecurity e HashiCorp Vault para gestão de segredos.
  - Conformidade com GDPR e autenticação de dois fatores (2FA).

- **DevOps**:
  - Configuração de infraestrutura para gerenciamento de logs usando ELK (Elasticsearch, Logstash, Kibana).
  - Monitoramento com Prometheus/Grafana.

## Como Executar
1. Certifique-se de que Docker e Docker Compose estão instalados.
2. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/ft_transcendence.git
   ```
3. Navegue até o diretório do projeto:
   ```bash
   cd ft_transcendence
   ```
4. Inicie o projeto com o Docker:
   ```bash
   docker-compose up --build
   ```

## Licença
Este projeto é licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
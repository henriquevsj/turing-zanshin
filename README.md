# turing-core

## **Visão geral do projeto**

Turing é uma plataforma de integração e distribuição de informação sobre analises de vulnerabilidades end to end que oferece funcionalidades avançadas, segurança robusta e facilidade de uso. Com sua arquitetura flexível e tecnologias modernas, Turing ajuda as organizações a otimizar seus processos, melhorar a colaboração entre equipes e alcançar maior eficiência operacional.

## **Arquitetura do sistema**

O sistema Turing é composto por diversos componentes que trabalham em conjunto para fornecer funcionalidades de integração e distribuição. A arquitetura geral do sistema inclui:

1. **Frontend**: Interface de usuário acessível por meio de um navegador da web. Permite aos usuários interagir com as funcionalidades da plataforma, configurar integrações e visualizar dados através do Retool.
2. **Backend**: Responsável por gerenciar a lógica de negócios, processar solicitações do cliente, autenticar usuários, acessar bancos de dados e interagir com outras APIs externas, construído através de microserviços visando a manutenção e atualização a longo prazo.  
3. **Banco de Dados**: Armazena informações sobre integrações configuradas, dados de usuário, registros de atividades e principalmente o registro atual e histórico de vulnerabilidades.
4. **APIs Externas**: Integrações com APIs de terceiros para acessar dados e funcionalidades adicionais, como bancos de dados de clientes, sistemas de CRM, ferramentas de desenvolvimento, entre outros.

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/dc003310-0060-4aae-9207-54c030384e05/68736597-8f4e-47f9-bb4a-1217c6350b3f/Untitled.png)

## **Stack de Tecnologia**

- **Frontend**: Retool
- **Backend**: Python
- **Banco de Dados**: MongoDB
- **Autenticação**: OAuth para autenticação de usuário
- **Integrações**: APIs RESTful e SDK’s
- **Controle de Versão**: GitHub
- **CI/CD:** GitHub Actions
- **Secrets**: GitHub Secrets e Azure KeyVault
- **Implantação**: Azure Function

## **Funcionalidades Principais**

### **1. Configurações de coleta e distribuição**

Os usuários podem configurar distribuições entre diferentes sistemas e ferramentas de descobertas de vulnerabilidades, especificando os parâmetros de conexão as regras de sincronização de dados e para onde desejam disponibilizar os dados coletados. 

Atualmente contempla as seguintes categorias:

- Cloud Security
    - CSPM
        - Palo Alto Prisma
        - Zanshin
- Desenvolvimento
    - SAST
        - SonarQube
        - Semgrep
    - DAST
        - Nessus
    - SCA
        - Dependaboot
        - Snyk
- Gerenciamento
    - Jira
    - Microsoft Teams

Próximos:

- KSPM
- Verificação da infraestrutura como código

### **2. Monitoramento e Gerenciamento**

Os usuários têm acesso a painéis nativos de controle que permitem monitorar o status das integrações, visualizar logs de atividades, gerenciar configurações, visualizar dados detalhados sobre todas as vulnerabilidades encontradas e ver informações com insights inteligentes sobre processos ou ferramentas.

### **3. Autenticação e Segurança**

O sistema Turing implementa medidas de segurança robustas, como autenticação de dois fatores, criptografia de dados e auditoria de acesso, para garantir a proteção dos dados do usuário.

### **4. Notificações e Alertas**

Os usuários podem configurar notificações e alertas para serem informados sobre eventos importantes relacionados às integrações, como erros de sincronização, alterações nos dados ou atividades suspeitas.

## **Fluxo de Funcionamento**

1. O usuário acessa a plataforma Turing por meio do Retool.
2. O usuário configura integrações, especificando os sistemas e ferramentas a serem conectados e as regras de sincronização de dados.
3. O backend processa as solicitações do usuário, autentica o usuário, acessa os bancos de dados e interage com APIs externas conforme necessário.
4. As integrações são ativadas e monitoradas pelo sistema.
5. Os dados são sincronizados entre os sistemas conectados de acordo com as configurações definidas pelo usuário.
6. O usuário recebe notificações e alertas sobre eventos relevantes relacionados às integrações.
7. O usuario visualiza os dados coletados através de dashboards e ex

## **Considerações de Segurança**

- Todos os dados transmitidos entre o cliente e o servidor são criptografados usando SSL/TLS para garantir a segurança das informações.
- As senhas dos usuários são armazenadas de forma segura usando técnicas de hash e salt.
- O acesso aos recursos do sistema é controlado por meio de permissões e políticas de acesso baseadas em função.
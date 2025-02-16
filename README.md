# Ferramenta de Automação para Dispositivos de Redes!

Bem-vindo à ferramenta de automação para dispositivos! Esta ferramenta foi desenvolvida para simplificar a administração e o gerenciamento de dispositivos de rede, permitindo a execução de comandos configuráveis via SSH.

## Sumário
- [Apresentação da Ferramenta](#apresentação-da-ferramenta)
- [Funcionalidades Principais](#funcionalidades-principais)
- [Pré-requisitos](#pré-requisitos)
- [Instalação e Configuração](#instalação-e-configuração)
- [Como Usar](#como-usar)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Exemplos de Uso](#exemplos-de-uso)
- [Contribuição](#contribuição)
- [Licença](#licença)
- [Contato](#contato)

## Apresentação da Ferramenta
Esta ferramenta foi criada para auxiliar administradores de rede na execução de comandos em dispositivos de forma automatizada e organizada. Ela utiliza a biblioteca netmiko para estabelecer conexões SSH e permite:
- Executar comandos de diagnóstico e monitoramento.
- Realizar backups de configurações.
- Gerenciar múltiplos dispositivos de forma centralizada.
- Facilitar o troubleshooting em ambientes complexos.

## Funcionalidades Principais
- **Interface Interativa**: Seleção de clientes, hosts e comandos através de menus simples.
- **Execução Remota de Comandos**: Conexão SSH com dispositivos para execução de comandos.
- **Suporte a VPN Instances**: Identificação e execução de comandos específicos para instâncias de VPN.
- **Backup Automatizado**: Opção para salvar a configuração atual do dispositivo em um arquivo.
- **Paginação de Saídas**: Exibição de saídas longas em blocos de 100 linhas.
- **Segurança**: Uso de getpass para entrada segura de senhas.

## Pré-requisitos
Antes de utilizar a ferramenta, certifique-se de que os seguintes requisitos estão atendidos:
- **Python 3.x**: A ferramenta foi desenvolvida em Python. Certifique-se de ter o Python instalado.
- **Bibliotecas Necessárias**:
  - netmiko: Para conexões SSH.
  - getpass: Para entrada segura de senhas.
  - json: Para manipulação de arquivos JSON.
  - os: Para manipulação de caminhos de arquivos.
- **Arquivo de Configuração**: Um arquivo JSON (hosts_by_client.json) contendo a lista de clientes e hosts.

## Instalação e Configuração
1. Clone o Repositório:
   ```bash
   git clone https://github.com/FelipeC0d3r-Git/automation_by_netmiko.git
   cd automation_by_netmiko
   ```
2. Instale as Dependências:
   ```bash
   pip install netmiko
   ```
3. Prepare o Arquivo de Hosts:
   Crie um arquivo `hosts_by_client.json` no mesmo diretório do script com o formato abaixo:
   ```json
   {
     "Cliente A": [
       {"name": "Host 1", "host": "192.168.1.1", "id": "001"},
       {"name": "Host 2", "host": "192.168.1.2", "id": "002"}
     ],
     "Cliente B": [
       {"name": "Host 3", "host": "192.168.1.3", "id": "003"}
     ]
   }
   ```

## Como Usar
1. **Autenticação**:
   - Ao iniciar o script, você será solicitado a fornecer seu nome de usuário e senha.
2. **Seleção de Cliente**:
   - Escolha um cliente da lista exibida.
3. **Seleção de Host**:
   - Escolha um host dentro do cliente selecionado.
4. **Seleção de Comandos**:
   - Escolha um grupo de comandos e, em seguida, um comando específico para execução.
5. **Execução**:
   - O comando será executado no dispositivo selecionado, e a saída será exibida.
6. **Opções Adicionais**:
   - Para saídas longas, a ferramenta oferece paginação.
   - Para comandos como `display current-configuration`, você pode optar por salvar um backup.

## Estrutura do Projeto
```
/
├── main.py                # Script principal da ferramenta.
├── hosts_by_client.json   # Arquivo JSON com a lista de clientes e hosts.
├── commands.py            # Arquivo contendo os grupos de comandos.
├── README.md              # Este arquivo.
└── requirements.txt       # Lista de dependências (opcional).
```

## Exemplos de Uso
- **Verificar Sessões BGP**:
   - Selecione o grupo de comandos "Visualização de Sessão BGP".
   - Escolha um comando como `display bgp vpnv4 vpn-instance {vpn_instance} peer`.
   - A ferramenta identificará as VPN instances disponíveis e permitirá a execução do comando.
- **Realizar Backup**:
   - Execute o comando `display current-configuration`.
   - Quando solicitado, confirme se deseja salvar o backup.
- **Verificar Tabela de Roteamento**:
   - Execute comandos como `display ip routing-table`.
   - A ferramenta exibirá a saída em blocos de 100 linhas.

## Contribuição
Contribuições são bem-vindas! Siga os passos abaixo:
1. Faça um fork do repositório.
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`).
3. Commit suas mudanças (`git commit -m 'Adicionando nova feature'`).
4. Push para a branch (`git push origin feature/nova-feature`).
5. Abra um Pull Request.

## Licença
Este projeto está licenciado sob a licença MIT. Consulte o arquivo LICENSE para mais detalhes.

## Contato
Se tiver dúvidas ou sugestões, entre em contato:
- E-mail: ft.oliveira.ti@gmail.com
- GitHub: [FelipeC0d3r-Git](https://github.com/FelipeC0d3r-Git)

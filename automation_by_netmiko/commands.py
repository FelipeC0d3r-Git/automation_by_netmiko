# commands.py

commands_groups = {
    "Visualização de Configuração": [
        "display current-configuration | include ip vpn-instance # Mostra a configuração atual incluindo instâncias VPN",
        "display current-configuration # Mostra a configuração atual"
    ],
    "Visualização de Sessão BGP": [
        "display bgp peer # Mostra as sessões BGP v4",
        "display bgp ipv6 peer # Mostra as sessões BGP v6",
        "display bgp vpnv4 vpn-instance {vpn_instance} peer # Mostra as sessões BGP VPNv4 VPN-Instance",
        "display bgp vpnv6 vpn-instance {vpn_instance} peer # Mostra as sessões BGP VPNv6 VPN-Instance"
    ],
    "Visualização de Log": [
        "display logbuffer # Mostra o buffer de log",
        "display trapbuffer # Mostra o buffer de trap"
    ],
    "Visualização de IPs": [
        "display ip interface brief # Mostra um resumo das interfaces IP",
        "display ip routing-table # Mostra a tabela de roteamento IP"
    ],
    "Visualização de Interfaces": [
        "display interface brief # Mostra um resumo das interfaces",
        "display interface description # Mostra a descrição das interfaces"
    ]
}
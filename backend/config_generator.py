def generate_wireguard_config(vpn):
    return f"""
[Interface]
PrivateKey = {vpn.private_key}
Address = {vpn.assigned_ip}/24
DNS = 1.1.1.1

[Peer]
PublicKey = SERVER_PUBLIC_KEY_PLACEHOLDER
Endpoint = SERVER_IP_PLACEHOLDER:51820
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25
""".strip()
from wireguard import generate_keypair

private_key, public_key = generate_keypair()

print("PRIVATE:", private_key)
print("PUBLIC :", public_key)
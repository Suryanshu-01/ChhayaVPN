import subprocess


def generate_keypair():
    private_key = (
        subprocess.check_output(
            ["wg", "genkey"],
            text=True
        )
        .strip()
    )

    public_key = (
        subprocess.check_output(
            ["wg", "pubkey"],
            input=private_key,
            text=True
        )
        .strip()
    )

    return private_key, public_key
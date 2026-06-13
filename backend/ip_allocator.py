from models import VPNProfile


def get_next_ip(db):
    vpns = (
        db.query(VPNProfile)
        .order_by(VPNProfile.id.desc())
        .first()
    )

    if not vpns:
        return "10.0.0.2"

    last_ip = vpns.assigned_ip

    last_octet = int(
        last_ip.split(".")[-1]
    )

    next_octet = last_octet + 1

    if next_octet > 254:
        raise Exception(
            "VPN network exhausted"
        )

    return f"10.0.0.{next_octet}"
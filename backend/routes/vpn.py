from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import VPNProfile, Account
from schemas import VPNProfileResponse
from auth import get_current_user
from typing import List
from wireguard import generate_keypair
from fastapi.responses import PlainTextResponse,Response
from config_generator import generate_wireguard_config
from ip_allocator import get_next_ip




# Future Security Roadmap
# -----------------------
# ✓ Database encryption
# ✓ Key management
# ✓ Secret storage
# ✓ Server private key protection
# ✓ Production security review
# Database encryption Key management Secret storage we will do it in future remember ok

router=APIRouter()

@router.post(
    "/create",
    response_model=VPNProfileResponse
)
def create_vpn(
    db: Session = Depends(get_db),
    current_user: Account = Depends(get_current_user)
):
    private_key,public_key=generate_keypair()
    vpn = VPNProfile(
        owner_id=current_user.id,
        public_key=public_key,
        private_key=private_key,
        assigned_ip=get_next_ip(db)
    )

    db.add(vpn)
    db.commit()
    db.refresh(vpn)

    return vpn


@router.get(
    "/my-vpns",
    response_model=List[VPNProfileResponse]
)
def get_my_vpns(
    db: Session = Depends(get_db),
    current_user: Account = Depends(get_current_user)
):
    vpns = (
        db.query(VPNProfile)
        .filter(
            VPNProfile.owner_id == current_user.id
        )
        .all()
    )

    return vpns


@router.delete("/{vpn_id}")
def delete_vpn(
    vpn_id:int,
    db:Session=Depends(get_db),
    current_user:Account=Depends(get_current_user)
):
    vpn=(
        db.query(VPNProfile)
        .filter(VPNProfile.id==vpn_id)
        .first()
    )

    if not vpn:
        raise HTTPException(
            status_code=404,
            detail="VPN profile not found"
        )
    
    if vpn.owner_id!=current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to delete this VPN"
        )
    
    db.delete(vpn)
    db.commit()

    return{
        "message":"VPN profile deleted successfully"
    }



@router.get("/{vpn_id}/config")
def download_config(
    vpn_id: int,
    db: Session = Depends(get_db),
    current_user: Account = Depends(get_current_user)
):
    vpn = (
        db.query(VPNProfile)
        .filter(VPNProfile.id == vpn_id)
        .first()
    )

    if not vpn:
        raise HTTPException(
            status_code=404,
            detail="VPN profile not found"
        )

    if vpn.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    config = generate_wireguard_config(vpn)

    return PlainTextResponse(config)


@router.get("/{vpn_id}/download")
def download_config(
    vpn_id: int,
    db: Session = Depends(get_db),
    current_user: Account = Depends(get_current_user)
):
    vpn = (
        db.query(VPNProfile)
        .filter(VPNProfile.id == vpn_id)
        .first()
    )

    if not vpn:
        raise HTTPException(
            status_code=404,
            detail="VPN profile not found"
        )

    if vpn.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    config = generate_wireguard_config(vpn)

    return Response(
        content=config,
        media_type="text/plain",
        headers={
            "Content-Disposition":
            f'attachment; filename="vpn-{vpn.id}.conf"'
        }
    )
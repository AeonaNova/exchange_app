from db import Session, Wallet
from fastapi import FastAPI, Depends

app = FastAPI()

async def get_db():
    session_l = Session()
    try:
        yield session_l
    finally:
        session_l.close()


@app.post('/api/v1/wallets/<WALLET_UUID>/operation')
async def exchange(uuid: str, balance: float, operation: str, db: Session = Depends(get_db)):

    wallet = db.query(Wallet).filter(Wallet.uuid == uuid).first()
    if not wallet:
        wallet = Wallet(uuid=uuid, balance=balance)
        db.add(wallet)
        db.commit()
        return {"wallet has been created with new incoming quantity:": balance}
    if str(operation) == "DEPOSIT":
        wallet.balance += balance
    elif str(operation) == "WITHDRAW":
        if wallet.balance-balance > 0:
            wallet.balance -= balance
        else: return {"not enough value:": "uncompleted balance"}
    db.commit()
    return {"status:": "successful"}


@app.get('/api/v1/wallets/{WALLET_UUID}')
async def get_wallet(uuid: str, db: Session = Depends(get_db)):
    balance = db.query(Wallet).filter(Wallet.uuid == uuid).first()
    if balance:
        return {"balance:": balance.balance}
    else:
        wallet = Wallet(uuid=uuid, balance=0.0)
        db.add(wallet)
        return {"wallet has been created with new incoming quantity:": wallet.balance}

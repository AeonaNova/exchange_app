from db import Session, Wallet
from fastapi import FastAPI, Depends

app = FastAPI()

def get_db():
    session_l = Session()
    try:
        yield session_l
    finally:
        session_l.close()


@app.post('/api/v1/wallets/{WALLET_UUID}/operation')
def exchange(WALLET_UUID: str, balance: float, operation: str, db: Session = Depends(get_db)):

    wallet = db.query(Wallet).filter(Wallet.uuid == WALLET_UUID).first()
    if not wallet:
        wallet = Wallet(uuid=WALLET_UUID, balance=balance)
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
def get_wallet(WALLET_UUID: str, db: Session = Depends(get_db)):
    balance = db.query(Wallet).filter(Wallet.uuid == WALLET_UUID).first()
    if balance:
        return {"balance:": balance.balance}
    else:
        wallet = Wallet(uuid=WALLET_UUID, balance=0.0)
        db.add(wallet)
        db.commit()
        return {"wallet has been created with new incoming quantity:": wallet.balance}

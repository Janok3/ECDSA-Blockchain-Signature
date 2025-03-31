import random

from DS import KeyGen, SignGen

def concatenateData(serial_number, amount, receiver_beta, sender_beta):
    """Hashes the transaction data into a fixed-length digest using SHA3_256."""
    return f"{serial_number}{amount}{receiver_beta}{sender_beta}".encode()
    

def formatData(s, h, serialNumber, amount, recieverBeta, senderBeta):
    """Return a string representation of the transaction."""
    return (
        f"**** Bitcoin transaction ****\n"
        f"Signature (s): {s}\n"
        f"Signature (h): {h}\n"
        f"Serial number: {serialNumber}\n"
        f"Amount: {amount}\n"
        f"Payee public key (beta): {recieverBeta}\n"
        f"Payer public key (beta): {senderBeta}"
    )


def gen_random_tx(q, p, g):
    senderSK, senderPK = KeyGen(q,p,g) 
    receiverSK, receiverPK = KeyGen(q, p, g)
    serialNumber = random.getrandbits(128)
    amount = random.randint(1, 1000000)
    
    data = (f"Serial number: {serialNumber}\n"
            f"Amount: {amount}\n"
            f"Payee public key (beta): {receiverPK}\n"
            f"Payer public key (beta): {senderPK}\n"
        )
   
    s, h = SignGen(data, q, p, g, senderSK)
    

    return formatData(s, h, serialNumber, amount, receiverPK, senderPK)

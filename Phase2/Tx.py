import random
import os

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

def gen_random_txblock(q, p, g, TxCnt, filename):
    # check TxCnt to make sure it is a power of 2
    
    if os.path.exists(filename) == False:
        with open(filename, 'w') as file:
            for _ in range(TxCnt):
                file.write(gen_random_tx(q, p, g) + "\n")  # Adds a newline after each block
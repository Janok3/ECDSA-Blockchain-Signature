from hashlib import sha3_256
import random

def parseByBlock(filename, TxCnt):
    with open(filename, 'r') as file:
        lines = file.readlines()
        
        nonce = None
        currentLine = 0

        # Check if the first line contains the nonce
        if lines[0].startswith("Nonce: "):
            nonce_str = lines[0].split(':')[1].strip()
            nonce = int(nonce_str)
            currentLine = 1
        
        # Rest of the file contains transactions, 7 lines per transaction
        transactions = []
        
        while currentLine < len(lines) and len(transactions) < TxCnt:
            if currentLine + 6 <= len(lines):
                txLines = lines[currentLine:currentLine + 7]
                tx = ''.join(txLines)
                transactions.append(tx)
            currentLine += 7
            
        return nonce, transactions

def calculateMerkleRoot(transactions):
    if not transactions:
        return None
    
    # Hash all transactions individually
    hashes = [sha3_256(tx.encode()).digest() for tx in transactions]
    
    # Build the Merkle tree
    while len(hashes) > 1:
        if len(hashes) % 2 == 1:
            hashes.append(hashes[-1])  # Duplicate last hash if odd number
        
        nextLevel = []
        for i in range(0, len(hashes), 2):
            combined = hashes[i] + hashes[i + 1]
            nextHash = sha3_256(combined).digest()
            nextLevel.append(nextHash)
        hashes = nextLevel
    
    return hashes[0] if hashes else None

def CheckPow(p, g, q, PoWLen, TxCnt, filename):
    # Read the block file
    nonce, transactions = parseByBlock(filename, TxCnt)

    # Compute Merkle root of transactions
    merkleRoot = calculateMerkleRoot(transactions)
    
    print(f"H_r: {merkleRoot}")

    # Convert nonce to bytes and append to Merkle root
    nonceBytes = nonce.to_bytes((nonce.bit_length() + 7) // 8, byteorder='big')
    combined = merkleRoot + nonceBytes
    
    # Compute final PoW hash
    powHash = sha3_256(combined).hexdigest()
    
    # Verify the required number of leading zeros
    prefix = '0' * PoWLen
    if powHash.startswith(prefix):
        return powHash

    return ""

def formatReturnString(nonce, transactions):
    toReturn = "Nonce: " + str(nonce) + "\n"
    
    for transaction in transactions:
        toReturn += transaction

    return toReturn

def PoW(PoWLen, q, p, g, TxCnt, filename):
    _, transactions = parseByBlock(filename, TxCnt)
    
    # print(transactions)
    merkleRoot = calculateMerkleRoot(transactions)
    prefix = '0' * PoWLen

    nonce = 0
    while True:
        # nonce = random.getrandbits(32)
        nonceBytes = nonce.to_bytes((nonce.bit_length() + 7) // 8, byteorder='big')
        combined = merkleRoot + nonceBytes

        powHash = sha3_256(combined).hexdigest()

        if powHash.startswith(prefix):
            return formatReturnString(nonce, transactions)
        nonce += 1


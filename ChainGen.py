from hashlib import sha3_256

def calculateHashTree(block_candidate, TxCnt):
        hashTree = []
        for i in range(0, TxCnt):
            transaction = "".join(block_candidate[i*9:(i+1)*9])
            hashTree.append(sha3_256(transaction.encode('UTF-8')).digest())
        
        t = TxCnt
        j = 0
        while(t > 1):
            for i in range(j, j+t, 2):
                hashTree.append(sha3_256(hashTree[i] + hashTree[i+1]).digest())
            j += t
            t = t >> 1
        
        return hashTree[2*TxCnt-2]

def AddBlock2Chain(PoWLen, TxCnt, block_candidate, PrevBlock):
    # For first block
    if PrevBlock == "":
        prevPoW = "0" * 20
    else:
        # Get previous block's PoW from the block content itself
        # previous_pow = SHA3_256.new(''.join(PrevBlock[2:]).encode('UTF-8')).hexdigest().encode('UTF-8') Wrong old implementation
        PrevH_r = calculateHashTree(PrevBlock[2:], TxCnt)
        PrevNonce = int(PrevBlock[1].split(": ")[1].strip())
        PrevPrevPoW = PrevBlock[0].split(": ")[1].strip()

        PrevPrevPoWBytes = PrevPrevPoW.encode()
        PrevNonceBytes = PrevNonce.to_bytes((PrevNonce.bit_length()+7)//8, byteorder='big')

        digest = PrevH_r + PrevPrevPoWBytes + PrevNonceBytes
        prevPoW = sha3_256(digest).hexdigest()

    H_r = calculateHashTree(block_candidate, TxCnt)
    # print(H_r)
    
    # Find nonce and PoW of current block
    nonce = 0
    currentPoW = ""
    while True:
        nonceBytes = nonce.to_bytes((nonce.bit_length()+7)//8, byteorder='big')
        prevPoWBytes = prevPoW.encode()

        digest = H_r + prevPoWBytes + nonceBytes
        currentPoW = sha3_256(digest).hexdigest()
        
        if currentPoW.startswith("0" * PoWLen):
            break

        nonce += 1
    
    # Create new block
    blockContent = ''.join(block_candidate)
    newBlock = f"Previous PoW: {prevPoW}\nNonce: {nonce}\n{blockContent}"
    
    return newBlock, currentPoW







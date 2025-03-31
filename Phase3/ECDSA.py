from hashlib import sha3_256
import random
from ecpy.curves import Curve,Point
from Crypto.Hash import SHA3_256

def KeyGen(E):
    n = E.order
    P = E.generator
    # Generate a random private key sA
    sA = random.randint(1, n - 1)
    # Compute the public key QA = sA * G, where P is the generator point of the curve
    QA = sA * P
    return sA, QA

def SignGen(message, E, sA):
    n = E.order
    P = E.generator
    
    while True:
        k = random.randint(1, n - 1)
        R = k * P
        r = R.x
        
        # Hash message with x-coordinate of kP
        rBytes = r.to_bytes((r.bit_length() + 7) // 8, byteorder='big')
        h = int.from_bytes(SHA3_256.new(message + rBytes).digest(), byteorder='big') % n
        
        s = (k - sA * h) % n
        if s != 0:
            break
    
    return s, h

def SignVer(message, s, h, E, QA):
    n = E.order
    P = E.generator
    
    # Calculate v = s * P + h * QA
    v = s * P + h * QA
    
    # Hash message with x-coordinate of v
    vBytes = v.x.to_bytes((v.x.bit_length() + 7) // 8, byteorder='big')
    u = int.from_bytes(SHA3_256.new(message + vBytes).digest(), byteorder='big') % n
    
    return 0 if u == h else -1


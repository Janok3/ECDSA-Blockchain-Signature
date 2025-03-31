import os
import sympy
import random
import warnings
import string
from Crypto.Hash import SHA3_256
import random

def GenerateOrRead(filename):
    """ Generate or read public parameters q, p, g. """
    if os.path.exists(filename) == False:
        q, p, g = pubParGen()
        with open(filename, 'w') as file:
            file.write(str(q) + '\n')
            file.write(str(p) + '\n')
            file.write(str(g) + '\n')
    with open(filename, 'r') as f:
        q = int(f.readline().strip())
        p = int(f.readline().strip())
        g = int(f.readline().strip())
    return (q, p, g)


def random_prime(bitsize):
    warnings.simplefilter('ignore')
    chck = False
    while chck == False:
        p = random.randrange(2**(bitsize-1), 2**bitsize-1)
        chck = sympy.isprime(p)
    warnings.simplefilter('default')    
    return p

def large_DL_Prime(q, bitsize):
    warnings.simplefilter('ignore')
    while True:
        # Generate k to ensure p is close to the desired bit size
        k = random.randrange(2**(bitsize - len(bin(q)[2:]) - 1), 2**(bitsize - len(bin(q)[2:])))
        p = k * q + 1
        if p.bit_length() == bitsize and sympy.isprime(p):  # Ensure correct bit size and primality
            warnings.simplefilter('default')
            return p

def pubParGen():
    qsize = 224 
    psize = 2048
    q = random_prime(qsize)
    p = large_DL_Prime(q, psize)
    tmp = (p-1)//q
    g = 1
    while g == 1:
        alpha = random.randrange(1, p)
        g = pow(alpha, tmp, p)
    return q, p, g


def random_string(length):
    """ Generate a random string of fixed length. """

    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def KeyGen(q, p, g):
    """  
    A user picks a random secret key 0 < a < q - 1 and computes the public
    key β = g^a mod p.
    """

    a = random.randint(1, q) # private key
    b = pow(g, a, p)         # public key
    return a, b

def SignGen(message, q, p, g, alpha):
    """
    Signature generation: Let m be an arbitrary length message. The signature is computed
    as follows:
    1. k ← Zq, (i.e., k is a random integer in [1, q - 2]).
    2. r = g ^k (mod p) 
    3. h = SHA3 256(m||r) (mod q)
    4. s = k - a · h (mod q)
    5. The signature for m is the tuple (s, h).
    """

    # if isinstance(alpha, bytes):
    #     alpha = int.from_bytes(alpha, byteorder='big')
    
    # Ensure the message is in bytes
    if not isinstance(message, bytes):
        message = str(message).encode('utf-8')  # Convert to bytes if not already


    # Step 1: Generate a random k in [1, q-2]
    k = random.randint(1, q - 2)

    # Step 2: Compute r = g^k mod p
    r = pow(g, k, p)

    # Step 3: Compute h = SHA3-256(m || r) mod q
    # Concatenate the message and r as bytes
    r_bytes = r.to_bytes((r.bit_length() + 7) // 8, byteorder='big')
    hasher = SHA3_256.new()
    hasher.update(message + r_bytes)
    h = int.from_bytes(hasher.digest(), byteorder='big') % q

    # Step 4: Compute s = (k - alpha * h) mod q
    s = (k - (alpha * h)) % q

    # Step 5: Return the signature (s, h)
    return (s, h)


def SignVer(message, s, h, q, p, g, beta):
    """ 
    Let m be a message and the tuple (s, h) is a signature for m. The
    verification proceeds as follows:
    - v = g^s*β^h (mod p)
    - u = SHA3 256(m||v) (mod q)
    - Accept the signature only if u = h
    - Reject it otherwise. 
    """

    # Ensure the message is in bytes
    if not isinstance(message, bytes):
        message = str(message).encode('utf-8')  # Convert to bytes if not already

    v = (pow(g, s, p) * pow(beta, h, p)) % p

    # Concatenate the message and v as bytes
    v_bytes = v.to_bytes((v.bit_length() + 7) // 8, byteorder='big')
    hasher = SHA3_256.new()
    hasher.update(message + v_bytes)
    u = int.from_bytes(hasher.digest(), byteorder='big') % q
    
    # print("u:",u)
    # print("h:",h)

    if u == h:
        return 0
    else:
        return -1  
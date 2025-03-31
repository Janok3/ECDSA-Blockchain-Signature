# Blockchain Cryptography Project

## Project Description
This project implements core cryptographic components for a blockchain system across three phases. The implementation focuses on digital signatures, transaction processing, proof-of-work consensus, and blockchain construction.

## Phase Breakdown

### Phase I: Digital Signatures & Transactions
**Core Components:**
- Digital signature scheme using 224-bit/2048-bit primes
- Blockchain transaction generation and validation

**Key Files:**
- `DS.py`  
  - Implements:  
    ✓ Public parameter generation (`q|p-1`)  
    ✓ Key pair generation  
    ✓ Signature creation/verification (modified DSA variant)  
    ✓ SHA3-256 hashing integration

- `Tx.py`  
  - Generates valid transactions containing:  
    ✓ Dual-part signatures (s,h)  
    ✓ 128-bit serial numbers  
    ✓ Satoshi-denominated amounts  
    ✓ Payer/payee public keys

### Phase II: Transaction Blocks & Proof-of-Work
**Core Components:**
- Merkle tree construction
- Mining simulation with adjustable difficulty

**Key Files:**
- Enhanced `Tx.py`  
  - Adds `gen_random_txblock()` for bulk transaction generation
  - Enforces power-of-two transaction counts

- `PoW.py`  
  - Implements mining logic:  
    ✓ Nonce discovery  
    ✓ Leading zero validation (PoWLen configurable)  
    ✓ Merkle root hashing with SHA3-256

**Optimization Note:**
- Recommends testing with PoWLen=3 before attempting higher values

### Phase III: ECDSA & Blockchain
**Core Components:**
- Elliptic Curve cryptography integration
- Block chaining mechanism

**Key Files:**
- `ECDSA.py`  
  - Replaces Phase I signatures with:  
    ✓ EC point arithmetic (using `ecpy`)  
    ✓ Revised transaction structure

- `ChainGen.py`  
  - Implements blockchain growth via:  
    ✓ Previous PoW linking  
    ✓ Genesis block handling  
    ✓ Chain validation checks


## Technical Specifications
- **Hashing:** SHA3-256 throughout
- **Key Sizes:** 
  - Phase I: 224-bit q / 2048-bit p
  - Phase III: 256-bit ECC
- **Nonce Handling:** Big-endian byte conversion

## Validation Approach
Each phase includes dedicated test files (`Phase*_Test.py`) that verify:
- Cryptographic correctness
- Structural requirements
- Consensus rule compliance

# VoteChain Architecture & Design

Complete documentation of the Secure Voting System's architecture, design decisions, and implementation details.

## Overview

VoteChain is a **Streamlit-based web application** that demonstrates secure voting using:
- **Blind Signatures** for voter anonymity
- **RSA Cryptography** for authenticity
- **Blockchain** for immutability
- **Session State** for state management

## System Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Streamlit App                      │
│  (Single Page App with Multi-Page Navigation)       │
└──────────────────┬──────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
    ┌───▼────┐          ┌────▼────┐
    │ Frontend│          │ Backend │
    │ (Pages) │          │ (Logic) │
    └─────────┘          └────┬────┘
                              │
                    ┌─────────┼──────────┐
                    │         │          │
                 ┌──▼-─┐   ┌───▼──┐  ┌───▼──┐
                 │Utils│   │Crypto│  │Chain │
                 └─────┘   └──────┘  └──────┘
```

## Component Breakdown

### 1. Frontend (Streamlit Pages)

**app.py** (Home)
- Landing page with system overview
- Key concepts explanation
- Status dashboard
- Navigation guide

**pages/1_setup.py** (Setup)
- Step 1: Generate government RSA keys
- Step 2: Create voter key files
- Step 3: Configure candidates
- Step 4: Initialize election

**pages/2_vote.py** (Voting)
- Step 1: Authenticate with voter key
- Step 2: Select candidate
- Step 3: Crypto theater (blind → sign → unblind)
- Step 4: Submit vote
- Step 5: Display receipt

**pages/3_results.py** (Results)
- Real-time vote tallies
- Vote distribution charts
- Election status metrics
- Blockchain statistics

**pages/4_verify.py** (Verification)
- Receipt code search
- Blockchain integrity check
- Blockchain explorer
- Export blockchain data

### 2. Backend Modules

#### crypto.py
Cryptographic utilities for:
- RSA key generation
- Signing/verification
- **Blind signature protocol** (key innovation)
- Message hashing
- Key import/export

Key functions:
```python
# Key generation
private_key, public_key = generate_rsa_keys()

# Blind signature protocol
blinded_msg, factor = blind_message(vote, public_key)
signature = sign_blinded_message(blinded_msg, private_key)
final_sig = unblind_signature(signature, factor, public_key)
```

#### blockchain.py
Lightweight blockchain implementation:
- Simple block structure with cryptographic links
- Genesis block on initialization
- Vote recording with receipts
- Chain validation
- Receipt lookup

Key class:
```python
blockchain = Blockchain()
block = blockchain.add_vote(vote_hash, signature, receipt_code)
is_valid = blockchain.is_chain_valid()
```

#### utils.py
Application utilities:
- Session state initialization
- Vote counting
- Receipt generation
- Voter tracking (prevent double-voting)
- Election state management

Key functions:
```python
initialize_session_state()
receipt_code = generate_receipt_code()
increment_vote_count(candidate)
has_already_voted(voter_id)
```

## State Management

### Session State Variables

```python
st.session_state:
├── Government Keys
│   ├── government_private_key (RSA)
│   └── government_public_key (RSA)
├── Voter State
│   ├── authenticated_voter_id (str)
│   ├── current_voter_key (RSA)
│   └── current_selection (str)
├── Election Config
│   ├── candidates (list)
│   ├── election_initialized (bool)
│   └── num_voters (int)
├── Blockchain
│   └── blockchain (Blockchain object)
├── Vote Tracking
│   ├── voted_voters (set)
│   ├── voter_receipts (dict)
│   └── vote_counts (dict)
└── Session Artifacts
    ├── current_receipt (str)
    └── crypto_complete (bool)
```

### State Initialization

Called at page load via `initialize_session_state()`:
- Sets defaults for all session variables
- Creates blockchain instance
- Initializes empty vote counts

### State Flow

```
Setup Page:
  user → generate keys → auth voter → configure candidates → init election
    ↓ (stores in session)
    government_private_key ✓
    government_public_key ✓
    candidates ✓
    election_initialized ✓

Vote Page:
  user → upload key → authenticate → select → crypto → cast → store
    ↓ (updates session)
    authenticated_voter_id (temp)
    current_selection (temp)
    current_receipt → voted_voters
    vote_counts incremented

Results Page:
  reads vote_counts from session → displays metrics

Verify Page:
  queries blockchain (read-only)
```

## Cryptographic Protocol: The Blind Signature Scheme

### Why Blind Signatures?

Problem: Government must verify voter eligibility WITHOUT seeing the vote

Solution: Blind Signature Protocol

### Protocol Flow

```
Voter                           Government
  |                                |
  |--- blind(vote, n, e) -------->|
  |                                | signs blind value
  |<--- sign(blind_vote) ---------| 
  |                                |
  | unblind(signature, r_inv) -->[internal]
  |
  ✓ Has valid signature for actual vote
  ✓ Government never saw actual vote
  ✓ Voter can prove they got signature
```

### Implementation Details

**Blinding Step:**
```python
blinded = (vote_hash × r^e) mod n
where:
  - vote_hash = SHA256(candidate)
  - r = random blinding factor
  - e = public exponent
  - n = modulus
```

**Unblinding Step:**
```python
unblinded_sig = (blind_sig × r^-1) mod n
where:
  - blind_sig = government's signature
  - r^-1 = modular inverse of r
```

**Property:** blind_sig ≡ actual_vote^d (mod n)
- ∴ It's a valid RSA signature for the actual vote

## Blockchain Implementation

### Block Structure

```python
@dataclass
class Block:
    index: int                  # Position in chain
    timestamp: str             # ISO 8601 timestamp
    vote_hash: str             # SHA256(encrypted vote)
    previous_hash: str         # Hash of previous block
    nonce: int                 # For future PoW expansion
    signature: str             # Voter's unblinded signature
    receipt_code: str          # User-facing receipt
```

### Chain Validation

```python
def is_chain_valid():
    for each block:
        recalc_hash = hash(previous_block)
        if block.previous_hash ≠ recalc_hash:
            return False
    return True
```

### Receipt System

- Receipt = random alphanumeric code (e.g., "A7F3B2C9D1E8")
- Links voter to their block WITHOUT revealing vote
- Only voter has their receipt
- Used for verification: "My vote is in Block #7"

## UX/UI Design

### Components Used

All **Streamlit native** components:
- `st.button()` - Candidate selection, form actions
- `st.file_uploader()` - Key file loading
- `st.status()` - Crypto theater staging
- `st.success/error/warning/info()` - Feedback
- `st.metric()` - Vote counts
- `st.columns()` - Layout
- `st.expander()` - Progressive disclosure
- `st.json()` - Blockchain data

### No Custom CSS/Components

Rationale:
- Single dev, fixed deadline
- Streamlit defaults are professional
- Crypto concepts are the star, not UI
- Reduces bugs and complexity

### Emoji System

Visual scanning and personality:
- 🔐 Blinding/encryption
- ✍️ Signature
- 🗳️ Voting
- ✅ Success
- ❌ Error
- ⚠️ Warning

## Data Flow: Complete Voting Example

```
1. SETUP PHASE
   ├─ Admin clicks "Generate Keys"
   │  └─ `crypto.generate_rsa_keys()` → stores in session_state
   │
   ├─ Admin enters candidates
   │  └─ `st.session_state.candidates = ['Alice', 'Bob']`
   │     └─ `st.session_state.vote_counts = {'Alice': 0, 'Bob': 0}`
   │
   └─ Admin clicks "Initialize Election"
      └─ `election_initialized = True`

2. VOTING PHASE
   ├─ Voter uploads key.pem
   │  └─ `crypto.import_key_from_bytes(key_data)` → current_voter_key
   │
   ├─ Voter selects "Alice"
   │  └─ `st.session_state.current_selection = 'Alice'`
   │
   ├─ Voter clicks "Begin Crypto Theater"
   │  ├─ `crypto.blind_message('Alice', public_key)` → blinded_msg, factor
   │  ├─ `crypto.sign_blinded_message(blinded_msg, private_key)` → signature
   │  ├─ `crypto.unblind_signature(signature, factor, public_key)` → final_sig
   │  └─ `st.session_state.crypto_complete = True`
   │
   ├─ Voter clicks "Cast Vote"
   │  ├─ `hash_message('Alice')` → vote_hash
   │  ├─ `generate_receipt_code()` → receipt = 'A7F3B2C9D1E8'
   │  ├─ `blockchain.add_vote(vote_hash, final_sig, receipt)` → Block #5
   │  ├─ `increment_vote_count('Alice')` → vote_counts['Alice'] = 3
   │  ├─ `mark_voter_as_voted(voter_id, receipt)`
   │  └─ Display receipt to voter

3. RESULTS PHASE
   └─ Results page queries `st.session_state.vote_counts` → displays metrics

4. VERIFICATION PHASE
   ├─ Voter enters "A7F3B2C9D1E8"
   ├─ `blockchain.find_vote_by_receipt('A7F3B2C9D1E8')` → Block #5
   ├─ `blockchain.is_chain_valid()` → True
   └─ Display "✅ Vote found in Block #5"
```

## Error Handling Strategy

### Graceful Degradation

All errors caught and converted to user-friendly messages:

```python
try:
    # cryptographic operation
except Exception as e:
    st.error(f"❌ {error_explanation}")
    return False  # Stop processing
```

Examples:
- Invalid key → "Invalid key file"
- Already voted → "You have already voted" + show previous receipt
- Blockchain invalid → "Chain integrity check failed"

## Testing Strategy

### Test Suites

**test_voting_system.py** includes:
- Unit tests for crypto functions
- Unit tests for blockchain
- Integration tests for workflows
- Edge case validation

### Test Coverage

```
TestCryptoModule:
  ✓ Key generation
  ✓ Sign/verify
  ✓ Blind/unblind
  ✓ Hashing
  ✓ Truncation

TestBlockchain:
  ✓ Genesis block
  ✓ Add vote
  ✓ Find by receipt
  ✓ Chain validation
  ✓ Vote counting

TestIntegration:
  ✓ Complete voting workflow
  ✓ Multiple votes
```

### Running Tests

```bash
python streamlit_app/test_voting_system.py
```

Expected output: All tests pass ✓

## Deployment Considerations

### Current Setup: Local Only

- No network communication
- Single machine
- Session state in memory
- Data lost on restart/refresh

### For Classroom Demo

Perfect as-is:
- ✅ No WiFi required
- ✅ Offline-friendly
- ✅ Can't have connectivity failures mid-demo
- ✅ Data stays on presenter's laptop

### For Future Production

Would need:
- Persistent database (PostgreSQL, MongoDB)
- Session serialization
- Key management system
- Audit logging
- Real blockchain (Ethereum, etc.)

## Security Properties Verified

| Property | How Achieved | Evidence |
|----------|-------------|----------|
| **Anonymity** | Vote encrypted in blind signature | Can't link voter→choice |
| **Eligibility** | Government signs proving authorization | Only authorized votes signed |
| **Integrity** | Blockchain with hash links | Any change detected |
| **Uniqueness** | Vote tracking prevents double-voting | voted_voters set |
| **Verifiability** | Receipt + blockchain lookup | User can prove vote recorded |

## Performance Characteristics

| Operation | Time | Notes |
|-----------|------|-------|
| RSA key generation (2048) | ~1 second | Streamlit blocking |
| Blind signature | <100ms | Fast |
| Blockchain validation | <10ms | Small blockchain |
| Page load | ~500ms | Streamlit rendering |

## File Organization Rationale

```
streamlit_app/
├── app.py              # Entry point & home page
├── crypto.py           # Pure functions, no state
├── blockchain.py       # Data structures, no state
├── utils.py            # State management helpers
├── test_voting_system.py  # All tests in one file
└── pages/
    ├── 1_setup.py      # Admin operations
    ├── 2_vote.py       # Main UX
    ├── 3_results.py    # Reporting
    └── 4_verify.py     # Audit
```

Rationale:
- Numbered pages control Streamlit sidebar order
- Utilities separated by concern (crypto, blockchain, state)
- Single test file for simplicity
- Clear purpose for each module

## Future Enhancements

Possible improvements without changing architecture:

1. **Confirmation Button** - "Are you sure?" before casting
2. **Candidate Photos** - Visual identification
3. **Vote Revocation** - Allow changing vote before submission
4. **Admin Controls** - Pause election, view running tallies
5. **Advanced Audit** - Block timestamps, cryptographic proofs
6. **Multi-Language** - i18n support
7. **Export Results** - PDF report generation
8. **Tally Board** - Projected vote distributions

All doable without major refactoring.

## Design Philosophy

### Simplicity First
- Clear, single-purpose functions
- Minimal abstractions
- Readable code for grade context

### Presentation-Ready
- Zero crashes
- Graceful error handling
- Informative messages

### Educational Value
- Comments explain crypto
- Config file documents decisions
- Test suite shows usage patterns

---

**Last Updated:** February 2026
**Architecture Version:** 1.0
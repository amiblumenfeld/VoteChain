# Project File Reference

Quick reference guide for all files in the VoteChain project.

## 📂 Project Structure

```
/Users/amichaiblumenfeld/cyber_grade_11/votting/VoteChain/
├── README.md                          ← Project overview
├── ARCHITECTURE.md                    ← Technical architecture
├── STEP1_IMPLEMENTATION.md            ← This step's completion summary
├── requirements.txt                   ← Python dependencies
├── tasks.py                           ← Invoke task definitions
├── build/                             ← Sphinx documentation (generated)
├── source/                            ← Sphinx source files
└── streamlit_app/                     ← Main application directory
    ├── app.py                         ← Home page (entry point)
    ├── crypto.py                      ← Cryptographic utilities (195 lines)
    ├── blockchain.py                  ← Blockchain implementation (180 lines)
    ├── utils.py                       ← State management & helpers (190 lines)
    ├── test_voting_system.py          ← Complete test suite (430+ lines)
    ├── voter_keys/                    ← Generated voter key files (runtime)
    └── pages/
        ├── 1_setup.py                 ← Admin setup page (200+ lines)
        ├── 2_vote.py                  ← Voting interface (280+ lines)
        ├── 3_results.py               ← Results dashboard (150+ lines)
        └── 4_verify.py                ← Verification & audit (200+ lines)
```

## 📄 File Descriptions

### Core Application Files

#### `app.py` (Main Entry Point)
**Purpose:** Home page and application entry point
**Contains:**
- System overview and key concepts
- Two-act experience explanation
- Navigation guide
- System status dashboard
- Technical details (expandable)

**When to Use:** First page users see when starting the app

---

#### `crypto.py` (Cryptographic Utilities)
**Purpose:** All cryptographic operations
**Key Functions:**
- `generate_rsa_keys(key_size=2048)` - Generate RSA key pair
- `sign_message(message, private_key)` - Sign with RSA
- `verify_signature(message, signature_hex, public_key)` - Verify signature
- `blind_message(message, public_key)` - Blind a message
- `sign_blinded_message(blinded_msg, private_key)` - Sign blinded message
- `unblind_signature(signature_hex, factor_hex, public_key)` - Unblind signature
- `hash_message(message)` - SHA256 hash
- `truncate_hash(hash_str, length=12)` - Format hash for display
- `import_key_from_file(filepath)` - Load RSA key from file
- `import_key_from_bytes(key_bytes)` - Load RSA key from bytes
- `export_key_to_file(key, filepath)` - Save RSA key to file

**When to Use:** Whenever cryptographic operations are needed (signing, blinding, hashing)

---

#### `blockchain.py` (Blockchain Implementation)
**Purpose:** Simple blockchain for vote storage and verification
**Classes:**
- `Block` - Single blockchain block
  - `index` - Position in chain
  - `timestamp` - Creation time
  - `vote_hash` - Hash of encrypted vote
  - `previous_hash` - Link to previous block
  - `signature` - Voter's signature
  - `receipt_code` - User-facing receipt

- `Blockchain` - Complete blockchain
  - `create_genesis_block()` - Init with genesis block
  - `add_vote(vote_hash, signature, receipt_code)` - Record vote
  - `is_chain_valid()` - Validate entire chain
  - `find_vote_by_receipt(receipt_code)` - Lookup vote by receipt
  - `validate_receipt(receipt_code)` - Validate receipt with chain integrity check
  - `get_vote_count()` - Total votes cast
  - `export_chain()` - Export as JSON

**When to Use:** Storing votes, validating chain, searching receipts

---

#### `utils.py` (State Management & Helpers)
**Purpose:** Streamlit session state and application utilities
**Key Functions:**
- `initialize_session_state()` - Initialize all session variables
- `generate_receipt_code(length=12)` - Generate random receipt
- `clear_voter_session()` - Clear voter-specific state
- `reset_election()` - Reset entire election
- `get_vote_count(candidate)` - Get votes for candidate
- `increment_vote_count(candidate)` - +1 vote for candidate
- `has_already_voted(voter_id)` - Check if voter already voted
- `mark_voter_as_voted(voter_id, receipt)` - Record that voter voted
- `validate_election_state()` - Check if election is ready
- `format_hash_for_display(hash_str)` - Truncate hash for UI

**When to Use:** Managing state, preventing double-voting, tracking votes

---

### Streamlit Pages

#### `pages/1_setup.py` (Admin Setup)
**Purpose:** Initialize election infrastructure
**User:** Administrator (before presentation)
**Workflow:**
1. Generate government RSA keys
2. Create voter key files (N voters)
3. Configure candidates
4. Initialize election

**Status:** Step indicator showing completion
**Duration:** ~2 minutes for setup

---

#### `pages/2_vote.py` (Main Voting Interface)
**Purpose:** Core voting experience (the "two-act" demo)
**User:** Classmates (voters)
**Workflow:**
1. Upload voter key file
2. Authenticate (voter ID displayed)
3. Select candidate
4. Watch "crypto theater"
   - Blind the vote
   - Government signs it
   - Unblind to get signature
5. Cast vote
6. Display receipt code

**Status:** "Crypto theater" with `st.status()` and 1.5s delays per stage
**Duration:** ~60 seconds per voter

---

#### `pages/3_results.py` (Results Dashboard)
**Purpose:** Display election results in real-time
**User:** All (observers during demo)
**Displays:**
- Vote counts per candidate (with %)
- Vote distribution chart
- Total votes & election status
- Blockchain statistics
- Blockchain explorer (expandable)

**Auto-updates:** As votes are cast
**Duration:** Continuous display

---

#### `pages/4_verify.py` (Verification & Audit)
**Purpose:** Prove vote integrity and find receipts
**User:** Teachers/auditors (Mr. Cohen) and curious voters
**Features:**
- Receipt search (enter code → find vote)
- Chain integrity verification
- Blockchain explorer (blocks with details)
- Export blockchain JSON

**Shows:** Receipt found/not found, block location, chain status
**Duration:** ~3-5 minutes for thorough audit

---

#### `test_voting_system.py` (Test Suite)
**Purpose:** Comprehensive testing of all modules
**Test Classes:**
- `TestCryptoModule` (5 tests) - Crypto operations
- `TestBlockchain` (7 tests) - Blockchain functionality
- `TestUtilities` (4 tests) - Helper functions
- `TestIntegration` (2 tests) - Complete workflows

**Run:** `python test_voting_system.py`
**Results:** 17 passed, 1 skipped

---

### Documentation Files

#### `README.md`
**Purpose:** Project overview and quick start
**Contains:**
- Feature overview
- Quick start instructions
- Page descriptions
- Project structure
- Cryptographic details
- Demo workflow
- Testing guide

**For:** Users getting started with the project

---

#### `ARCHITECTURE.md`
**Purpose:** Technical design and implementation details
**Contains:**
- System architecture diagram
- Component breakdown
- State management design
- Cryptographic protocol explanation
- Blockchain details
- UX/UI rationale
- Data flow diagrams
- Error handling strategy
- Performance metrics

**For:** Developers understanding the system

---

#### `STEP1_IMPLEMENTATION.md`
**Purpose:** Summary of Step 1 completion
**Contains:**
- What was implemented
- File descriptions
- Test results
- Metrics
- Notes for future steps

**For:** Tracking progress and completeness

---

## 🚀 Quick Start

### Installation
```bash
cd /Users/amichaiblumenfeld/cyber_grade_11/votting/VoteChain
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Running
```bash
streamlit run streamlit_app/app.py
```

### Testing
```bash
python streamlit_app/test_voting_system.py
```

---

## 📊 Statistics

| Metric | Count |
|--------|-------|
| Python Files | 9 |
| Total Lines of Code | 1845 |
| Test Cases | 18 |
| Test Pass Rate | 94% (17/18) |
| Streamlit Pages | 4 + 1 home |
| Documentation Files | 3 |

---

## 🔑 Key Files to Modify for Future Steps

1. **crypto.py** - Add new cryptographic operations
2. **blockchain.py** - Enhance blockchain features
3. **pages/2_vote.py** - Refine voting UX
4. **utils.py** - Extend state management
5. **test_voting_system.py** - Add new test cases

---

## 💡 Usage Tips

### For Development
- Start with `crypto.py` for cryptographic updates
- Use `blockchain.py` for vote storage logic
- Modify pages individually for UX changes
- Run tests after every change

### For Presentations
- Open `app.py` first to see overview
- Use `1_setup.py` to prepare election
- Have voters use `2_vote.py`
- Show results on `3_results.py`
- Audit with `4_verify.py` for credibility

### For Debugging
- Check test suite for examples of correct usage
- Use `st.write()` to inspect session state
- Check browser console for JavaScript errors
- Refer to docstrings in each module

---

**Last Updated:** February 27, 2026
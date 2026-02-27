# VoteChain: Secure Voting System Demo

A web-based demonstration of secure voting using blind signatures, RSA cryptography, and blockchain technology. Built with Streamlit for educational presentation.

## 🎯 Overview

VoteChain demonstrates how modern cryptography can ensure both **voter privacy** and **electoral integrity**. The system implements a two-act experience:

1. **Act 1: Crypto Theater** - Watch the blind signature process unfold as your vote is blinded, signed by government, and unblinded
2. **Act 2: Receipt Reveal** - Receive a verification code proving your vote exists without revealing your choice

## ✨ Key Features

- 🔐 **Blind Signatures**: Voters get cryptographic proof of eligibility without revealing their choice
- ⛓️ **Blockchain**: Immutable ledger of votes with tamper detection
- 🗳️ **Anonymous Voting**: Votes are encrypted and cannot be linked to voters
- 🎟️ **Receipt Verification**: Voters can prove their vote was recorded
- 📊 **Real-Time Results**: Live vote counting and blockchain status monitoring
- 🔍 **Blockchain Explorer**: Audit the voting system and verify integrity

## 📋 Pages

### 1. Home (app.py)
- Overview of the voting system
- Key concepts explanation
- System status dashboard

### 2. Setup Page (1_setup.py)
*Admin only*
- Generate government RSA keys
- Create voter key files
- Configure candidates
- Initialize election

### 3. Vote Page (2_vote.py)
*Main voting experience*
- Authenticate with voter key
- Select candidate
- Watch blind signature process (crypto theater)
- Cast vote and receive receipt

### 4. Results Page (3_results.py)
*Live election dashboard*
- Vote counts by candidate
- Blockchain statistics
- Vote distribution visualization
- Chain integrity status

### 5. Verify Page (4_verify.py)
*Audit and verification*
- Search votes by receipt code
- Verify blockchain integrity
- Explore blockchain structure
- Export blockchain data

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Chrome browser (latest)
- ~5 minutes for demo setup

### Installation

1. **Clone and navigate**
   ```bash
   cd VoteChain
   ```

2. **Create virtual environment** (macOS/Linux)
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

```bash
streamlit run streamlit_app/app.py
```

The app opens at `http://localhost:8501`

## 📁 Project Structure

```
streamlit_app/
├── app.py                     # Home page and entry point
├── crypto.py                  # Cryptographic utilities
├── blockchain.py              # Blockchain implementation
├── utils.py                   # Session state and helpers
├── test_voting_system.py      # Test suite
└── pages/
    ├── 1_setup.py             # Election setup page
    ├── 2_vote.py              # Voting page (main experience)
    ├── 3_results.py           # Results dashboard
    └── 4_verify.py            # Verification & audit page
```

## 🔐 Cryptographic Details

**Algorithms Used:**
- RSA-2048 for key generation and signing
- SHA-256 for hashing
- PKCS1 v1.5 padding for signatures
- Blind signature protocol for anonymous voting

**Key Operations:**
1. **Blind**: Hide vote before sending to government
2. **Sign**: Government signs without seeing vote
3. **Unblind**: Make signature valid for your actual vote
4. **Submit**: Add signed vote to blockchain
5. **Verify**: Prove vote exists using receipt code

## 📊 Demo Workflow

### For Presenter (Moshe)
1. Open Setup page
2. Click "Generate Keys" → "Create Voter Keys" → "Set Candidates" → "Initialize Election"
3. Share voter key files with participants

### For Voters (Sarah, David, etc.)
1. Navigate to Vote page
2. Upload voter key file
3. Select candidate
4. Watch crypto theater (blind → sign → unblind)
5. Click "Cast Vote"
6. Save receipt code

### For Auditor (Mr. Cohen)
1. Navigate to Verify page
2. Enter receipt code to verify vote
3. Click "Verify Chain Integrity"
4. Explore blockchain blocks

## 🧪 Testing

Run the test suite:
```bash
python streamlit_app/test_voting_system.py
```

Tests cover:
- Cryptographic operations (key generation, blind signatures)
- Blockchain functionality (block creation, chain validation)
- Application utilities (state management, vote tracking)
- Integration workflows

## 🎓 Educational Value

Students learn:
- **Cryptography**: How RSA signatures work
- **Privacy**: Blind signatures for anonymity
- **Integrity**: Blockchain for tamper detection
- **Trust**: Combining privacy AND auditability
- **Security**: Real-world voting system challenges

## ⚙️ Configuration

### Candidates
Edit the default candidates in Setup page (app suggested: Alice, Bob, Charlie)

### Number of Voters
Configurable in Setup page (default: 5 voters)

### Blockchain
- Genesis block: Always "GENESIS"
- Blocks are immutable once added
- Chain validation detects any tampering

## 📝 Documentation

- **User Guide**: See [source/user_guide.rst](source/user_guide.rst)
- **API Docs**: Check docstrings in `crypto.py`, `blockchain.py`, `utils.py`
- **Test Suite**: See [streamlit_app/test_voting_system.py](streamlit_app/test_voting_system.py)

## 🔍 Technical Stack

- **Streamlit**: Web framework for rapid demos
- **PyCryptodome**: RSA and cryptographic operations
- **Python 3.8+**: Core language
- **Pandas**: Data visualization

## 🚨 Important Notes

- **Educational Only**: For learning/demo purposes
- **Not Production Ready**: Lacks advanced security features
- **Local Only**: No network communication (all in-memory)
- **Session-Based**: Data resets on page refresh/restart

## 💡 UX Design Principles

This app follows clean UX principles:
- ✅ **One action per section**: No multi-step wizards
- ✅ **Instant feedback**: Every action gets immediate response
- ✅ **Zero crashes**: All errors handled gracefully
- ✅ **Clear emoji usage**: Visual scanning for busy demos
- ✅ **Progressive disclosure**: Details hidden in expanders

## 🎬 Demo Tips

- **Timing**: ~30 minutes for full demo
- **Network**: Works offline (important for presentations!)
- **Browser**: Test in Chrome before presentation
- **Key Files**: Generate and test once, then demonstrate to class
- **Reception**: Students love the crypto theater visualization!

## 🐛 Troubleshooting

**App won't start?**
```bash
pip install -r requirements.txt --upgrade
streamlit run streamlit_app/app.py
```

**Can't upload voter keys?**
- Ensure keys are in PEM format
- Keys must be generated by Setup page

**Blockchain invalid?**
- This shouldn't happen in normal operation
- If it does: Reset election on Setup page
- Check test suite for edge cases

## 📚 Further Reading

- IETF RFC 3447: RSA specification
- Blind Signatures: Origin by David Chaum
- Bitcoin & Blockchain: Distributed ledger concepts
- Anonymous Electronic Voting: Research papers

## 🤝 Contributing

For improvements:
1. Run the test suite
2. Document any changes
3. Test with full voting workflow
4. Verify presentation works

## 📄 License

Educational use

## 👨‍🏫 Author

Cyber Grade 11 - VoteChain Project

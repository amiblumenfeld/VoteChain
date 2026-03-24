"""
Secure Voting System - Main Application Entry Point

This Streamlit application provides a secure voting system using:
- Blind signatures for voter privacy
- RSA cryptography for authenticity
- Blockchain for immutability and auditability

Navigate using the sidebar to access:
1. Setup: Admin page to initialize election
2. Vote: Main page for casting votes
3. Results: Real-time election results
4. Verify: Audit and receipt verification
"""

import streamlit as st

from utils import initialize_session_state

# Page configuration
st.set_page_config(
    page_title="Secure Voting System",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
initialize_session_state()

# Main Page
st.title("🗳️ Secure Voting System")
st.write(
    """
    Welcome to the **Secure Voting System** - a production-ready implementation of how modern cryptography 
    can ensure both **voter privacy** and **electoral integrity**.
    """
)

st.divider()

# Two-Act Experience Overview
st.header("The Two-Act Experience")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Act 1: The Crypto Theater 🎭")
    st.write(
        """
        Watch the blind signature process unfold:
        - Your vote gets **blinded** (hidden from view)
        - Government **signs** it (proving you're eligible)
        - Signature gets **unblinded** (becomes valid)
        
        **Result:** You have a valid proof of eligibility without 
        the government ever seeing your choice!
        """
    )

with col2:
    st.subheader("Act 2: The Receipt Reveal 🎉")
    st.write(
        """
        You receive a verification code that proves:
        - Your vote **exists** in the blockchain
        - Your vote is **unchanged** and secure
        - **Only you** have the receipt
        
        **Result:** You can prove your vote counts without 
        revealing who you voted for!
        """
    )

st.divider()

# How to Use
st.header("How to Use This System")

st.markdown("""
1. **Setup Page** (`🔧 Election Setup`)
   - Generate government RSA keys
   - Create voter key files
   - Configure candidates
   - Initialize the election
   
2. **Vote Page** (`🗳️ Cast Your Vote`)
   - Upload your voter key
   - Select a candidate
   - Witness the blind signature process
   - Cast your vote and get a receipt

3. **Results Page** (`📊 Election Results`)
   - View real-time vote counts
   - Monitor blockchain status
   - See vote distribution

4. **Verify Page** (`🔍 Verify Your Vote`)
   - Search for your vote using receipt code
   - Verify blockchain integrity
   - Explore blockchain structure
""")

st.divider()

# Key Concepts
st.header("Key Concepts")

concept_cols = st.columns(3)

with concept_cols[0]:
    st.subheader("🔐 Blind Signatures")
    st.write(
        """
        A cryptographic technique that allows signing a message 
        without seeing its contents. Perfect for proving eligibility 
        without revealing voting choice.
        """
    )

with concept_cols[1]:
    st.subheader("⛓️ Blockchain")
    st.write(
        """
        An immutable ledger of votes where each block cryptographically 
        links to the previous one. Any tampering is immediately detectable.
        """
    )

with concept_cols[2]:
    st.subheader("🎟️ Receipts")
    st.write(
        """
        Unique codes proving votes were recorded and included in the 
        blockchain. Only the voter has their receipt, ensuring privacy.
        """
    )

st.divider()

# Status Panel
st.header("System Status")

status_cols = st.columns(4)

with status_cols[0]:
    keys_status = "✅ Ready" if st.session_state.government_private_key else "⏳ Not Set"
    st.metric("Government Keys", keys_status)

with status_cols[1]:
    candidates_status = f"✅ {len(st.session_state.candidates)}" if st.session_state.candidates else "⏳ Not Set"
    st.metric("Candidates", candidates_status)

with status_cols[2]:
    election_status = "✅ Ready" if st.session_state.election_initialized else "⏳ Setup Needed"
    st.metric("Election", election_status)

with status_cols[3]:
    total_votes = sum(st.session_state.vote_counts.values()) if st.session_state.vote_counts else 0
    st.metric("Votes Cast", total_votes)

st.divider()

# Navigation Guide
st.header("📍 Navigation")

st.info(
    """
    Use the **sidebar menu** on the left to navigate between pages.
    
    **First time?** Start with the **Setup** page to initialize the election.
    """
)

st.divider()

# Technical Details (Expandable)
with st.expander("🔧 Technical Details"):
    st.write("""
    **Technology Stack:**
    - Framework: Streamlit (Python web framework)
    - Cryptography: PyCryptodome (RSA, SHA256)
    - Data Structure: Custom Blockchain implementation
    
    **Cryptographic Algorithms:**
    - RSA-2048 for key generation and signing
    - SHA-256 for hashing
    - PKCS1 v1.5 padding for signatures
    
    **Security Properties:**
    - Blind Signature for voter anonymity
    - Blockchain for immutability
    - Digital signatures for authenticity
    """)

with st.expander("📚 Architecture"):
    st.write("""
    **Project Structure:**
    ```
    streamlit_app/
    ├── app.py              # Main entry point (this file)
    ├── crypto.py           # Cryptographic utilities
    ├── blockchain.py       # Blockchain implementation
    ├── utils.py            # General utilities and state management
    └── pages/
        ├── 1_setup.py      # Election setup
        ├── 2_vote.py       # Voting interface
        ├── 3_results.py    # Results dashboard
        └── 4_verify.py     # Verification and audit
    ```
    
    **Data Flow:**
    1. Setup generates government RSA keys
    2. Voter uses blinded signature to cast anonymous vote
    3. Vote added to blockchain with receipt code
    4. Users can verify receipt and blockchain integrity
    """)

st.divider()

st.success(
    """
    ✅ **Ready to get started?**
    
    Navigate to the **Setup** page from the sidebar menu to begin!
    """
)

"""
Setup page for the Secure Voting System.

This page allows administrators to:
- Generate government RSA keys
- Create voter key files
- Configure candidates
- Initialize the election
"""

import streamlit as st
from Crypto.PublicKey import RSA
import os
from pathlib import Path

from crypto import generate_rsa_keys, export_key_to_file
from utils import initialize_session_state, reset_election, validate_election_state

# Initialize session state
initialize_session_state()

st.title("🔧 Election Setup")
st.write("Initialize the election infrastructure for the secure voting demo.")

st.divider()

# Step 1: Generate Government Keys
st.header("Step 1: Generate Government Keys")
st.write("Create the RSA keypair that will sign all votes to prove voter eligibility.")

if st.button("Generate Keys", key="gen_keys"):
    try:
        private_key, public_key = generate_rsa_keys(key_size=2048)
        st.session_state.government_private_key = private_key
        st.session_state.government_public_key = public_key
        
        st.success("✅ Government keys generated successfully!")
        st.info(f"🔑 Public Key Modulus: {str(public_key.n)[:50]}...")
    except Exception as e:
        st.error(f"❌ Error generating keys: {str(e)}")

if st.session_state.government_private_key is not None:
    st.info("✅ Government keys are ready")
else:
    st.warning("⚠️ Please generate keys first")

st.divider()

# Step 2: Create Voter Key Files
st.header("Step 2: Create Voter Key Files")
st.write("Generate RSA keypairs for each voter. Each voter will use their private key to authenticate.")

num_voters = st.number_input(
    "Number of voters to create:",
    min_value=1,
    max_value=50,
    value=5,
    step=1
)

if st.button("Create Voter Keys", key="create_voters"):
    if st.session_state.government_private_key is None:
        st.error("❌ Please generate government keys first")
    else:
        try:
            # Create voters directory
            voters_dir = Path("voter_keys")
            voters_dir.mkdir(exist_ok=True)
            
            # Clear previous keys
            for file in voters_dir.glob("*.pem"):
                file.unlink()
            
            # Generate voter keys
            voter_files = []
            for i in range(1, int(num_voters) + 1):
                voter_private_key, voter_public_key = generate_rsa_keys()
                filepath = voters_dir / f"voter_{i:02d}_private.pem"
                export_key_to_file(voter_private_key, str(filepath))
                voter_files.append(f"voter_{i:02d}_private.pem")
            
            st.session_state.num_voters = int(num_voters)
            st.success(f"✅ Created {num_voters} voter keys in `voter_keys/` directory")
            st.info("📁 Voter files: " + ", ".join(voter_files[:3]) + "...")
        except Exception as e:
            st.error(f"❌ Error creating voter keys: {str(e)}")

st.divider()

# Step 3: Configure Candidates
st.header("Step 3: Configure Candidates")
st.write("Enter the candidates for this election.")

candidates_input = st.text_area(
    "Enter candidate names (one per line):",
    value="Alice\nBob\nCharlie",
    height=150
)

if st.button("Set Candidates", key="set_candidates"):
    candidates = [c.strip() for c in candidates_input.split('\n') if c.strip()]
    
    if len(candidates) < 2:
        st.error("❌ Please enter at least 2 candidates")
    else:
        st.session_state.candidates = candidates
        st.session_state.vote_counts = {candidate: 0 for candidate in candidates}
        st.success(f"✅ Configured {len(candidates)} candidates")
        for candidate in candidates:
            st.write(f"  • {candidate}")

st.divider()

# Step 4: Initialize Election
st.header("Step 4: Initialize Election")
st.write("Finalize setup and start the election.")

col1, col2 = st.columns(2)

with col1:
    if st.button("Initialize Election", key="init_election"):
        # don't check election_initialized itself, since we're about to set it
        if st.session_state.government_public_key is None:
            st.error("❌ Government keys not generated. Please complete Step 1 first.")
        elif not st.session_state.candidates:
            st.error("❌ No candidates configured. Please complete Step 3 first.")
        else:
            st.session_state.election_initialized = True
            st.success("✅ Election Ready! 🗳️")
            st.info("You can now navigate to the Vote page for participants to cast their votes.")

with col2:
    if st.button("Reset Election", key="reset_election"):
        reset_election()
        st.warning("⚠️ Election has been reset")
        st.rerun()

st.divider()

# Status Display
st.header("Election Status")

status_cols = st.columns(3)

with status_cols[0]:
    keys_status = "✅ Generated" if st.session_state.government_private_key else "⏳ Pending"
    st.metric("Government Keys", keys_status)

with status_cols[1]:
    candidates_status = f"✅ {len(st.session_state.candidates)}" if st.session_state.candidates else "⏳ Pending"
    st.metric("Candidates", candidates_status)

with status_cols[2]:
    election_status = "✅ Ready" if st.session_state.election_initialized else "⏳ Not Ready"
    st.metric("Election Status", election_status)

st.divider()

# Technical Details (Expandable)
with st.expander("📋 Technical Details"):
    st.write("**Session State Variables:**")
    st.code(f"""
government_private_key: {type(st.session_state.government_private_key).__name__}
government_public_key: {type(st.session_state.government_public_key).__name__}
candidates: {st.session_state.candidates}
election_initialized: {st.session_state.election_initialized}
    """)
    
    if st.session_state.government_public_key:
        st.write("**Government Public Key (PEM):**")
        st.code(st.session_state.government_public_key.export_key().decode()[:200] + "...")

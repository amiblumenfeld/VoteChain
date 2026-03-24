"""
Vote page for the Secure Voting System.

This page implements the main voting flow:
1. Authenticate with voter key
2. Select candidate
3. Witness blind signature process (crypto theater)
4. Submit vote and receive receipt
"""

import streamlit as st
import time

from crypto import (
    import_key_from_bytes, sign_message, hash_message, 
    blind_message, sign_blinded_message, unblind_signature
)
from utils import (
    initialize_session_state, validate_election_state, 
    has_already_voted, mark_voter_as_voted, 
    increment_vote_count, generate_receipt_code
)

# Initialize session state
initialize_session_state()

st.title("🗳️ Cast Your Vote")
st.write("Vote securely using blind signatures. Your vote is anonymous and verified.")

st.divider()

# Validate election state first
is_valid, error_msg = validate_election_state()
if not is_valid:
    st.error(f"❌ {error_msg}")
    st.stop()

# Step 1: Authentication
st.header("Step 1: Authenticate")
st.write("Upload your voter key file to authenticate.")

uploaded_file = st.file_uploader(
    "Choose your voter key file (.pem):",
    type=["pem"],
    key="voter_key_upload"
)

if uploaded_file is not None:
    try:
        key_bytes = uploaded_file.read()
        voter_key = import_key_from_bytes(key_bytes)
        
        if voter_key is None:
            st.error("❌ Invalid key file. Please upload a valid RSA private key.")
        else:
            voter_id = f"Voter_{abs(hash(key_bytes)) % 10000:04d}"
            
            # Check if already voted
            if has_already_voted(voter_id):
                previous_receipt = st.session_state.voter_receipts.get(voter_id, '')
                st.warning(f"⚠️ You have already voted in this election")
                if previous_receipt:
                    st.info(f"Your previous receipt code: `{previous_receipt}`")
                st.stop()
            
            st.session_state.authenticated_voter_id = voter_id
            st.session_state.current_voter_key = voter_key
            st.success(f"🔑 Welcome, {voter_id}!")
            
            # Reset voting state if this is a new voter
            if st.session_state.authenticated_voter_id != st.session_state.get('last_voter_id'):
                st.session_state.vote_cast = False
                st.session_state.crypto_complete = False
                st.session_state.current_selection = None
                # Don't reset current_receipt - it should persist for the current voter's session
                st.session_state.email_sent = False
                st.session_state.email_recipient = None
                st.session_state.last_voter_id = st.session_state.authenticated_voter_id
    except Exception as e:
        st.error(f"❌ Error reading key file: {str(e)}")
        st.stop()
else:
    st.info("📝 Please upload your voter key file to proceed")
    st.stop()

st.divider()

# Step 2: Select Candidate
st.header("Step 2: Select Your Candidate")
st.write("Choose who you want to vote for:")

# Create columns for candidate buttons
cols = st.columns(min(3, len(st.session_state.candidates)))
for idx, candidate in enumerate(st.session_state.candidates):
    with cols[idx % len(cols)]:
        if st.button(candidate, key=f"candidate_{candidate}", use_container_width=True):
            st.session_state.current_selection = candidate
            st.success(f"✅ You selected: **{candidate}**")

if st.session_state.current_selection is None:
    st.info("👆 Click a candidate button above to select")
    st.stop()

st.divider()

# Step 3: Crypto Theater - Blind Signature Process
st.header("Step 3: Secure Your Vote")
st.write("Watch as your vote is protected using blind signatures...")

if st.button("🔐 Begin Crypto Theater", key="start_crypto"):
    # The Crypto Theater Experience
    with st.status("🔐 Securing your vote...", expanded=True) as status:
        time.sleep(0.5)
        
        # Stage 1: Blinding
        st.write("🔒 **Blinding your vote...**")
        st.write(f"Your choice: `{st.session_state.current_selection}`")
        
        try:
            blinded_msg, blinding_factor = blind_message(
                st.session_state.current_selection,
                st.session_state.government_public_key
            )
            st.write(f"_Blinded value: {blinded_msg[:20]}..._")
            st.caption("✅ Your choice is now hidden from the government")
            time.sleep(1.5)
            
            # Stage 2: Government Signing
            st.write("✍️ **Government signing...**")
            st.write("_(Proving you're an eligible voter)_")
            signature = sign_blinded_message(blinded_msg, st.session_state.government_private_key)
            st.write(f"_Signature: {signature[:20]}..._")
            st.caption("✅ Government has signed without seeing your vote")
            time.sleep(1.5)
            
            # Stage 3: Unblinding
            st.write("🔓 **Unblinding signature...**")
            st.write("_(Making signature valid for your actual vote)_")
            final_signature = unblind_signature(signature, blinding_factor, st.session_state.government_public_key)
            st.write(f"_Final signature: {final_signature[:20]}..._")
            st.caption("✅ You now have a valid, anonymous vote")
            time.sleep(1)
            
            # Store for next step
            st.session_state.crypto_complete = True
            st.session_state.final_signature = final_signature
            
            status.update(label="✅ Vote secured!", state="complete")
            
        except Exception as e:
            st.error(f"❌ Crypto error: {str(e)}")
            status.update(label="❌ Error securing vote", state="error")
            st.session_state.crypto_complete = False

if not st.session_state.get('crypto_complete', False):
    st.info("👆 Click 'Begin Crypto Theater' above to secure your vote")
    st.stop()

# Redirect already-completed vote to receipt page (Step 5/6)
if st.session_state.get('vote_cast', False):
    st.switch_page("5_receipt")

st.divider()

# Step 4: Submit Vote
st.header("Step 4: Submit Your Vote")
st.write("Ready to cast your vote? Click below to add it to the blockchain.")

# Check if vote has already been cast
vote_cast = st.session_state.get('vote_cast', False)

if not vote_cast:
    if st.button("🗳️ Cast Vote", key="cast_vote"):
        try:
            # Generate receipt code
            receipt_code = generate_receipt_code()
            
            # Add to blockchain
            vote_hash = hash_message(st.session_state.current_selection)
            block = st.session_state.blockchain.add_vote(
                vote_hash=vote_hash,
                signature=st.session_state.final_signature,
                receipt_code=receipt_code
            )
            
            # Update vote counts
            increment_vote_count(st.session_state.current_selection)
            
            # Mark voter as voted
            mark_voter_as_voted(st.session_state.authenticated_voter_id, receipt_code)
            
            # Store receipt for next page
            st.session_state.current_receipt = receipt_code
            st.session_state.vote_cast = True
            
            st.success("🎉 Your vote has been cast successfully!")
            st.balloons()
            
            # Redirect to receipt page for Step 5 and 6
            st.switch_page("5_receipt")
        except Exception as e:
            st.error(f"❌ Error casting vote: {str(e)}")
else:
    st.success("🎉 Your vote has been cast successfully!")
    st.balloons()
    st.switch_page("5_receipt")

st.divider()

# Help Section
with st.expander("❓ How does this work?"):
    st.write("""
    **Blind Signature Protocol:**
    1. You select your candidate
    2. Your vote is "blinded" (hidden) before sending to government
    3. Government signs the blinded vote (proving you're eligible)
    4. You "unblind" the signature to make it valid
    5. Your vote goes to blockchain - signed but secret from everyone
    
    **Why this matters:**
    - 🔐 Government can't see how you voted
    - 🔓 But they verified you're eligible
    - 🗳️ Vote is cryptographically tied to you (can't vote twice)
    - ✅ You can prove it exists without revealing your choice
    """)

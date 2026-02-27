"""
Verify page for the Secure Voting System.

This page allows users to:
- Search for their vote using receipt code
- Verify blockchain integrity
- Explore blockchain structure
"""

import streamlit as st

from utils import initialize_session_state, validate_election_state, format_hash_for_display

# Initialize session state
initialize_session_state()

st.title("🔍 Verify Your Vote")
st.write("Search for your vote using your receipt code and verify blockchain integrity.")

st.divider()

# Validate election state
is_valid, error_msg = validate_election_state()
if not is_valid:
    st.error(f"❌ {error_msg}")
    st.info("Please complete the Setup page first")
    st.stop()

# Section 1: Receipt Search
st.header("Search for Your Receipt")
st.write("Enter your receipt code to verify your vote exists in the blockchain:")

col1, col2 = st.columns([4, 1])

with col1:
    receipt_input = st.text_input(
        "Receipt Code:",
        placeholder="e.g., A7F3B2C9D1E8",
        key="receipt_search"
    )

with col2:
    search_clicked = st.button("🔍 Search", key="search_receipt")

if search_clicked and receipt_input:
    result = st.session_state.blockchain.validate_receipt(receipt_input.strip().upper())
    
    if result['valid']:
        st.success(f"✅ Vote found in Block #{result['block_index']}")
        
        block = result['block']
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Block Index", block['index'])
        with col2:
            st.metric("Timestamp", block['timestamp'][:19])
        with col3:
            st.metric("Status", "✅ Valid")
        
        with st.expander("📋 Block Details"):
            st.json(block)
    else:
        st.error(f"❌ {result['message']}")
        st.info("Please check your receipt code and try again")

st.divider()

# Section 2: Blockchain Verification
st.header("Blockchain Integrity Check")
st.write("Verify that the entire blockchain is valid and hasn't been tampered with:")

if st.button("✅ Verify Chain Integrity", key="verify_chain"):
    is_valid = st.session_state.blockchain.is_chain_valid()
    
    if is_valid:
        st.success("✅ All blocks are valid and properly linked!")
        st.info(
            f"Total blocks: {len(st.session_state.blockchain.chain)}\n\n"
            f"Each block's hash correctly links to the previous block. "
            f"The chain has not been tampered with."
        )
    else:
        st.error("❌ Blockchain integrity check failed!")
        st.warning(
            "One or more blocks have been modified or corrupted. "
            "The chain is no longer valid."
        )

st.divider()

# Section 3: Blockchain Explorer
st.header("📦 Blockchain Explorer")
st.write("Browse the blockchain structure and view block details:")

blockchain_data = st.session_state.blockchain.get_chain_as_dict()

for block in blockchain_data:
    with st.expander(f"Block #{block['index']} - {block['receipt_code'][:12]}..."):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Block Information**")
            st.write(f"- Index: {block['index']}")
            st.write(f"- Timestamp: {block['timestamp']}")
            st.write(f"- Receipt: `{block['receipt_code']}`")
        
        with col2:
            st.write("**Hash Information**")
            vote_hash_display = format_hash_for_display(block['vote_hash'])
            st.write(f"- Vote Hash: `{vote_hash_display}`")
            prev_hash_display = format_hash_for_display(block['previous_hash'])
            st.write(f"- Previous Hash: `{prev_hash_display}`")
        
        if block['signature']:
            with st.expander("🔐 Signature"):
                sig_display = format_hash_for_display(block['signature'], 16)
                st.code(sig_display)

st.divider()

# Section 4: Statistics
st.header("📊 Blockchain Statistics")

total_votes = len(st.session_state.blockchain.get_all_votes())
total_blocks = len(st.session_state.blockchain.chain)

stat_cols = st.columns(4)

with stat_cols[0]:
    st.metric("Total Blocks", total_blocks)

with stat_cols[1]:
    st.metric("Votes Cast", total_votes)

with stat_cols[2]:
    valid_status = "✅ Valid" if st.session_state.blockchain.is_chain_valid() else "❌ Invalid"
    st.metric("Chain Status", valid_status)

with stat_cols[3]:
    genesis_block = st.session_state.blockchain.chain[0]
    st.metric("Genesis Block", genesis_block.receipt_code)

st.divider()

# Section 5: Export Blockchain
with st.expander("💾 Export Blockchain Data"):
    st.write("Download the complete blockchain as JSON:")
    
    blockchain_json = st.session_state.blockchain.export_chain()
    
    st.download_button(
        label="⬇️ Download Blockchain JSON",
        data=blockchain_json,
        file_name="blockchain.json",
        mime="application/json"
    )
    
    st.code(blockchain_json[:500] + "...", language="json")

st.divider()

# Help Section
with st.expander("❓ How Verification Works"):
    st.write("""
    **Receipt Search:**
    - Each vote receives a unique receipt code when cast
    - Use your receipt code to prove your vote was recorded
    - The receipt links to a block in the blockchain
    - ℹ️ Note: Your actual vote contents remain hidden (encrypted)
    
    **Blockchain Integrity:**
    - Each block contains a hash of the previous block
    - If any block is modified, the chain becomes invalid
    - All blocks must validate correctly for the chain to be "valid"
    
    **Why Receipt + Blockchain?**
    - 🎟️ Receipt proves YOUR vote exists (only you have it)
    - ⛓️ Blockchain proves the system didn't alter votes
    - 🔐 Together they show: "My vote was recorded and unchanged"
    """)

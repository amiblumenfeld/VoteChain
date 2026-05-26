"""
Results page for the Secure Voting System.

This page displays:
- Real-time vote tallies per candidate
- Total votes cast
- Live election status
"""

import streamlit as st

from utils import initialize_session_state, validate_election_state, get_all_vote_counts, get_total_votes

# Initialize session state
initialize_session_state()

st.title("📊 Election Results")
st.write("Real-time vote counts and election status")

st.divider()

# Validate election state
is_valid, error_msg = validate_election_state()
if not is_valid:
    st.error(f"❌ {error_msg}")
    st.info("Please complete the Setup page first")
    st.stop()

# Get current vote counts
vote_counts = get_all_vote_counts()
total_votes = get_total_votes()

# Display Vote Counts
st.header("Vote Counts")

if total_votes == 0:
    st.info("No votes cast yet. Participants can vote on the Vote page.")
else:
    # Create metric cards for each candidate
    metric_cols = st.columns(min(3, len(st.session_state.candidates)))
    
    for idx, candidate in enumerate(st.session_state.candidates):
        with metric_cols[idx % len(metric_cols)]:
            votes = vote_counts.get(candidate, 0)
            percentage = (votes / total_votes * 100) if total_votes > 0 else 0
            st.metric(
                candidate,
                votes,
                f"{percentage:.1f}%"
            )

st.divider()

# Summary Statistics
st.header("Election Summary")

summary_cols = st.columns(3)

with summary_cols[0]:
    st.metric("Total Votes Cast", total_votes)

with summary_cols[1]:
    st.metric("Candidates", len(st.session_state.candidates))

with summary_cols[2]:
    blockchain_blocks = len(st.session_state.blockchain.chain)
    st.metric("Blockchain Blocks", blockchain_blocks)

st.divider()

# Candidate Visualization
st.header("Vote Distribution")

if total_votes > 0:
    # Create bar chart data
    import pandas as pd
    
    chart_data = pd.DataFrame({
        'Candidate': st.session_state.candidates,
        'Votes': [vote_counts.get(c, 0) for c in st.session_state.candidates]
    })
    
    st.bar_chart(chart_data.set_index('Candidate'))
else:
    st.info("No data to display yet")

st.divider()

# Election Status
st.header("Election Status")

status_cols = st.columns(4)

with status_cols[0]:
    st.metric("Election Status", "🗳️ Active" if st.session_state.election_initialized else "⏳ Not Started")

with status_cols[1]:
    st.metric("Voters Participated", total_votes)

with status_cols[2]:
    blockchain_valid = "✅ Valid" if st.session_state.blockchain.is_chain_valid() else "❌ Invalid"
    st.metric("Blockchain", blockchain_valid)

with status_cols[3]:
    eligible_voters = getattr(st.session_state, 'num_voters', 0)
    if eligible_voters > 0:
        participation = f"{total_votes}/{eligible_voters}"
        st.metric("Participation", participation)

st.divider()

# Auto-Refresh Notice
st.info("💡 This page auto-updates as votes are cast. Visit the Vote page for participants to begin voting.")

st.divider()

# Technical Details
with st.expander("🔍 Blockchain Details"):
    st.write(f"**Blockchain Status:**")
    st.write(f"- Total blocks: {len(st.session_state.blockchain.chain)}")
    st.write(f"- Blocks are valid: {'✅ Yes' if st.session_state.blockchain.is_chain_valid() else '❌ No'}")
    st.write(f"- Genesis block: {st.session_state.blockchain.chain[0].receipt_code}")
    
    if st.button("🔍 View Full Blockchain"):
        st.json(st.session_state.blockchain.get_chain_as_dict())

with st.expander("📋 Detailed Vote Breakdown"):
    st.write("**Votes by candidate:**")
    for candidate in st.session_state.candidates:
        votes = vote_counts.get(candidate, 0)
        percentage = (votes / total_votes * 100) if total_votes > 0 else 0
        bar = "█" * int(percentage / 5) + "░" * (20 - int(percentage / 5))
        st.write(f"{candidate:<15} {votes:>3} votes ({percentage:>5.1f}%) {bar}")

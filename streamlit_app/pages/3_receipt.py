"""
Receipt and Email Certificate page for Secure Voting System.

After vote is cast on the Vote page (Step 4), user is routed here to see Step 5 and 6.
"""

import streamlit as st
from utils import send_voting_certificate

st.title("🧾 Step 5 & 6: Receipt + Email Certificate")

if not st.session_state.get('vote_cast', False):
    st.error("❌ No vote found. Please cast your vote first.")
    if st.button("← Back to Vote"):
        st.switch_page("2_vote")
    st.stop()

receipt_code = st.session_state.get('current_receipt', '')
if not receipt_code:
    st.error("❌ Receipt code missing. Please go back to vote.")
    if st.button("← Back to Vote"):
        st.switch_page("2_vote")
    st.stop()

# Step 5 - receipt
st.header("Step 5: Your Receipt")
st.write("**Save this code to verify your vote later:**")
st.code(receipt_code, language=None)

st.info(
    "✅ Your vote is now in the blockchain. "
    "Use this receipt on the Verify page to prove your vote exists without revealing your choice."
)

st.caption(f"📋 Receipt Code: `{receipt_code}` (Save this!)")

st.divider()

# Step 6 - optional email certificate
st.header("Step 6: Email Certificate")
st.write("Enter your email address to receive an official certificate confirming your vote.")

if st.session_state.get('email_sent', False):
    recipient = st.session_state.get('email_recipient', 'unknown')
    st.success(f"✅ Certificate already sent to {recipient}", icon="✅")

cert_email = st.text_input("Email address:", placeholder="your.email@example.com", key="cert_email")

col1, col2 = st.columns(2)
with col1:
    send_btn = st.button("📧 Send Certificate")
with col2:
    skip_btn = st.button("⏭️ Skip Email")

if send_btn:
    if not cert_email:
        st.error("❌ Please enter an email address")
    else:
        result = send_voting_certificate(
            cert_email,
            st.session_state.authenticated_voter_id,
            receipt_code,
            st.session_state.current_selection,
        )
        if result:
            st.success(f"✅ Certificate sent to: {cert_email}", icon="✅")
            st.success("🎉 Your voting certificate has been emailed successfully!", icon="✅")
            st.balloons()
            st.session_state.email_sent = True
            st.session_state.email_recipient = cert_email
        else:
            st.error("❌ Failed to send certificate - check terminal logs.")

if skip_btn:
    st.success("✅ Done! Your vote is recorded.", icon="✅")

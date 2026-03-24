"""
General utility functions for the Secure Voting System.

This module provides helper functions for session management, receipts,
and other common operations.
"""

import streamlit as st
import string
import random
from datetime import datetime
from typing import Dict, Any, List


def initialize_session_state() -> None:
    """
    Initialize all session state variables for the voting app.
    
    This function sets up default values for:
    - Government key pair
    - Voter authentication state
    - Election configuration
    - Blockchain instance
    - Vote tracking
    """
    
    # Government keys (Setup page)
    if 'government_private_key' not in st.session_state:
        st.session_state.government_private_key = None
    if 'government_public_key' not in st.session_state:
        st.session_state.government_public_key = None
    
    # Voter authentication state
    if 'authenticated_voter_id' not in st.session_state:
        st.session_state.authenticated_voter_id = None
    if 'current_voter_key' not in st.session_state:
        st.session_state.current_voter_key = None
    
    # Election configuration
    if 'candidates' not in st.session_state:
        st.session_state.candidates = []
    if 'election_initialized' not in st.session_state:
        st.session_state.election_initialized = False
    
    # Blockchain
    if 'blockchain' not in st.session_state:
        from blockchain import Blockchain
        st.session_state.blockchain = Blockchain()
    
    # Vote tracking
    if 'voted_voters' not in st.session_state:
        st.session_state.voted_voters = set()
    if 'voter_receipts' not in st.session_state:
        st.session_state.voter_receipts = {}  # {voter_id: receipt_code}
    
    # Vote counts by candidate
    if 'vote_counts' not in st.session_state:
        st.session_state.vote_counts = {}
    
    # Current voting session
    if 'current_selection' not in st.session_state:
        st.session_state.current_selection = None
    if 'current_receipt' not in st.session_state:
        st.session_state.current_receipt = None
    
    # Voting progress states
    if 'vote_cast' not in st.session_state:
        st.session_state.vote_cast = False
    if 'crypto_complete' not in st.session_state:
        st.session_state.crypto_complete = False
    if 'last_voter_id' not in st.session_state:
        st.session_state.last_voter_id = None
    
    # Email functionality (optional)
    if 'sent_certificates' not in st.session_state:
        st.session_state.sent_certificates = []  # List of sent certificates
    if 'email_sent' not in st.session_state:
        st.session_state.email_sent = False
    if 'email_recipient' not in st.session_state:
        st.session_state.email_recipient = None


def generate_receipt_code(length: int = 12) -> str:
    """
    Generate a random receipt code for vote verification.
    
    Args:
        length: Length of receipt code
        
    Returns:
        Random receipt code (alphanumeric)
    """
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def clear_voter_session() -> None:
    """Clear voter-specific session state after vote is cast."""
    st.session_state.current_selection = None
    st.session_state.current_receipt = None
    st.session_state.authenticated_voter_id = None
    st.session_state.current_voter_key = None


def reset_election() -> None:
    """Reset entire election state (admin only)."""
    st.session_state.government_private_key = None
    st.session_state.government_public_key = None
    st.session_state.candidates = []
    st.session_state.election_initialized = False
    
    from blockchain import Blockchain
    st.session_state.blockchain = Blockchain()
    st.session_state.voted_voters = set()
    st.session_state.voter_receipts = {}
    st.session_state.vote_counts = {}
    
    # Reset email-related state
    st.session_state.sent_certificates = []
    
    clear_voter_session()


def get_vote_count(candidate: str) -> int:
    """
    Get vote count for a specific candidate.
    
    Args:
        candidate: Candidate name
        
    Returns:
        Vote count for the candidate
    """
    return st.session_state.vote_counts.get(candidate, 0)


def get_all_vote_counts() -> Dict[str, int]:
    """
    Get vote counts for all candidates.
    
    Returns:
        Dictionary mapping candidate name to vote count
    """
    return st.session_state.vote_counts.copy()


def increment_vote_count(candidate: str) -> None:
    """
    Increment vote count for a candidate.
    
    Args:
        candidate: Candidate name
    """
    if candidate not in st.session_state.vote_counts:
        st.session_state.vote_counts[candidate] = 0
    st.session_state.vote_counts[candidate] += 1


def has_already_voted(voter_id: str) -> bool:
    """
    Check if a voter has already cast a vote.
    
    Args:
        voter_id: Voter identifier
        
    Returns:
        True if voter has voted, False otherwise
    """
    return voter_id in st.session_state.voted_voters


def mark_voter_as_voted(voter_id: str, receipt_code: str) -> None:
    """
    Mark a voter as having cast their vote.
    
    Args:
        voter_id: Voter identifier
        receipt_code: Receipt code for the vote
    """
    st.session_state.voted_voters.add(voter_id)
    st.session_state.voter_receipts[voter_id] = receipt_code


def get_receipt_for_voter(voter_id: str) -> str:
    """
    Get receipt code for a voter.
    
    Args:
        voter_id: Voter identifier
        
    Returns:
        Receipt code if available, empty string otherwise
    """
    return st.session_state.voter_receipts.get(voter_id, '')


def validate_election_state() -> tuple[bool, str]:
    """
    Validate that election is properly initialized.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not st.session_state.election_initialized:
        return False, "Election not initialized. Please run Setup first."
    
    if st.session_state.government_public_key is None:
        return False, "Government keys not generated. Please run Setup first."
    
    if not st.session_state.candidates:
        return False, "No candidates configured. Please run Setup first."
    
    return True, ""


def format_hash_for_display(hash_str: str, preview_length: int = 8) -> str:
    """
    Format hash for display (truncated with ellipsis).
    
    Args:
        hash_str: Full hash string
        preview_length: Number of chars to show from each end
        
    Returns:
        Formatted hash (e.g., "a7f3b2...c9d1")
    """
    if len(hash_str) <= preview_length * 2:
        return hash_str
    return f"{hash_str[:preview_length]}...{hash_str[-preview_length:]}"


def get_total_votes() -> int:
    """
    Get total number of votes cast.
    
    Returns:
        Total vote count
    """
    return sum(st.session_state.vote_counts.values())


# Email functionality for optional certificate delivery
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional


def send_voting_certificate(email: str, voter_id: str, receipt_code: str, candidate: str) -> bool:
    """
    Send a voting certificate via email.

    Args:
        email: Recipient email address
        voter_id: Voter identifier
        receipt_code: Receipt code for verification
        candidate: Candidate voted for

    Returns:
        True if email sent successfully, False otherwise
    """
    print(f"\n{'='*60}")
    print(f"📧 STARTING EMAIL SEND PROCESS")
    print(f"{'='*60}")
    print(f"To: {email}")
    print(f"Voter ID: {voter_id}")
    print(f"Receipt Code: {receipt_code}")
    print(f"Candidate: {candidate}")
    print(f"{'='*60}\n")
    
    try:
        # Hardcoded Gmail configuration
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        sender_email = 'very.secure.voting.system@gmail.com'
        sender_password = 'eqxrausisfwyzxpo'
        
        print(f"Step 1: Connecting to {smtp_server}:{smtp_port}...")

        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = 'Your Secure Voting Certificate'

        print(f"Step 2: Creating message...")
        
        # Certificate content
        certificate_text = f"""
SECURE VOTING SYSTEM - OFFICIAL CERTIFICATE
==========================================

Voter ID: {voter_id}
Date/Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

CERTIFICATE OF VOTING
---------------------

This certifies that you have successfully cast your vote in the election.

Your Vote Receipt Code: {receipt_code}

IMPORTANT SECURITY NOTICE:
- This certificate proves you voted, but does not reveal your choice
- Keep your receipt code secure for vote verification
- Your vote remains anonymous and cannot be linked to your identity

To verify your vote:
1. Visit the Verify page
2. Enter your receipt code: {receipt_code}
3. Confirm your vote exists in the blockchain

Thank you for participating in secure democratic voting!

Election Authority
Secure Voting System
"""
        msg.attach(MIMEText(certificate_text, 'plain'))

        print(f"Step 3: Attaching email content...")

        # Send email
        print(f"Step 4: Connecting to SMTP server...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        
        print(f"Step 5: Starting TLS...")
        server.starttls()
        
        print(f"Step 6: Logging in as {sender_email}...")
        server.login(sender_email, sender_password)
        
        print(f"Step 7: Converting message to string...")
        text = msg.as_string()
        
        print(f"Step 8: Sending email...")
        server.sendmail(sender_email, email, text)
        
        print(f"Step 9: Closing connection...")
        server.quit()

        print(f"\n✅ SUCCESS! Certificate sent to {email}\n")
        print(f"{'='*60}\n")
        return True

    except smtplib.SMTPAuthenticationError as e:
        print(f"\n❌ AUTHENTICATION ERROR: {e}")
        print(f"Check your Gmail password/app password")
        print(f"{'='*60}\n")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        print(f"{'='*60}\n")
        return False


def test_email_configuration() -> bool:
    """
    Test email configuration by sending a test email.

    Returns:
        True if test email sent successfully, False otherwise
    """
    try:
        # Hardcoded Gmail configuration
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        sender_email = 'very.secure.voting.system@gmail.com'
        sender_password = 'eqxrausisfwyzxpo'

        # Create test message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = sender_email  # Send to self for testing
        msg['Subject'] = 'Secure Voting System - Email Test'

        msg.attach(MIMEText('This is a test email from the Secure Voting System.', 'plain'))

        # Send test email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, sender_email, text)
        server.quit()

        return True

    except Exception as e:
        print(f"❌ Email test failed: {e}")
        return False

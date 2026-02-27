"""
General utility functions for the Secure Voting System.

This module provides helper functions for session management, receipts,
and other common operations.
"""

import streamlit as st
import string
import random
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

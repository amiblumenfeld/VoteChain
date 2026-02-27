"""
Unit tests for the Secure Voting System.

This test suite validates:
- Cryptographic utilities (key generation, blind signatures, etc.)
- Blockchain implementation (block creation, chain validation, etc.)
- Application utilities (session state, vote tracking, etc.)
"""

import unittest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from crypto import (
    generate_rsa_keys, sign_message, verify_signature, 
    blind_message, unblind_signature, sign_blinded_message,
    hash_message, truncate_hash
)
from blockchain import Blockchain, Block
from utils import (
    generate_receipt_code, get_vote_count, increment_vote_count,
    has_already_voted, mark_voter_as_voted, format_hash_for_display,
    initialize_session_state, validate_election_state
)


class TestCryptoModule(unittest.TestCase):
    """Test cryptographic utilities."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.private_key, self.public_key = generate_rsa_keys(key_size=1024)  # Smaller for speed
        self.test_message = "Test vote message"
    
    def test_key_generation(self):
        """Test RSA key pair generation."""
        private, public = generate_rsa_keys()
        self.assertIsNotNone(private)
        self.assertIsNotNone(public)
        self.assertTrue(private.has_private())
        self.assertFalse(public.has_private())
    
    def test_sign_and_verify(self):
        """Test message signing and verification."""
        signature = sign_message(self.test_message, self.private_key)
        self.assertIsNotNone(signature)
        
        # Verify with correct key
        is_valid = verify_signature(self.test_message, signature, self.public_key)
        self.assertTrue(is_valid)
        
        # Verify with wrong message
        is_invalid = verify_signature("Different message", signature, self.public_key)
        self.assertFalse(is_invalid)
    
    def test_blind_and_unblind(self):
        """Test blind signature protocol."""
        # Blind the message
        blinded_msg, blinding_factor = blind_message(self.test_message, self.public_key)
        self.assertIsNotNone(blinded_msg)
        self.assertIsNotNone(blinding_factor)
        
        # Sign the blinded message
        signature = sign_blinded_message(blinded_msg, self.private_key)
        self.assertIsNotNone(signature)
        
        # Unblind the signature
        unblinded = unblind_signature(signature, blinding_factor, self.public_key)
        self.assertIsNotNone(unblinded)
        self.assertNotEqual(unblinded, signature)
    
    def test_hash_message(self):
        """Test message hashing."""
        hash1 = hash_message(self.test_message)
        hash2 = hash_message(self.test_message)
        
        # Same message produces same hash
        self.assertEqual(hash1, hash2)
        
        # Different message produces different hash
        hash3 = hash_message("Different message")
        self.assertNotEqual(hash1, hash3)
    
    def test_truncate_hash(self):
        """Test hash truncation for display."""
        hash_str = "a" * 64
        truncated = truncate_hash(hash_str, length=12)
        
        self.assertIn("...", truncated)
        self.assertEqual(len(truncated), 15)  # 6 + "..." + 6


class TestBlockchain(unittest.TestCase):
    """Test blockchain implementation."""
    
    def setUp(self):
        """Set up test blockchain."""
        self.blockchain = Blockchain()
    
    def test_genesis_block_creation(self):
        """Test that genesis block is created on initialization."""
        self.assertEqual(len(self.blockchain.chain), 1)
        genesis = self.blockchain.chain[0]
        self.assertEqual(genesis.index, 0)
        self.assertEqual(genesis.receipt_code, "GENESIS")
    
    def test_add_vote(self):
        """Test adding a vote to blockchain."""
        initial_length = len(self.blockchain.chain)
        
        vote_hash = hash_message("Alice")
        signature = "test_signature_123"
        receipt = "ABC123DEF456"
        
        block = self.blockchain.add_vote(vote_hash, signature, receipt)
        
        self.assertEqual(len(self.blockchain.chain), initial_length + 1)
        self.assertEqual(block.receipt_code, receipt)
        self.assertEqual(block.vote_hash, vote_hash)
    
    def test_find_vote_by_receipt(self):
        """Test finding a vote by receipt code."""
        receipt = "TEST_RECEIPT_001"
        self.blockchain.add_vote("hash1", "sig1", receipt)
        
        found_block = self.blockchain.find_vote_by_receipt(receipt)
        self.assertIsNotNone(found_block)
        self.assertEqual(found_block.receipt_code, receipt)
        
        # Non-existent receipt
        not_found = self.blockchain.find_vote_by_receipt("NONEXISTENT")
        self.assertIsNone(not_found)
    
    def test_chain_validation(self):
        """Test blockchain validation."""
        # Fresh blockchain should be valid
        self.assertTrue(self.blockchain.is_chain_valid())
        
        # Add votes and validate
        self.blockchain.add_vote("hash1", "sig1", "RECEIPT1")
        self.blockchain.add_vote("hash2", "sig2", "RECEIPT2")
        self.assertTrue(self.blockchain.is_chain_valid())
    
    def test_get_vote_count(self):
        """Test getting total vote count."""
        self.assertEqual(self.blockchain.get_vote_count(), 0)
        
        self.blockchain.add_vote("hash1", "sig1", "RECEIPT1")
        self.assertEqual(self.blockchain.get_vote_count(), 1)
        
        self.blockchain.add_vote("hash2", "sig2", "RECEIPT2")
        self.assertEqual(self.blockchain.get_vote_count(), 2)
    
    def test_validate_receipt(self):
        """Test receipt validation."""
        receipt = "VALID_RECEIPT"
        self.blockchain.add_vote("hash1", "sig1", receipt)
        
        result = self.blockchain.validate_receipt(receipt)
        self.assertTrue(result['valid'])
        self.assertEqual(result['block_index'], 1)
        
        # Invalid receipt
        result = self.blockchain.validate_receipt("INVALID")
        self.assertFalse(result['valid'])
    
    def test_blockchain_reset(self):
        """Test blockchain reset."""
        self.blockchain.add_vote("hash1", "sig1", "RECEIPT1")
        self.assertEqual(len(self.blockchain.chain), 2)
        
        self.blockchain.reset()
        self.assertEqual(len(self.blockchain.chain), 1)
        self.assertEqual(self.blockchain.chain[0].receipt_code, "GENESIS")


class TestUtilities(unittest.TestCase):
    """Test application utilities."""
    
    def test_receipt_code_generation(self):
        """Test receipt code generation."""
        receipt1 = generate_receipt_code()
        receipt2 = generate_receipt_code()
        
        self.assertEqual(len(receipt1), 12)
        self.assertEqual(len(receipt2), 12)
        self.assertNotEqual(receipt1, receipt2)
        self.assertTrue(receipt1.isalnum())
    
    def test_vote_count_operations(self):
        """Test vote count tracking (skipped in non-Streamlit context)."""
        # Note: Session state functions require Streamlit runtime context
        # This test is more of an integration test that runs within Streamlit
        # Skip in unit test context
        self.skipTest("Session state requires Streamlit runtime context")
    
    def test_hash_formatting(self):
        """Test hash formatting for display."""
        long_hash = "a" * 64
        formatted = format_hash_for_display(long_hash, preview_length=8)
        
        self.assertIn("...", formatted)
        self.assertTrue(formatted.startswith("a"))
        self.assertTrue(formatted.endswith("a"))

    def test_validate_election_state(self):
        """Validate election state helper works as expected."""
        from utils import validate_election_state
        # simulate session state manually
        import streamlit as st
        
        # reset session
        initialize_session_state()
        
        # initially not initialized
        valid, msg = validate_election_state()
        self.assertFalse(valid)
        self.assertIn("Election not initialized", msg)

        # set keys only
        st.session_state.government_public_key = object()
        valid, msg = validate_election_state()
        self.assertFalse(valid)
        self.assertIn("Election not initialized", msg)

        # set candidates but still not initialized
        st.session_state.candidates = ["Alice", "Bob"]
        valid, msg = validate_election_state()
        self.assertFalse(valid)
        self.assertIn("Election not initialized", msg)

        # mark initialized and verify passes
        st.session_state.election_initialized = True
        valid, msg = validate_election_state()
        self.assertTrue(valid)
        self.assertEqual(msg, "")

    def test_build_tools_available(self):
        """Ensure build tools (invoke, sphinx) remain importable and functional."""
        # import via python modules rather than relying on shell PATH
        try:
            import invoke
        except ImportError:
            self.fail("invoke module is not installed")
        try:
            import sphinx
        except ImportError:
            self.fail("sphinx module is not installed")
        # check basic attributes / versions
        self.assertTrue(hasattr(invoke, '__version__'))
        self.assertTrue(hasattr(sphinx, '__version__'))
        # version strings should be non-empty
        self.assertTrue(len(invoke.__version__) > 0)
        self.assertTrue(len(sphinx.__version__) > 0)
    
    def test_truncate_hash_short(self):
        """Test truncating a short hash (no ellipsis needed)."""
        short_hash = "abcd1234"
        truncated = truncate_hash(short_hash, length=20)
        
        self.assertEqual(truncated, short_hash)


class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflows."""
    
    def test_voting_workflow(self):
        """Test complete voting workflow."""
        # Setup
        blockchain = Blockchain()
        private_key, public_key = generate_rsa_keys(key_size=1024)
        candidate = "Alice"
        
        # Blind signature
        blinded_msg, factor = blind_message(candidate, public_key)
        blind_sig = sign_blinded_message(blinded_msg, private_key)
        final_sig = unblind_signature(blind_sig, factor, public_key)
        
        # Cast vote
        vote_hash = hash_message(candidate)
        receipt = generate_receipt_code()
        block = blockchain.add_vote(vote_hash, final_sig, receipt)
        
        # Verify
        self.assertTrue(blockchain.is_chain_valid())
        found = blockchain.find_vote_by_receipt(receipt)
        self.assertIsNotNone(found)
        self.assertEqual(found.index, block.index)
    
    def test_multiple_votes(self):
        """Test multiple votes in blockchain."""
        blockchain = Blockchain()
        private_key, public_key = generate_rsa_keys(key_size=1024)
        candidates = ["Alice", "Bob", "Charlie"]
        
        for candidate in candidates:
            blinded_msg, factor = blind_message(candidate, public_key)
            blind_sig = sign_blinded_message(blinded_msg, private_key)
            final_sig = unblind_signature(blind_sig, factor, public_key)
            
            vote_hash = hash_message(candidate)
            receipt = generate_receipt_code()
            blockchain.add_vote(vote_hash, final_sig, receipt)
        
        # Verify all votes
        self.assertTrue(blockchain.is_chain_valid())
        self.assertEqual(blockchain.get_vote_count(), 3)


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestCryptoModule))
    suite.addTests(loader.loadTestsFromTestCase(TestBlockchain))
    suite.addTests(loader.loadTestsFromTestCase(TestUtilities))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)

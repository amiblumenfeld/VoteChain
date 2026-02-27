"""
Blockchain utilities for the Secure Voting System.

This module provides simple blockchain functionality including block creation,
chain validation, and vote storage.
"""

import hashlib
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Block:
    """Represents a single block in the blockchain."""
    index: int
    timestamp: str
    vote_hash: str  # Hash of encrypted vote
    previous_hash: str
    nonce: int = 0
    signature: Optional[str] = None  # Signature proof from voter
    receipt_code: Optional[str] = None  # User-facing receipt
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert block to dictionary."""
        return asdict(self)


class Blockchain:
    """Simple blockchain implementation for vote storage and verification."""
    
    def __init__(self):
        """Initialize blockchain with genesis block."""
        self.chain: List[Block] = []
        self.create_genesis_block()
    
    def create_genesis_block(self) -> None:
        """Create the first block (genesis block)."""
        genesis_block = Block(
            index=0,
            timestamp=datetime.now().isoformat(),
            vote_hash="0",
            previous_hash="0",
            nonce=0,
            receipt_code="GENESIS"
        )
        self.chain.append(genesis_block)
    
    def get_latest_block(self) -> Block:
        """Get the most recent block in the chain."""
        return self.chain[-1]
    
    def calculate_hash(self, block: Block) -> str:
        """
        Calculate SHA256 hash of a block.
        
        Args:
            block: Block to hash
            
        Returns:
            Hex-encoded hash string
        """
        block_dict = block.to_dict()
        # Don't include the signature in hash calculation
        block_dict.pop('signature', None)
        block_string = json.dumps(block_dict, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def add_vote(self, vote_hash: str, signature: str, receipt_code: str) -> Block:
        """
        Add a new vote to the blockchain.
        
        Args:
            vote_hash: Hash of the encrypted vote
            signature: Signature proof from voter
            receipt_code: User-facing receipt code
            
        Returns:
            The newly created block
        """
        latest_block = self.get_latest_block()
        previous_hash = self.calculate_hash(latest_block)
        
        new_block = Block(
            index=len(self.chain),
            timestamp=datetime.now().isoformat(),
            vote_hash=vote_hash,
            previous_hash=previous_hash,
            signature=signature,
            receipt_code=receipt_code
        )
        
        self.chain.append(new_block)
        return new_block
    
    def is_chain_valid(self) -> bool:
        """
        Validate the entire blockchain by checking hash links.
        
        Returns:
            True if chain is valid, False otherwise
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Recalculate hash of previous block
            previous_hash = self.calculate_hash(previous_block)
            
            # Check if previous hash matches
            if current_block.previous_hash != previous_hash:
                return False
        
        return True
    
    def find_vote_by_receipt(self, receipt_code: str) -> Optional[Block]:
        """
        Find a vote block by its receipt code.
        
        Args:
            receipt_code: The receipt code to search for
            
        Returns:
            Block if found, None otherwise
        """
        for block in self.chain:
            if block.receipt_code == receipt_code:
                return block
        return None
    
    def get_all_votes(self) -> List[Block]:
        """
        Get all vote blocks (excluding genesis block).
        
        Returns:
            List of blocks containing votes
        """
        return self.chain[1:]  # Skip genesis block
    
    def get_chain_as_dict(self) -> List[Dict[str, Any]]:
        """
        Convert entire chain to list of dictionaries.
        
        Returns:
            List of block dictionaries
        """
        return [block.to_dict() for block in self.chain]
    
    def validate_receipt(self, receipt_code: str) -> Dict[str, Any]:
        """
        Validate a receipt code and return block information.
        
        Args:
            receipt_code: The receipt code to validate
            
        Returns:
            Dictionary with validation result and block info
        """
        block = self.find_vote_by_receipt(receipt_code)
        
        if block is None:
            return {
                'valid': False,
                'message': 'Receipt not found in blockchain',
                'block': None
            }
        
        # Verify chain integrity
        is_valid = self.is_chain_valid()
        
        return {
            'valid': is_valid,
            'message': f'✅ Vote found in Block #{block.index}' if is_valid else '❌ Chain integrity check failed',
            'block': block.to_dict(),
            'block_index': block.index
        }
    
    def get_vote_count(self) -> int:
        """
        Get total number of votes cast (excluding genesis block).
        
        Returns:
            Number of votes in blockchain
        """
        return len(self.chain) - 1
    
    def export_chain(self) -> str:
        """
        Export chain as JSON string.
        
        Returns:
            JSON representation of blockchain
        """
        return json.dumps(self.get_chain_as_dict(), indent=2)
    
    def reset(self) -> None:
        """Reset blockchain to genesis state."""
        self.chain = []
        self.create_genesis_block()

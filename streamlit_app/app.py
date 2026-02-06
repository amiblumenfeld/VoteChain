"""
Streamlit application for document signing and verification.

This application provides a user-friendly interface to sign documents using
cryptographic algorithms and verify the authenticity of signed documents.
"""

import streamlit as st
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_v1_5
from Crypto.Hash import SHA256
import base64
import os

# Set page config
st.set_page_config(page_title="Document Signing & Verification", layout="wide")

# Title
st.title("📝 Document Signing & Verification Application")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select an operation:", ["Sign Document", "Verify Document", "Key Management"])

# Initialize session state for keys
if "private_key" not in st.session_state:
    st.session_state.private_key = None
if "public_key" not in st.session_state:
    st.session_state.public_key = None


def generate_keys():
    """Generate RSA key pair."""
    key = RSA.generate(2048)
    return key, key.publickey()


def sign_document(document_data: bytes, private_key: RSA.RsaKey) -> str:
    """
    Sign a document using RSA private key.
    
    Args:
        document_data: The document to sign as bytes
        private_key: RSA private key for signing
    
    Returns:
        Base64 encoded signature
    """
    hash_object = SHA256.new(document_data)
    signer = pkcs1_v1_5.new(private_key)
    signature = signer.sign(hash_object)
    return base64.b64encode(signature).decode()


def verify_document(document_data: bytes, signature_b64: str, public_key: RSA.RsaKey) -> bool:
    """
    Verify a document signature using RSA public key.
    
    Args:
        document_data: The document to verify as bytes
        signature_b64: Base64 encoded signature
        public_key: RSA public key for verification
    
    Returns:
        True if signature is valid, False otherwise
    """
    try:
        signature = base64.b64decode(signature_b64)
        hash_object = SHA256.new(document_data)
        verifier = pkcs1_v1_5.new(public_key)
        return verifier.verify(hash_object, signature)
    except Exception as e:
        st.error(f"Error during verification: {str(e)}")
        return False


# Page: Sign Document
if page == "Sign Document":
    st.header("🔐 Sign Document")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Generate Keys (if needed)")
        if st.button("Generate New Key Pair", key="gen_keys"):
            st.session_state.private_key, st.session_state.public_key = generate_keys()
            st.success("Key pair generated successfully!")
    
    if st.session_state.private_key:
        with col2:
            st.subheader("Current Key Status")
            st.success("✅ Private key loaded")
            st.success("✅ Public key loaded")
    else:
        st.warning("⚠️ No private key available. Generate a key pair first.")
    
    st.divider()
    
    # File upload for signing
    st.subheader("Upload Document to Sign")
    uploaded_file = st.file_uploader("Choose a file to sign", key="sign_uploader")
    
    if uploaded_file and st.session_state.private_key:
        if st.button("Sign Document", key="sign_btn"):
            try:
                file_data = uploaded_file.read()
                signature = sign_document(file_data, st.session_state.private_key)
                
                st.success("✅ Document signed successfully!")
                
                # Display signature
                st.subheader("Signature")
                st.text_area("Base64 Encoded Signature:", value=signature, height=150, disabled=True)
                
                # Download signature
                st.download_button(
                    label="Download Signature",
                    data=signature,
                    file_name=f"{uploaded_file.name}.sig",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"Error signing document: {str(e)}")
    elif uploaded_file and not st.session_state.private_key:
        st.warning("Please generate a key pair first to sign documents.")


# Page: Verify Document
elif page == "Verify Document":
    st.header("✅ Verify Document")
    
    st.subheader("Load Public Key for Verification")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Option 1: Use generated key from session**")
        if st.session_state.public_key:
            if st.button("Use Session Public Key"):
                st.success("✅ Using public key from current session")
        else:
            st.info("No public key in session. Generate one or import from file.")
    
    with col2:
        st.markdown("**Option 2: Import public key from file**")
        key_file = st.file_uploader("Upload public key file (.pem)", type=["pem", "txt"], key="key_uploader")
        if key_file:
            try:
                key_data = key_file.read()
                st.session_state.public_key = RSA.import_key(key_data)
                st.success("✅ Public key loaded successfully!")
            except Exception as e:
                st.error(f"Error loading public key: {str(e)}")
    
    st.divider()
    
    if st.session_state.public_key:
        st.subheader("Upload Document and Signature for Verification")
        
        col1, col2 = st.columns(2)
        
        with col1:
            document = st.file_uploader("Choose document to verify", key="verify_doc_uploader")
        
        with col2:
            signature_input = st.text_area("Paste signature (Base64 encoded):", height=150)
        
        if document and signature_input:
            if st.button("Verify Signature", key="verify_btn"):
                try:
                    doc_data = document.read()
                    is_valid = verify_document(doc_data, signature_input, st.session_state.public_key)
                    
                    if is_valid:
                        st.success("✅ Signature is VALID! Document authenticity confirmed.")
                    else:
                        st.error("❌ Signature is INVALID! Document may have been tampered with.")
                
                except Exception as e:
                    st.error(f"Error verifying document: {str(e)}")
    else:
        st.warning("⚠️ No public key available. Please load or generate a public key first.")


# Page: Key Management
elif page == "Key Management":
    st.header("🔑 Key Management")
    
    st.subheader("Generate New Key Pair")
    if st.button("Generate RSA Key Pair (2048 bits)", key="keymgmt_gen"):
        st.session_state.private_key, st.session_state.public_key = generate_keys()
        st.success("✅ New key pair generated!")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Export Private Key")
        if st.session_state.private_key:
            private_key_pem = st.session_state.private_key.export_key().decode()
            st.text_area("Private Key (PEM format):", value=private_key_pem, height=200, disabled=True)
            st.download_button(
                label="Download Private Key",
                data=private_key_pem,
                file_name="private_key.pem",
                mime="text/plain"
            )
        else:
            st.info("No private key generated yet.")
    
    with col2:
        st.subheader("Export Public Key")
        if st.session_state.public_key:
            public_key_pem = st.session_state.public_key.export_key().decode()
            st.text_area("Public Key (PEM format):", value=public_key_pem, height=200, disabled=True)
            st.download_button(
                label="Download Public Key",
                data=public_key_pem,
                file_name="public_key.pem",
                mime="text/plain"
            )
        else:
            st.info("No public key generated yet.")
    
    st.divider()
    
    st.subheader("Import Existing Keys")
    
    col1, col2 = st.columns(2)
    
    with col1:
        private_key_file = st.file_uploader("Import private key (.pem)", key="import_private")
        if private_key_file:
            try:
                key_data = private_key_file.read()
                st.session_state.private_key = RSA.import_key(key_data)
                st.success("✅ Private key imported!")
            except Exception as e:
                st.error(f"Error importing private key: {str(e)}")
    
    with col2:
        public_key_file = st.file_uploader("Import public key (.pem)", key="import_public")
        if public_key_file:
            try:
                key_data = public_key_file.read()
                st.session_state.public_key = RSA.import_key(key_data)
                st.success("✅ Public key imported!")
            except Exception as e:
                st.error(f"Error importing public key: {str(e)}")

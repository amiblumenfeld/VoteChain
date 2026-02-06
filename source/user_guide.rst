User Guide: Document Signing & Verification
=============================================

Overview
--------

The Document Signing & Verification Application is a Streamlit-based web interface that allows users to:

- **Sign documents** using RSA cryptography to create digital signatures
- **Verify signatures** to ensure document authenticity and integrity
- **Manage cryptographic keys** for signing and verification operations

This guide will walk you through the installation, setup, and usage of the application.

Prerequisites
-------------

Before you begin, ensure you have:

- **Python 3.8 or higher** installed on your system
- **Git** installed for version control
- A terminal/command prompt application

Installation & Setup
--------------------

1. **Clone the Repository**

   .. code-block:: bash

      git clone <repository-url>
      cd VoteChain

2. **Create a Virtual Environment**

   Virtual environments isolate project dependencies from your system Python installation.

   **On macOS/Linux:**

   .. code-block:: bash

      python3 -m venv .venv
      source .venv/bin/activate

   **On Windows:**

   .. code-block:: bash

      python -m venv .venv
      .venv\Scripts\activate

   You should see ``(.venv)`` prepended to your terminal prompt when activated.

3. **Install Dependencies**

   With the virtual environment activated, install all required packages:

   .. code-block:: bash

      pip install -r requirements.txt

   This will install:

   - **streamlit**: Web application framework
   - **pycryptodome**: Cryptography library for RSA operations
   - **sphinx** and **sphinx-autobuild**: Documentation tools
   - **invoke**: Task runner for automation

Running the Application
-----------------------

The application can be run using the Invoke task runner:

.. code-block:: bash

   invoke run-app

This command will:

1. Start the Streamlit development server
2. Open the application in your default web browser (usually at ``http://localhost:8501``)

**Alternative method** (without Invoke):

.. code-block:: bash

   streamlit run streamlit_app/app.py

Usage Guide
-----------

The application has three main sections accessible from the sidebar:

1. Sign Document
2. Verify Document
3. Key Management

Sign Document
~~~~~~~~~~~~~

To sign a document:

1. Navigate to the **Sign Document** tab from the sidebar
2. Click **Generate New Key Pair** to create a new RSA key pair (2048-bit)
   
   - You should see confirmation that both the private and public keys are loaded

3. Upload the document you want to sign by clicking **Choose a file to sign**
4. Click **Sign Document** button
5. The Base64-encoded signature will appear in a text area
6. Click **Download Signature** to save the signature to a file

**Important**: Keep your private key secure. Never share it with anyone.

Verify Document
~~~~~~~~~~~~~~~

To verify a document signature:

1. Navigate to the **Verify Document** tab from the sidebar
2. Load the public key using one of two methods:

   - **Option 1**: Use the session public key (if you just generated keys)
   - **Option 2**: Import a public key file by uploading a ``.pem`` file

3. Upload the original document to verify
4. Paste the Base64-encoded signature in the text area
5. Click **Verify Signature**

The application will display:

- **✅ Signature is VALID** if the signature matches the document
- **❌ Signature is INVALID** if the document has been tampered with or the signature doesn't match

Key Management
~~~~~~~~~~~~~~

The **Key Management** section provides tools for working with cryptographic keys:

**Generate New Key Pair**

- Click **Generate RSA Key Pair (2048 bits)** to create a new pair
- This overwrites any previously generated keys in the session

**Export Keys**

- Export your private and public keys in PEM format
- Download them as files for backup or transfer
- Use these keys in other cryptographic applications

**Import Keys**

- Upload previously saved ``.pem`` key files
- Import either private or public keys separately
- Useful for loading keys from backups or other systems

Key Concepts
------------

RSA Cryptography
~~~~~~~~~~~~~~~~

RSA (Rivest-Shamir-Adleman) is an asymmetric encryption algorithm that uses two keys:

- **Private Key**: Known only to you. Used to sign documents (prove ownership).
- **Public Key**: Can be shared with anyone. Used to verify your signatures.

Digital Signatures
~~~~~~~~~~~~~~~~~~

A digital signature is created by:

1. Hashing the document (creating a unique fingerprint)
2. Encrypting the hash with your private key

The signature proves that:

- The document came from you (authentication)
- The document hasn't been modified (integrity)

Verification Process
~~~~~~~~~~~~~~~~~~~~

Verification works by:

1. Creating a hash of the received document
2. Decrypting the signature using the signer's public key
3. Comparing the two hashes

If they match, the signature is valid.

Troubleshooting
---------------

Application Won't Start
~~~~~~~~~~~~~~~~~~~~~~~~

**Error**: ``command not found: streamlit``

**Solution**: Ensure the virtual environment is activated:

.. code-block:: bash

   source .venv/bin/activate  # macOS/Linux
   .venv\Scripts\activate      # Windows

**Error**: ``ModuleNotFoundError: No module named 'streamlit'``

**Solution**: Install dependencies:

.. code-block:: bash

   pip install -r requirements.txt

Cannot Verify Signature
~~~~~~~~~~~~~~~~~~~~~~~~

**Issue**: Signature verification fails for a document you know is correct

**Possible causes**:

1. Using the wrong public key (make sure it corresponds to the private key used for signing)
2. Document has been modified since signing
3. Wrong signature was pasted
4. Incorrect Base64 encoding of the signature

**Solution**: Generate a new key pair, sign again, and verify with the matching public key.

Port Already in Use
~~~~~~~~~~~~~~~~~~~~

**Error**: ``Streamlit needs to communicate with the server at http://localhost:8501``

**Solution**: The default port (8501) is in use. Run with a different port:

.. code-block:: bash

   streamlit run streamlit_app/app.py --server.port 8502

Building Documentation
----------------------

To build the Sphinx documentation locally:

.. code-block:: bash

   invoke build-doc

This starts a live server that rebuilds the documentation automatically when files change. Open your browser to ``http://localhost:8000`` to view the docs.

Best Practices
--------------

1. **Secure Your Private Key**
   
   - Download and store private keys in a secure location
   - Never share your private key with anyone
   - Use strong passwords if you encrypt your key files

2. **Backup Your Keys**
   
   - Keep copies of your keys in safe locations
   - If you lose your private key, you cannot sign new documents
   - If you lose your public key, you cannot verify old signatures

3. **Document Management**
   
   - Keep original documents and their signatures together
   - For important documents, store signatures separately from the documents
   - Document the public key used to verify each signature

4. **Communication**
   
   - Share only your public key with others
   - Receive signatures from others and verify them with their public keys
   - Never transmit private keys over insecure channels

Advanced Usage
--------------

Batch Verification
~~~~~~~~~~~~~~~~~~~

To verify multiple documents:

1. Export your public key from the Key Management tab
2. Share it with others or keep it for future verification
3. For each document, upload it and the corresponding signature
4. Use the Verify Document tab to check each one

Integration with Other Tools
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The RSA signing mechanism follows industry standards (PKCS#1 v1.5) and can be used with other cryptographic tools that support PEM format keys.

Frequently Asked Questions
--------------------------

**Q: How long are the signatures?**

A: Base64-encoded signatures for 2048-bit RSA keys are typically 344-512 characters long.

**Q: Can I use the same key pair indefinitely?**

A: Yes, RSA key pairs don't expire. However, for security reasons, it's recommended to generate new key pairs periodically and retire old ones.

**Q: What happens if I close the browser?**

A: The keys are stored in the Streamlit session. Closing the browser will lose them. Download your keys if you want to use them later.

**Q: Can this application sign multiple documents?**

A: Yes! Generate keys once, then sign and verify as many documents as needed during that session.

**Q: Is this suitable for production use?**

A: This application is designed as an educational tool. For production systems, consider using dedicated cryptographic libraries with additional security features.

Support & Feedback
------------------

For issues, questions, or feedback about this application, please refer to the project documentation or contact the development team.

---

**Last Updated**: February 2026

**Version**: 1.0

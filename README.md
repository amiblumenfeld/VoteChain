# VoteChain

A document signing and verification application built with Streamlit and RSA cryptography.

## Features

- 📝 **Sign Documents**: Create digital signatures for documents using RSA cryptography
- ✅ **Verify Signatures**: Verify document authenticity and integrity
- 🔑 **Key Management**: Generate, import, and export RSA key pairs
- 🌐 **User-Friendly Interface**: Web-based interface built with Streamlit

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd VoteChain
   ```

2. **Create and activate a virtual environment**
   
   **macOS/Linux:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
   
   **Windows:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

Using Invoke (recommended):
```bash
invoke run-app
```

Or directly with Streamlit:
```bash
streamlit run streamlit_app/app.py
```

The application will open in your browser at `http://localhost:8501`.

## Usage

The application has three main sections:

1. **Sign Document**: Upload a file and sign it with your private key
2. **Verify Document**: Upload a file and signature to verify authenticity
3. **Key Management**: Generate, export, and import RSA key pairs

For detailed usage instructions, see the [User Guide](source/user_guide.rst) or run:
```bash
invoke build-doc
```

## Project Structure

```
VoteChain/
├── streamlit_app/
│   └── app.py                 # Main Streamlit application
├── source/
│   ├── conf.py               # Sphinx configuration
│   ├── index.rst             # Documentation index
│   └── user_guide.rst        # Comprehensive user guide
├── tasks.py                  # Invoke task definitions
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Development

### Building Documentation

To build and serve the Sphinx documentation:
```bash
invoke build-doc
```

Documentation will be available at `http://localhost:8000`.

### Task Commands

Available Invoke tasks:

- `invoke run-app`: Start the Streamlit application
- `invoke build-doc`: Build and serve Sphinx documentation

## Technology Stack

- **Streamlit**: Web application framework
- **PyCryptodome**: Cryptography library
- **Sphinx**: Documentation generator
- **Invoke**: Task runner

## Security Notes

- This application is designed for educational purposes
- Store private keys securely and never share them
- For production use, consider using dedicated security libraries with additional features

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]

## Support

For questions or issues, please refer to the documentation or contact the development team.

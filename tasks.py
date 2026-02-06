from invoke import task

@task
def build_doc(c):
    """Run a live Sphinx autobuild server to build and serve documentation.
    This task invokes `sphinx-autobuild` to build Sphinx docs from the `source/`
    directory into the `build/` directory and watches for file changes to
    automatically rebuild and reload the documentation in the browser.
    Args:
        c: Execution context (e.g., an Invoke Context or similar) used to run
           shell commands.
    Raises:
        RuntimeError: If the documentation build command fails.
    """

    c.run("sphinx-autobuild source/ build/")


@task
def run_app(c):
    """Run the Streamlit application for document signing and verification.
    
    This task launches the Streamlit application which provides a user-friendly
    interface for signing documents and verifying signatures using RSA cryptography.
    
    Args:
        c: Execution context used to run shell commands.
    
    Usage:
        invoke run-app
    """
    c.run("streamlit run streamlit_app/app.py")
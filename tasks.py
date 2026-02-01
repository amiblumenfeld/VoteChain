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
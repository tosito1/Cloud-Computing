from invoke import task

from app import greet

@task
def test_greet(monkeypatch):
    import io
    from contextlib import redirect_stdout

    f = io.StringIO()
    with redirect_stdout(f):
        greet(None)
    output = f.getvalue().strip()
    assert output == "Hola, World!"


@task
def test(c):
    """Ejecuta las pruebas."""
    print("Ejecutando pruebas...")
    c.run("pytest") 

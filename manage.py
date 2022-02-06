import click
from app import app, db


@app.cli.command("init_db")
def init_db():
    from app import db
    import juxgen.models
    print("Initializing db")
    db.drop_all()
    db.create_all()
    db.session.commit()


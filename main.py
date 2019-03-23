from app import make_app
from configs import Config
from commands import db_cli


app = make_app(Config)
app.cli.add_command(db_cli)

if __name__ == '__main__':
    app.run()



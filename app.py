import logging
import random
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Query

from juxgen.manage import cmds
from juxgen.views import routes


logger = logging.getLogger("juxgen")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


class GetRandomQuery(Query):
    def get_random(self):
        return self.get(random.randint(0, self.count() - 1))


# flask setup
app = Flask(__name__, static_url_path="")
app.config.from_object("juxgen.config.Config")
db = SQLAlchemy(app, query_class=GetRandomQuery)
app.register_blueprint(routes)
app.register_blueprint(cmds)

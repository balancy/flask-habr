from flask import Flask, request, render_template
from werkzeug.exceptions import BadRequest
from flask_migrate import Migrate

from habr import config
from habr.models.database import db
from habr.views.habr import habr_app

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(habr_app)


# @app.route("/")
# @app.route("/<name>/")
# def hello_world(name="World"):
#     return render_template("index.html", name=name)
#
#
# @app.route("/product/<int:product_id>/")
# def get_product(product_id):
#     return f"product {product_id!r}"
#
#
# @app.route("/sum/")
# def sum_values():
#     try:
#         a = int(request.args.get("a"))
#         b = int(request.args.get("b"))
#     except ValueError:
#         raise BadRequest("`a` and `b` have to be integers")
#     return {"a": a, "b": b, "sum": a + b}

from flask import Flask
from praxis.routes.projects import projects_blueprint
from praxis.routes.experts import experts_blueprint
from praxis.routes.praxis import praxis_blueprint

app = Flask(__name__)
app.config.from_object('praxis.config.DevelopmentConfig')

app.register_blueprint(projects_blueprint)
app.register_blueprint(experts_blueprint)
app.register_blueprint(praxis_blueprint)
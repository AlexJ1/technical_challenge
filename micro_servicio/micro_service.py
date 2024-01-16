import configparser

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# DB - Configuración.
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@localhost/mydatabase'
db = SQLAlchemy(app)

# Creación de modelo para la base de datos.
class dependencia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    repositorio = db.Column(db.String(255), nullable=False)
    groupId = db.Column(db.String(255), nullable=False)
    artifactId = db.Column(db.String(255), nullable=False)
    version = db.Column(db.String(255), nullable=False)

    def __init__(self, repositorio, groupId, artifactId, version):
        self.repositorio = repositorio
        self.groupId = groupId
        self.artifactId = artifactId
        self.version = version

    def to_dict(self):
        return {
            'id': self.id,
            'repositorio': self.repositorio,
            'groupId': self.groupId,
            'artifactId': self.artifactId,
            'version': self.version
        }

# Configuración de endpoint de recepción.
@app.route('/api/reportar', methods=['POST'])
def reportar_dependencias():
    data = request.json

    # Verificar que data es un diccionario y contiene las claves esperadas
    if not isinstance(data, dict) or 'repositorio' not in data or 'dependencias' not in data:
        return jsonify({"error": "Formato de datos incorrecto"}), 400

    repositorio = data['repositorio']
    dependencias = data['dependencias']

    # Verificar que dependencias es una lista
    if not isinstance(dependencias, list):
        return jsonify({"error": "Formato de dependencias incorrecto"}), 400

    for dep in dependencias:
        # Verificar que cada dependencia es un diccionario y contiene los valores  esperados
        if not isinstance(dep, dict) or 'groupId' not in dep or 'artifactId' not in dep or 'version' not in dep:
            continue

        nueva_dependencia = dependencia(
            repositorio=repositorio,
            groupId=dep['groupId'],
            artifactId=dep['artifactId'],
            version=dep['version']
        )
        db.session.add(nueva_dependencia)

    db.session.commit()
    return jsonify({"message": "success"}), 200

@app.route('/api/repositorios', methods=['GET'])
def get_repositorios():
    repositorios = dependencia.query.all()
    return jsonify([repo.to_dict() for repo in repositorios])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Control de base de datos.
    app.run(debug=True)
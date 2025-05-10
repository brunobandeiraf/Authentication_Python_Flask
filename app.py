from flask_login import LoginManager, login_user, current_user
from models.user import User
from flask import Flask, request, jsonify
from database import db
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Configuração do CORS para desenvolvimento
CORS(app, supports_credentials=True, resources={
    r"/*": {
        "origins": "*",  # Permite todas as origens em desenvolvimento
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "expose_headers": ["Content-Type"],
        "supports_credentials": True
    }
})

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)

login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if username and password:
       #login
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)  
            print(current_user.is_authenticated)    
            return jsonify({"message": "Autenticação realizada com sucesso!"}), 200
    
    return jsonify({"message": "Credenciais inválidas!"}), 400


@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return jsonify({"message": "Username e senha são obrigatórios!"}), 400
    
    # Verifica se o usuário já existe
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "Username já está em uso!"}), 400
    
    # Cria novo usuário
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "Usuário cadastrado com sucesso!"}), 201


@app.route("/users", methods=["GET"])
def list_users():
    users = User.query.all()
    users_list = [{"id": user.id, 
                   "username": user.username,
                   "password": user.password
                   } for user in users]
    return jsonify(users_list), 200

@app.route("/hello-world", methods=["GET"])
def hello_world():
 return "Hello world"

if __name__ == '__main__':
 app.run(debug=True)
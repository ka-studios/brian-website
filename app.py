from flask import Flask, render_template, session, request, redirect, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import hashlib
import pickle

# initial definitions
app = Flask(__name__, template_folder="static")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

with open("key.db", 'r') as key:
    app.secret_key = hashlib.sha256(key.read().encode()).hexdigest()
    key.close()

print(app.secret_key)

# user model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# index route
@app.route("/")
async def index():
    return render_template("index.html")
@app.route("/styles.css")
async def styles():
    return send_from_directory("static", "styles.css")
@app.route("/login", methods=['GET', 'POST'])
async def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user = User.query.filter_by(username=username, password=hashed_password).first()
        if user:
            session['username'] = username
            return redirect('/')
        else:
            return 'Invalid username or password'
    return render_template('login.html')

@app.route("/signup", methods=['GET', 'POST'])
async def signup():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        with app.app_context():
            if User.query.filter_by(username=username).first():
                return "Username is already taken"
            else:
                new_user = User(username=username, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                return redirect("login")
    return render_template("signup.html")

@app.route('/download')
async def download():
    return render_template("download.html")

@app.route('/main', methods = ['GET', "POST"])
async def main():
    if request.method == "POST":
        search = request.form.get("search-input")
        results = list()

        with open("products.db", 'rb') as file:
            products = pickle.loads(file.read())
            file.close()

        for item in products.keys():
            if search in item:
                results.append(item)
                request.form["image"].__setattr__["src"]    = products[item][0]
                request.form["image"].__setattr__["hidden"] = False

    return render_template("main.html")

def init_db():
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username="brian").first():
            hashed_password = hashlib.sha256("password".encode()).hexdigest()
            new_user = User(username="brian", password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4444, debug=True)
    init_db()

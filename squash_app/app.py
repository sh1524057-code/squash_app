from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
db = SQLAlchemy(app)

# 選手データ
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    team = db.Column(db.String)

# 結果データ
class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/history")
def history_page():
    return render_template("history.html")

# 選手検索API
@app.route("/search_player")
def search_player():
    q = request.args.get("q","")
    players = Player.query.filter(Player.name.contains(q)).all()
    return jsonify([{"label": f"{p.name}（{p.team}）"} for p in players])

# 投稿保存
@app.route("/post_result", methods=["POST"])
def post_result():
    text = request.json["text"]
    db.session.add(Result(text=text))
    db.session.commit()
    print("保存:", text)
    return {"status":"ok"}

# 履歴取得
@app.route("/results")
def results():
    data = Result.query.order_by(Result.id.desc()).all()
    return jsonify([{"text":r.text} for r in data])

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
import os
port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)


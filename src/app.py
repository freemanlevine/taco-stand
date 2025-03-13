from flask import Flask, redirect
from flask import request
from flask import render_template

from . import db, models, game

app = Flask(__name__)

links = {
    "home": '<div><a href="/">Back to Home</a></div>',
    "shops": '<div><a href="/shops">View Shops</a></div>',
    "customers": '<div><a href="/customers">View Customers</a></div>',
    "player": '<div><a href="/player">Load Player Profile</a></div>',
}

@app.route("/")
def home():
    active_player = db.get_active_player()
    return render_template(
        "home.html",
        player=active_player,
        shop_price=game.shop_price
    )

@app.route("/shop/<int:shop_id>/delete")
def delete_shop(shop_id):
    db.delete_shop(shop_id)
    return redirect("/shops")

@app.route("/increment")
def increment_simulation():
    active_player = db.get_active_player()
    return render_template(
        "increment.html",
        messages=game.increment_simulation(),
        player=active_player,
        shop_price=game.shop_price
    )

@app.route("/build-shop")
def build_shop():
    active_player = db.get_active_player()
    return render_template(
        "build_shop.html",
        message = db.build_shop(active_player.id, game.shop_price),

    )

@app.route("/player")
def show_players():
    with db.get_session() as session:
        players = db.get_all(session, models.Player)
        return render_template(
            "list_players.html",
            players=players,
            button_text="Create New Player"
        )

@app.route("/player/create")
def create_player():
    name = request.args.get('name')
    difficulty = request.args.get('difficulty')
    try:
        db.create_player(name, starting_money=game.difficulties[difficulty])
        return render_template(
            "player/create.html",
            name=name,
            difficulty=difficulty,
            button_text="Create"
        )
    except Exception as e:
        return render_template(
            "player/create.html",
            error=e,
            button_text="Create"
        )

@app.route("/player/<int:player_id>/load/")
def load_player(player_id):
    html = ''
    try:
        active_player = db.set_active_player(player_id)
        html = f'Player {active_player.name} loaded!'
    except Exception as e:
        html += f'Error loading player profile - {e}'
    html += links['home']
    return html

@app.route("/player/<int:player_id>/delete/")
def delete_player(player_id):
    try:
        db.delete_player(player_id)
        return redirect('/player')
    except Exception as e:
        print(f'Error deleting player - {e}')
        return redirect('/player')

@app.route("/shops")
def show_shops():
    with db.get_session() as session:
        shops = db.get_all(session, models.Shop)
        return render_template(
            "shops.html",
            shops=shops
        )

@app.route("/customers")
def show_customers():
    with db.get_session() as session:
        customers = db.get_all(session, models.Customer)
        return render_template(
            "customers.html",
            customers=customers
        )

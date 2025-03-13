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

def player_block():
    html = ""
    try:
        active_player = db.get_active_player()
        html += f'<div>Current Player: {active_player.name} - ${active_player.money/100.0:,.2f}<br>'
        html += f'<a href="/build-shop">Build Shop - ${game.shop_price/100:,.2f}</a><br>'
        html += f'<a href="increment">Increment Simulation</a></div><br>'
    except Exception as e:
        html += 'No Player loaded<br>'
    return html

@app.route("/")
def home():
    active_player = db.get_active_player()
    return render_template(
        "home.html",
        name=active_player.name,
        money=f'{active_player.money/100.0:,.2f}',
        shop_price=f'{game.shop_price/100.0:,.2f}'
    )

@app.route("/shop/<int:shop_id>/delete")
def delete_shop(shop_id):
    db.delete_shop(shop_id)
    return redirect("/shops")

@app.route("/increment")
def increment_simulation():
    html = "<div> Actions During Turn:<br>"
    html += "<br>".join(game.increment_simulation())
    html += "</div><br>"
    html += player_block()
    html += links["home"]
    return html

@app.route("/build-shop")
def build_shop():
    active_player = db.get_active_player()
    html = db.build_shop(active_player.id, game.shop_price)
    html += "<br>"
    html += player_block()
    html += links["home"]
    return html

@app.route("/player")
def show_players():
    engine = db.get_engine()
    html = ""
    with db.Session(engine) as session:
        players = db.get_all(session, models.Player)
        for player in players:
            html += f'<div>{player.name} - ${player.money/100.0:,.2f}</div>'
            html += f'<div><a href="/player/{player.id}/load">Load Profile</a></div>'
            html += f'<div><a href="/player/{player.id}/delete">Delete Profile</a></div>'
        html += create_player_form("Create New Player")
    html += links["home"]
    return html

difficulties = {
    'easy': 100*100, # $100,
    'medium': 75*100, # $100,
    'hard': 50*100, # $100,
    'ultra': 25*100 # $100
}

difficulty_selector = f"""
<label for="difficulty">Difficulty</label>
<select name="difficulty" id="difficulty">
  <option value="easy">Easy - $100</option>
  <option value="medium">Medium - $75</option>
  <option value="hard">Hard - $50</option>
  <option value="ultra">Ultra - $25</option>
</select>
"""

def create_player_form(button_text):
    html = '<form action="/player/create">'
    html += '<label for="name">Name:</label>'
    html += '<input id="name" name="name"> '
    html += difficulty_selector
    html += f'<input type="submit" value="{button_text}">'
    html += '</form>'
    return html

@app.route("/player/create")
def create_player():
    name = request.args.get('name')
    difficulty = request.args.get('difficulty')
    html = ''
    try:
        db.create_player(name, starting_money=difficulties[difficulty])
        html += f'Player {name} created on {difficulty} difficulty!'
    except Exception as e:
        html += f'Error creating player - {e}'
    html += '<br><br>Create Another Player:'
    html += create_player_form("Create")
    html += links['home']
    return html

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

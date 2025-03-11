from flask import Flask

from . import db, models

app = Flask(__name__)

links = {
    "home": '<div><a href="/">Back to Home</a><div>',
    "shops": '<div><a href="/shops">View Shops</a><div>',
    "customers": '<div><a href="/customers">View Customers</a><div>'
}

@app.route("/")
def hello_world():
    html = "<p>Welcome to the Taco Stand App!</p>"
    html += links["shops"]
    html += links["customers"]
    return html

@app.route("/shops")
def show_shops():
    engine = db.get_engine()
    html = ""
    with db.Session(engine) as session:
        shops = db.get_all(session, models.Shop)
        for shop in shops:
            html += '<div>' + shop.get_menu_text() + '<div>'
    html += '<br>'
    html += links["home"]
    return html

@app.route("/customers")
def show_customers():
    engine = db.get_engine()
    html = ""
    with db.Session(engine) as session:
        customers = db.get_all(session, models.Customer)
        for customer in customers:
            html += '<div>{} - ${:,.2f} remaining</div>'.format(
                customer.name,
                customer.money / 100.0
            )
    html += '<br>'
    html += links["home"]
    return html

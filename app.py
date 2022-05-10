from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)

class Inventory(db.Model):
    __tablename__ = 'items'
    item_id = db.Column(db.String(300), primary_key=True)
    item_qty = db.Column(db.Integer, nullable=False)
    location_id = db.Column(db.String(300), db.ForeignKey('locations.location_id'))

    location = db.relationship('Location', foreign_keys=location_id)

    def __rep__(self):
        return '<Item %r>' % self.id

class Location(db.Model):
    __tablename__ = 'locations'
    location_id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(300))
    

    def __repr__(self):
        return '<Location %r>' % self.location_id

@app.route('/', methods=['POST','GET'])
def home():
    if (request.method == 'POST') and ('item_name' in request.form):
        item_name = request.form['item_name']
        item_qty = request.form['item_qty']
        location = request.form['location']
        new_item = Inventory(item_id=item_name, item_qty=item_qty, location_id=location)

        try:
            db.session.add(new_item)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error while adding the item'
    
    if (request.method == "POST") and ('location_name' in request.form):
        location_name    = request.form["location_name"]
        new_location     = Location(location_name=location_name)

        try:
            db.session.add(new_location)
            db.session.commit()
            return redirect("/")
        
        except:
            return "There Was an issue while add a new Location"
    else:
        items = Inventory.query.all()
        locations = Location.query.all()
        return render_template("index.html", items=items, locations=locations)



@app.route('/delete/<string:item_id>')
def delete(item_id):
    item_to_delete = Inventory.query.get_or_404(item_id)
    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an error while deleting that item'


@app.route('/update/<string:item_id>', methods=['GET','POST'])
def update(item_id):
    item = Inventory.query.get_or_404(item_id)

    if request.method == 'POST':
        item.item_id = request.form['item_name']
        item.item_qty = request.form['item_qty']
        item.location_id = request.form['location']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue while updating that task'

    else:
        locations = Location.query.all()
        return render_template('update.html', item=item, locations=locations)

@app.route('/deleteLocation/<string:location_id>')
def deleteLocation(location_id):
    location_to_delete = Location.query.get_or_404(location_id)
    try:
        db.session.delete(location_to_delete)
        db.session.commit()
        return redirect('/locations/')
    except:
        return 'There was an error while deleting that location'


@app.route('/updateLocation/<string:location_id>', methods=['GET','POST'])
def updateLocation(location_id):
    location = Location.query.get_or_404(location_id)

    if request.method == 'POST':
        location.location_name = request.form['location_name']
    
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue while updating that task'

    else:
        return render_template('updateLocation.html', location=location)

if __name__ == "__main__":
    app.run(debug=True)
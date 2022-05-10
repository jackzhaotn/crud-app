from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300), nullable=False)

    def __rep__(self):
        return '<Item %r>' % self.id

@app.route('/', methods=['POST','GET'])
def home():
    if request.method == 'POST':
        item_content = request.form['content']
        new_item = Inventory(content=item_content)

        try:
            db.session.add(new_item)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error while adding the item'

    else:
        items = Inventory.query.all()
        return render_template("index.html", items=items)

@app.route('/delete/<int:id>')
def delete(id):
    item_to_delete = Inventory.query.get_or_404(id)
    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an error while deleting that item'


@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    item = Inventory.query.get_or_404(id)

    if request.method == 'POST':
        item.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue while updating that task'

    else:
        return render_template('update.html', item=item)

if __name__ == "__main__":
    app.run(debug=True)
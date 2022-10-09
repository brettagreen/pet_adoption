"""Adopt-a-pet application."""

from flask import Flask, redirect, render_template, flash
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "bush-did-911"

connect_db(app)
db.create_all()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#######################
#########PETS##########
#######################

@app.route("/")
def home():
    """list all pets in database, including whether they are available for adoption"""
    pets = Pet.query.all()
    return render_template('pets.html', pets=pets)

@app.route('/add', methods=['GET', 'POST'])
def add_pet():
    """presents form for adding new pet to database and handles form submission logic as well"""
    form = AddPetForm()
    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data
        #data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        #new_pet = Pet(**data)
        pet = Pet(name=name, species=species, photo_url=photo_url, age=age, notes=notes)
        db.session.add(pet)
        db.session.commit()
        flash(f"{pet.name} has been added!")
        return redirect('/')
    else:
        return render_template('new_pet_form.html', form=form)

@app.route('/<int:pet_id>', methods=['GET', 'POST'])
def show_edit_form(pet_id):
    """presents form for editing pet info and handles form submission logic as well"""
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)
    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data

        db.session.add(pet)
        db.session.commit()
        flash(f"{pet.name}'s info has been updated.")
        return redirect('/')
    else:
        return render_template('pet_info_edit.html', pet=pet, form=form)
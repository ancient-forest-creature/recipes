from flask_app import app
from flask import render_template, request, redirect, url_for, flash, session
from flask_app.models.user import User
from flask_app.models.recipe import Recipe


@app.route('/create_recipe', methods=['POST'])
def create_recipe():
    print("create recipe request from is:")
    print(request.form)
    if not Recipe.validate_recipe(request.form):
        flash("Name, Description, and Instructions all need at least 3 charaters","add")
        return redirect('/add')
    data ={
        "name": request.form['name'],
        "description": request.form['description'],
        "instruction": request.form['instruction'],
        "made_on": request.form['made_on'],
        "under_30": request.form['under_30'],
        "user_id": session['user_id']
    }
    print(f"recipe created is: {data}")
    res = Recipe.create(data)
    print(f"res is {res}")
    return redirect('/dashboard')

@app.route('/add')
def add_recipe():
    if 'user_id' not in session:
        flash("Please login to view content","bad_user")
        return redirect('/')
    return render_template('add.html')

@app.route('/read/<int:id>')
def read_recipe(id):
    if 'user_id' not in session:
        flash("Please login to view content","bad_user")
        return redirect('/')
    data = {'id':id}
    user = User.get_user(session['user_id'])
    recipe = Recipe.get_recipe(data) 
    return render_template('show.html', recipe = recipe, user = user)

@app.route('/edit/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:
        flash("Please login to view content","bad_user")
        return redirect('/')
    data = {'id':id}
    recipe = Recipe.get_recipe(data) 
    print('edit result is:')
    print(recipe.under_30)
    return render_template('edit.html', recipe = recipe)

@app.route('/update_recipe', methods=['POST'])
def update_recipe():
    print("update recipe request from is:")
    print(request.form)
    if not Recipe.validate_recipe(request.form):
        flash("Name, Description, and Instructions all need at least 3 charaters","edit")
        id=request.form['id']
        return redirect(url_for('edit_recipe', id = id))
    data ={
        "id": request.form['id'],
        "name": request.form['name'],
        "description": request.form['description'],
        "instruction": request.form['instruction'],
        "made_on": request.form['made_on'],
        "under_30": request.form['under_30']
    }
    print(f"recipe created is: {data}")
    res = Recipe.update(data)
    print(f"res is {res}")
    return redirect('/dashboard')


@app.route('/delete_reciept/<int:id>')
def result(id):
    data = {'id':id}
    Recipe.delete_recipe(data)
    return redirect('/dashboard')
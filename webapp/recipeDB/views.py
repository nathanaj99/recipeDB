from flask import Flask, request, session, redirect, url_for, render_template, flash
from .models import get25Recipes, search_recipes2, recipes_by_author, specific_recipe_query, recipe_backward_search

app = Flask(__name__)


@app.route('/')
def index():
    recipes = get25Recipes()
    
    return render_template(
        'index.html',
        result = recipes,
        success = "success"
        )

@app.route('/search', methods=['GET','POST'])
def search():
    if request.method == "POST":
        details = request.form
        phrase = details["phrase"]
        recipes = search_recipes2(phrase)

        return render_template(
            'search.html',
            result = recipes,
            success = "success"
        )
    return render_template('search.html')

@app.route('/advanced_search', methods=['GET','POST'])
def advanced_search():
    if request.method=="POST":
        d = request.form
        options = d.getlist("list")
        temp = list()
        for i in options:
            temp.append(i.split(";"))
        print(temp)

        return render_template(
            'advancedSearch.html',
            success = "success"
        )
    return render_template('advancedSearch.html')

@app.route('/backwards_ingredient', methods=['GET','POST'])
def backwards_ingredient():
    if request.method=="POST":
        d = request.form
        options = d.get("list")
        options = options[:-1].split(",")
        result = recipe_backward_search(options)
        return render_template(
            'backwardsIngredient.html',
            result = result,
            success = "success"
        )
    return render_template('backwardsIngredient.html')

@app.route('/recipe/<recipe_id>', methods=['GET','POST'])
def specific_recipe(recipe_id):
    result = specific_recipe_query(recipe_id)
    return render_template(
        'recipe.html',
        result=result.data(),
        success='success'
    )

@app.route('/author_recipes/<author>', methods=['GET','POST'])
def author_recipes(author):
    result = recipes_by_author(author)
    return render_template(
        'authorRecipes.html',
        result = result,
        success='success'
    )
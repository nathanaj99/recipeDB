from flask import Flask, request, session, redirect, url_for, render_template, flash
from .models import get25Recipes, search_recipes, recipes_by_author

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
        recipes = search_recipes(phrase)

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

@app.route('/author_recipes/<author>', methods=['GET','POST'])
def author_recipes(author):
    result = recipes_by_author(author)
    return render_template(
        'authorRecipes.html',
        result = result,
        success='success'
    )
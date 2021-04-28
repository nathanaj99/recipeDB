from flask import Flask, request, session, redirect, url_for, render_template, flash
from .models import get25Recipes, search_recipes2, recipes_by_author, specific_recipe_query, advanced_query, \
    recipe_backward_search, recipes_by_tag, category_query

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

def split_range(hi, d):
    score = d[hi].split(',')
    min_val, max_val = score[0], score[1]
    return min_val, max_val

@app.route('/advanced_search', methods=['GET','POST'])
def advanced_search():
    if request.method == "POST":
        d = request.form
        # health score comes in a range (a,b)
        dic = {}
        dic['min_health'], dic['max_health'] = split_range("health", d)
        dic['min_rating'], dic['max_rating'] = split_range("rating-val", d)
        dic['min_calories'], dic['max_calories'] = split_range("calorie-amt", d)
        dic['min_protein'], dic['max_protein'] = split_range("protein-amt", d)
        dic['min_sugar'], dic['max_sugar'] = split_range("sugar-amt", d)
        dic['min_sodium'], dic['max_sodium'] = split_range("sodium-amt", d)
        dic['min_cholesterol'], dic['max_cholesterol'] = split_range("cholesterol-amt", d)
        dic['min_carbs'], dic['max_carbs'] = split_range("carbs-amt", d)
        dic['min_fat'], dic['max_fat'] = split_range("fat-amt", d)
        dic['min_fiber'], dic['max_fiber'] = split_range("fiber-amt", d)
        dic['min_potassium'], dic['max_potassium'] = split_range("potassium-amt", d)
        dic['min_calcium'], dic['max_calcium'] = split_range("calcium-amt", d)
        dic['min_vitamina'], dic['max_vitamina'] = split_range("vitamina-amt", d)
        dic['min_vitaminc'], dic['max_vitaminc'] = split_range("vitaminc-amt", d)
        dic['tags'] = d.getlist("tag")
        dic['phrase'] = d['phrase'].lower().strip()

        result = advanced_query(dic)
        print(result)

        return render_template(
            'advancedSearch.html',
            result = result,
            success="success"
        )
    return render_template('advancedSearch.html')

@app.route('/backwards_ingredient', methods=['GET','POST'])
def backwards_ingredient():
    if request.method=="POST":
        d = request.form
        options = d.get("list").strip()
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
        success='success',
        author = author
    )

@app.route('/tag_recipes/<tag>', methods=['GET','POST'])
def tag_recipes(tag):
    result = category_query(tag)
    return render_template(
        'tagRecipes.html',
        result = result,
        success='success',
        tag = tag
    )

@app.route('/category_recipes/<category>', methods=['GET','POST'])
def category_recipes(category):
    result = category_query(category)
    return render_template(
        'category.html',
        result = result,
        success='success',
        category = category
    )
from py2neo import Graph, Node, Relationship
from datetime import datetime
import os
import uuid

recipe_graph = Graph("bolt://localhost:7687/neo4j", password="Voltrox19")

def get25Recipes():
    query = """
    MATCH (n:sch__Recipe)-[:sch__recipeInstructions]->(ins:sch__ItemList), (n)-[:sch__tags]->(t:ns0__RecipeTag),(n)-[:sch__author]->(a:ns0__Author) RETURN n,ins,collect(t.rdfs__label[0]) as tags,collect(distinct a.rdfs__label[0]) as authors LIMIT 25
    """

    return recipe_graph.run(query)

def search_recipes(phrase):
    query = """
    MATCH (n:sch__Recipe)-[:sch__recipeInstructions]->(ins:sch__ItemList) WHERE toLower(n.rdfs__label[0]) CONTAINS toLower(\""""+phrase+"""\") RETURN n,ins LIMIT 25
    """

    return recipe_graph.run(query)

def search_recipes2(phrase):
    phrase = phrase.lower().strip()
    query = """
    MATCH (a:ns0__Author)<-[:sch__author]-(n:sch__Recipe) 
    WITH n, a, toLower(n.rdfs__label[0]) AS name 
    WHERE name =~ '.*""" + phrase + """.*' 
    RETURN n, COLLECT(a) AS a
    """

    return recipe_graph.run(query)

def recipe_backward_search(list_ingredients):
    query = 'MATCH (a:ns0__Author)<-[:sch__author]-(n:sch__Recipe) WHERE'
    if len(list_ingredients) > 1:
        for i in list_ingredients[:-1]:
            query += '(size([ingredient IN n.sch__recipeIngredient WHERE toLower(ingredient) =~ ".*' + i.lower().strip() + '.*"]) > 0) AND '
    query += '(size([ingredient IN n.sch__recipeIngredient WHERE toLower(ingredient) =~ ".*' + list_ingredients[-1].lower().strip() + '.*"]) > 0) '
    query += 'RETURN n, COLLECT(a) AS a'

    return recipe_graph.run(query)

def specific_recipe_query(uri):
    query = """
    MATCH (a:ns0__Author)<-[:sch__author]-(n:sch__Recipe)-[:sch__nutrition]->(nut:sch__NutritionInformation), 
    (ins:sch__ItemList)<-[:sch__recipeInstructions]-(n:sch__Recipe)-[:sch__tags]->(t:ns0__RecipeTag) 
    WHERE toLower(n.rdfs__label[0]) =~ '""" + uri.lower().strip() + """' 
    RETURN n, COLLECT(DISTINCT t) AS t, COLLECT(DISTINCT a) AS a, nut, ins
    """

    return recipe_graph.run(query)

def advanced_query(dic):
    query = """
    MATCH (a:ns0__Author)<-[:sch__author]-(n:sch__Recipe)-[:sch__nutrition]->(nut:sch__NutritionInformation)
    WHERE (toLower(n.rdfs__label[0]) =~ '.*""" + dic['phrase'] + """.*')
    AND (""" + dic['min_health'] + """ <= n.sch__healthScore[0] <= """ + dic['max_health'] + """)
    AND (""" + dic['min_rating'] + """ <= n.sch__aggregateRating[0] <= """ + dic['max_rating'] + """)
    AND (""" + dic['min_protein'] + """ <= nut.sch__proteinContentDV[0] <= """ + dic['max_protein'] + """)
    AND (""" + dic['min_calories'] + """ <= nut.sch__calories[0] <= """ + dic['max_calories'] + """)
    AND (""" + dic['min_sodium'] + """ <= nut.sch__sodiumContentDV[0] <= """ + dic['max_sodium'] + """)
    AND (""" + dic['min_sugar'] + """ <= nut.sch__sugarContentDV[0] <= """ + dic['max_sugar'] + """)
    AND (""" + dic['min_cholesterol'] + """ <= nut.sch__cholesterolContentDV[0] <= """ + dic['max_cholesterol'] + """)
    AND (""" + dic['min_carbs'] + """ <= nut.sch__carbohydrateContentDV[0] <= """ + dic['max_carbs'] + """)
    AND (""" + dic['min_fat'] + """ <= nut.sch__fatContentDV[0] <= """ + dic['max_fat'] + """)
    AND (""" + dic['min_fiber'] + """ <= nut.sch__fiberContentDV[0] <= """ + dic['max_fiber'] + """)
    AND (""" + dic['min_potassium'] + """ <= nut.sch__potassiumContentDV[0] <= """ + dic['max_potassium'] + """)
    AND (""" + dic['min_calcium'] + """ <= nut.sch__calciumContentDV[0] <= """ + dic['max_calcium'] + """)
    AND (""" + dic['min_vitamina'] + """ <= nut.sch__vitaminAContentDV[0] <= """ + dic['max_vitamina'] + """)
    AND (""" + dic['min_vitaminc'] + """ <= nut.sch__vitaminCContentDV[0] <= """ + dic['max_vitaminc'] + """)
    RETURN n, COLLECT(a) AS a
    """

    return recipe_graph.run(query)

def recipes_by_author(author):
    query = """
    MATCH (a:ns0__Author)<-[:sch__author]-(n:sch__Recipe)-[:sch__nutrition]->(nut:sch__NutritionInformation)
    WHERE toLower(a.rdfs__label[0]) =~ '.*""" + author.lower().strip() + """.*'
    RETURN n, COLLECT(a) AS a
    """

    return recipe_graph.run(query)

def recipes_by_tag(tag):
    query = """
    MATCH (t:ns0__RecipeTag)<-[:sch__tags]-(n:sch__Recipe)-[:sch__author]->(a:ns0__Author)
    WHERE toLower(t.rdfs__label[0]) =~ '.*""" + tag.lower().strip() + """.*'
    RETURN n, COLLECT(a) AS a
    """

    return recipe_graph.run(query)

def category_query(category):
    query = ""
    if category == 'Healthy':
        query = """
        MATCH (a:ns0__Author)<-[:sch__author]-(n:sch__Recipe)
        WHERE (7.5 <= n.sch__healthScore[0] <= 10) RETURN n, COLLECT(a) AS a
        """

    elif category == 'Cheat Day':
        query = """
        MATCH (a:ns0__Author)<-[:sch__author]-(n:sch__Recipe)
        WHERE (0 <= n.sch__healthScore[0] <= 3.5) RETURN n, COLLECT(a) AS a
        """

    elif category == 'Dairy Free':
        query = """
        MATCH (a:ns0__Author)<-[:sch__author]-(n:sch__Recipe)-[:sch__tags]->(t:ns0__RecipeTag)
        WHERE (t.uri IN ['http://recipedb.com/tag100', 'http://recipedb.com/tag811', 'http://recipedb.com/tag1239'])
        RETURN n, COLLECT(a) AS a"""

    elif category == 'Tropical':
        tags = [524, 413, 620, 733, 111, 298, 372, 646, 49, 371, 389, 998, 213, 536, 472, 937, 900]
        tags = ['http://recipedb.com/tag' + str(i) for i in tags]
        tags = '[\'' + '\', \''.join(tags) + '\']'
        query = """
        MATCH (a:ns0__Author)<-[:sch__author]-(n:sch__Recipe)-[:sch__tags]->(t:ns0__RecipeTag)
        WHERE (t.uri IN """ + tags + """) RETURN n, COLLECT(a) AS a
        """

    elif category == 'Red Foods':
        tags = [135, 1500, 2045, 459, 1144, 2363, 193, 208, 1979]
        tags = ['http://recipedb.com/tag' + str(i) for i in tags]
        tags = '[\'' + '\', \''.join(tags) + '\']'
        query = """
        MATCH (a:ns0__Author)<-[:sch__author]-(n:sch__Recipe)-[:sch__tags]->(t:ns0__RecipeTag)
        WHERE (t.uri IN """ + tags + """) RETURN n, COLLECT(a) AS a
        """

    elif category == 'Cheesey':
        tags = [701, 805, 2302, 959, 190, 970, 1403, 456, 1594, 1790, 613, 1367, 1118, 2453, 1233, 1497, 1641,
                1624, 1483, 992, 1782, 1677, 19, 556, 1370]
        tags = ['http://recipedb.com/tag' + str(i) for i in tags]
        tags = '[\'' + '\', \''.join(tags) + '\']'
        query = """
                MATCH (a:ns0__Author)<-[:sch__author]-(n:sch__Recipe)-[:sch__tags]->(t:ns0__RecipeTag)
                WHERE (t.uri IN """ + tags + """) RETURN n, COLLECT(a) AS a
                """

    return recipe_graph.run(query)


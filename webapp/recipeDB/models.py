from py2neo import Graph, Node, Relationship
from datetime import datetime
import os
import uuid

recipe_graph = Graph("bolt://localhost:7687/neo4j", password="recipeDB")

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


def recipes_by_author(author):
    query = """
    MATCH (n:sch__Recipe)-[:sch__author]->(a:ns0__Author),(n)-[:sch__recipeInstructions]->(ins:sch__ItemList), (n)-[:sch__tags]->(t:ns0__RecipeTag),(n)-[:sch__author]->(a:ns0__Author) WHERE a.rdfs__label[0]=\""""+author+"""\" RETURN n,ins,collect(t.rdfs__label[0]) as tags,collect(distinct a.rdfs__label[0]) as authors LIMIT 25
    """

    return recipe_graph.run(query)
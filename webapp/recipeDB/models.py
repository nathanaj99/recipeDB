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

def recipes_by_author(author):
    query = """
    MATCH (n:sch__Recipe)-[:sch__author]->(a:ns0__Author),(n)-[:sch__recipeInstructions]->(ins:sch__ItemList), (n)-[:sch__tags]->(t:ns0__RecipeTag),(n)-[:sch__author]->(a:ns0__Author) WHERE a.rdfs__label[0]=\""""+author+"""\" RETURN n,ins,collect(t.rdfs__label[0]) as tags,collect(distinct a.rdfs__label[0]) as authors LIMIT 25
    """

    return recipe_graph.run(query)
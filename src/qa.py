#import spacy
#import fileinput
import wikipedia
import requests as req
import json
from SPARQLWrapper import SPARQLWrapper, JSON
import re
import warnings
import numpy as np

# Sacar por pantalla tabla de dependencias para una frase (doc)


def imprimirDOC(doc):
    print(f"Frase: {doc.text}")
    print(f"{'Governor':<27} | {'Rel.':<5} | {'Dependant':<27}")
    print(f"{'':-<65}")
    for token in doc:
        print(
            f"{token.head.text:<20}[{token.head.pos_:<5}] | {token.dep_:<5} | {token.text:<20}[{token.pos_:<5}]")


# Sacar por pantalla tabla de dependencias para una frase (doc).
# Formato Markdown
def imprimirMD(doc, type, persona, respuesta):
    print(f"**Frase:** {doc.text}")
    print("```")
    print(f"{'Governor':<27} | {'Rel.':<5} | {'Dependant':<27}")
    print(f"{'':-<65}")
    for token in doc:
        print(
            f"{token.head.text:<20}[{token.head.pos_:<5}] | {token.dep_:<5} | {token.text:<20}[{token.pos_:<5}]")
    print("```")
    print("**Tipo pregunta**: ", type)
    print("**Persona**: ", persona)
    print("**Respuesta**: ", respuesta)
    print("\n---\n")


# Display dependency tree
# TODO works??
# def displayTree(doc):
#     displacy.render(doc, style='dep', jupyter=False, options={'distance': 95})
#     print()


################################################################################
######################################################################
# PERSONA condiciones:

# - PERSONA 1: dep=="quien" Y rel=="nsubj" Y "gov_pos="PROPN"
#   - "¿Quién es ...?"
def condicionPERSONA_1(gov, gov_pos, rel, dep, dep_pos):
    # TODO tolerar falta de ortografía???
    quien = ["quién", "quien", "Quién", "Quien"]
    if dep not in quien:
        return False
    if rel != "nsubj":
        return False
    if gov_pos != "PROPN":
        return False
    return "PERSONA_1"  # TODO cambiar esto a constante, otra manera?


# Lista de condiciones PERSONA
condicionesPERSONA = [condicionPERSONA_1]

# Determinar Pregunta PERSONA


def esPreguntaPERSONA(doc):
    esPERSONA = False
    for token in doc:
        for condicion in condicionesPERSONA:
            type = condicion(gov=token.head.text, gov_pos=token.head.pos_,
                             rel=token.dep_, dep=token.text, dep_pos=token.pos_)
            if type != False:
                return type
    return False
######################################################################


######################################################################
# NACIMIENTO condiciones:
# - NACIMIENTO 1: dep~="donde" Y rel=="obl" Y gov="nació"
#   - "Dónde nació ...?"
def condicionNACIMIENTO_1(gov, rel, dep):
    # TODO tolerar falta de ortografía???
    donde = ["dónde", "donde", "Dónde", "Donde"]
    if dep not in donde:
        return False
    if rel != "obl":
        return False
    if gov != "nació":  # TODO no acepta falta de tilde. nacio.rel='compound'?
        return False
    return "NACIMIENTO_1"  # TODO cambiar esto a constante, otra manera?

# Lista de condiciones NACIMIENTO
condicionesNACIMIENTO = [condicionNACIMIENTO_1]

# Determinar Pregunta NACIMIENTO
def esPreguntaNACIMIENTO(doc):
    esNACIMIENTO = False
    for token in doc:
        for condicion in condicionesNACIMIENTO:
            type = condicion(gov=token.head.text,
                             rel=token.dep_, dep=token.text)
            if type != False:
                return type
    return False
######################################################################


######################################################################
listaPreguntas = [esPreguntaNACIMIENTO, esPreguntaPERSONA]


def encontrarTipoPregunta(doc):
    for pregunta in listaPreguntas:
        type = pregunta(doc)
        if type != False:
            return type
    return False
######################################################################
################################################################################


################################################################################
######################################################################
# Determina quien es la persona sobre la que se pregunta en PERSONA_1
def encontrarROOTPersonaPERSONA_1(doc):
    ROOT = []
    for token in doc:
        if (token.dep_ == "ROOT"
            and token.head.pos_ == "PROPN") or\
            (token.head.text in ROOT
             and token.dep_ == "flat"):
            ROOT.append(token.text)
    return ROOT
######################################################################


######################################################################
# Determina quien es la persona sobre la que se pregunta en PERSONA_1
def encontrarROOTPersonaNACIMIENTO_1(doc):
    ROOT = []
    for token in doc:
        if (token.dep_ == "nsubj"
            and token.pos_ == "PROPN") or\
            (token.head.text in ROOT
             and token.dep_ == "flat"):
            # ''' and token.pos_ == "PROPN" '''): # Por ej, Alex. Graham Bell (campana) lo pilla como diferente a PROPN (ADJ)
            ROOT.append(token.text)
    return ROOT
######################################################################


######################################################################
# Extiende el nombre de la persona
def extenderROOT(doc, ROOT):
    persona = ""
    for token in doc:
        if (token.head.text in ROOT
         and (token.dep_ == "det" or token.dep_ == "case")):
            if persona == "":
                persona = token.text
            else:
                persona = persona + " " + token.text
        elif (token.text in ROOT):
            if persona == "":
                persona = token.text
            else:
                persona = persona + " " + token.text
    return persona

######################################################################


######################################################################
def encontrarPersona(doc, type):
    ROOT = []
    if type == "PERSONA_1":
        ROOT = encontrarROOTPersonaPERSONA_1(doc)
    elif type == "NACIMIENTO_1":
        ROOT = encontrarROOTPersonaNACIMIENTO_1(doc)
        
    if not ROOT:
        return False
    else: 
        persona = extenderROOT(doc, ROOT)
        return persona
######################################################################
################################################################################


################################################################################
######################################################################
def buscarWikipedia(persona):
    warnings.catch_warnings()
    warnings.simplefilter("ignore")
    # Cambiar idioma de wikipedia a Español
    wikipedia.set_lang("es")
    try:
        page = wikipedia.search(persona, results=1)
        # TODO si la pagina no existe
        respuesta = wikipedia.summary(page, sentences=1)
        respuesta = re.sub(r'\[[^\]]*\]', '', respuesta)
        # TODO quitar parentesis a la busqueda: regex o parsing?
        return respuesta
    except (wikipedia.exceptions.DisambiguationError) as e:
        arr = np.array(e.options)
        filter = ( arr != persona)
        respuesta = "\n¿A quien te refieres?\nPosibles opciones:" + np.array2string(arr[filter][0:5])
        return respuesta



######################################################################


######################################################################
def buscarNacimientoDBPedia(persona):
    # DBPedia nombre del recurso, basado en texto persona
    r = req.get("https://lookup.dbpedia.org/api/search",
                params={
                    "query": "{persona}".format(persona=persona),
                    "typeName": "Person",
                    "format": "JSON"
                },
                )
    rjson = r.text
    rdata = json.loads(rjson)
    uri_persona = rdata['docs'][0]['resource'][0]

    # Realizar query SPARQL
    query = "PREFIX dbpedia-owl: <http://dbpedia.org/ontology/> PREFIX dbpedia: <http://dbpedia.org/resource/> SELECT ?PLACE { <%s> dbpedia-owl:birthPlace ?PLACE }" % (
        uri_persona)

    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)
    sparql.setQuery(query)
    results = sparql.query().convert()

    uri_lugar = results["results"]["bindings"][0]["PLACE"]["value"]

    lugar = re.sub(r'http.*/', '', uri_lugar)
    respuesta = re.sub(r'_', ' ', lugar)

    # TODO control de errores
    return respuesta

######################################################################


######################################################################
def responderPregunta(type, persona):
    if type == "PERSONA_1":
        respuesta = buscarWikipedia(persona)
    elif type == "NACIMIENTO_1":
        respuesta = buscarNacimientoDBPedia(persona)
    else:
        respuesta = False
    return respuesta
######################################################################
################################################################################

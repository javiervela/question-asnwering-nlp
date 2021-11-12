import spacy
import qa

################################################################################
# MAIN
phrase = input("Inserta una frase: ")
nlp = spacy.load("es_core_news_lg")
doc = nlp(phrase)
type = qa.encontrarTipoPregunta(doc)
if type == False:
    #qa.imprimirMD(doc, False, False, "No se puede responder a ese tipo de pregunta")
    print("No se puede responder a ese tipo de pregunta")
    exit(1)
persona = qa.encontrarPersona(doc, type)
if persona == False:
    #qa.imprimirMD(doc, type, False, "No se ha podido determinar la persona sobre la que preguntas")
    print("No se ha podido determinar la persona sobre la que preguntas")
    exit(1)
respuesta = qa.responderPregunta(type, persona)
#qa.imprimirMD(doc, type, persona, respuesta)
print("Respuesta: ", respuesta)
################################################################################

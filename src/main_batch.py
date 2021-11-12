import spacy
import qa
nlp = spacy.load("es_core_news_lg")

questions = [f"¿Dónde nació Alexander Graham Bell?",
             f"¿En qué lugar nació Alexander Graham Bell?",
             f"¿Dónde nació Ernesto Guevara?",
             f"¿En qué lugar nació Ernesto Guevara?",
             f"¿Dónde nació Mariano Rajoy?",
             f"¿En qué lugar nació Mariano Rajoy?",
             f"¿Dónde nació Simone de Beauvoir?",
             f"¿En qué lugar nació Simone de Beauvoir?",
             f"¿Dónde nació Judith Butler?",
             f"¿En qué lugar nació Judith Butler?",
             f"¿Dónde nació Ernest Hemingway?",
             f"¿En qué lugar nació Ernest Hemingway?",
             f"¿Dónde nació Sor Juana Inés de la Cruz?",
             f"¿En qué lugar nació Sor Juana Inés de la Cruz?",
             f"¿Quién fue Alexander Graham Bell?",
             f"¿Quién fue Ernesto Guevara?",
             f"¿Quién es Mariano Rajoy?",
             f"¿Quién fue Simone de Beauvoir?",
             f"¿Quién es Judith Butler?",
             f"¿Quién fue Ernest Hemingway?",
             f"¿Quién fue Sor Juana Inés de la Cruz?",
             f"¿Quién es James Hetfield?",
             f"¿Quién es Elon Musk?",
             f"¿Quién fue Nikola Tesla?",
             f"¿quién fue Leonardo Da Vinci?",
             f"¿Quién fue Michelangelo Buonarroti?",
             f"¿Quién fue Rafael Sanzio?",
             f"¿Quién es Jose Luis Rodríguez Zapatero?",
             f"¿Quién fue Alfonsina Storni?",
             f"¿Quién es Carolina Marín?",
             f"¿Quién es Mireia Belmonte? ",
             f"¿Quién fue Mary Shelley?",
             f"¿Quién fue Marie Curie?",
             f"¿Quién es Leila Khaled?",
             f"¿Quién ha apagado la luz?",
             f"¿Quién da de comer a los perros?",
             f"¿Quién es ese?",
             f"¿Quién es el conductor del autobús?",
             f"¿Quién controla a la banda?",
             f"¿Quién fuma cachimba?",
             f"¿Quiénes hicieron la guerra?",
             f"¿Quién fue el portero durante el mundial de fútbol?",
             f"¿Quién es mi padre?",
             f"¿Quién mató a Lincoln?",
             f"¿Quién mató a Kennedy?",
             f"¿Quién es África de las Heras?",
             f"¿Quién es Asia Carrera?",
             f"¿Quién es Dakota Fanning?",
             f"¿Quién fue Salomón?",
             f"¿Quién fue el rey Salomón?",
             f"¿Quién fue Lanzarote?",
             f"¿Quién fue Santiago?",
             f"¿Quién fue el apóstol Santiago?",
             f"¿Quién fue Guadalupe Larriva?",
             f"¿Quién fue Guadalupe Villa?",
             f"¿Quién fue Whitney Houston?",
             f"¿Quién fue Israel Gelfand?",
             f"¿Quién fue Orestes Jordán?",
             f"¿Quién fue Lincoln?",
             f"¿Quién es Orlando Bloom?",
             f"¿Quién es Pedro de la Vega?",
             f"¿Quién es el rey Felipe VI?",
             f"¿Quién fue Sir Lanzarote?",
             f"¿Quién fue Sir Lancelot?",
             f"¿Quién fue Lanzarote del Lago?",
             f"¿Quién es Merlín?",
             f"¿Quién es el mago Merlín?",
             f"¿Quién fue Miguel de Cervantes?",
             f"¿Quién fue el Inca Garcilaso?",
             f"¿Quién fue Garcilaso de la Vega?",
             f"¿Quién fue Bartolomé de las Casas?"]


################################################################################
# MAIN
for phrase in questions:
    doc = nlp(phrase)
    type = qa.encontrarTipoPregunta(doc)
    if type == False:
        qa.imprimirMD(doc, False, False,
                      "No se puede responder a ese tipo de pregunta")
        continue
    persona = qa.encontrarPersona(doc, type)
    if persona == False:
        qa.imprimirMD(
            doc, type, False, "No se ha podido determinar la persona sobre la que preguntas")
        continue
    respuesta = qa.responderPregunta(type, persona)
    qa.imprimirMD(doc, type, persona, respuesta)
################################################################################


# POS tagging: https://universaldependencies.org/docs/u/pos/
# https://ashutoshtripathi.com/2020/04/13/parts-of-speech-tagging-and-dependency-parsing-using-spacy-nlp/
# https://universaldependencies.org/

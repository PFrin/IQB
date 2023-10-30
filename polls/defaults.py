from django.db import models

DEFAULT_IS_OBLIGATORY = False
DEFAULT_QUESTION_DEFAULTS = {
    'choix multiple': {
        'title': "Nouvelle question choix multiple",
        'isObligatory': DEFAULT_IS_OBLIGATORY,
        'nbrAnswerMin': 1,
        'nbrAnswerMax': 2 #nbr answer de la question
    },
    'Choix unique': {
        'title': "Nouvelle question choix unique",
        'isObligatory': DEFAULT_IS_OBLIGATORY,
        'nbrAnswerMin': 1,
        'nbrAnswerMax': 1
    },
    'question ouverte': {
        'title': "Nouvelle question ouverte",
        'isObligatory': DEFAULT_IS_OBLIGATORY,
        'nbrAnswerMin': 1,
        'nbrAnswerMax': 1
    },
    'Question à échelle': {
        'title': "Comment etes vous satisfait ? ",
        'isObligatory': DEFAULT_IS_OBLIGATORY,
        'nbrAnswerMin': 1,
        'nbrAnswerMax': 1
    },
}
DEFAULT_RESPONSE_DEFAULTS = {
    'choix multiple': {
        'responses': ['Réponse 1', 'Réponse 2']
    },
    'Choix unique': {
        'responses': ['Réponse 1', 'Réponse 2']
    },
    'Question à échelle': {
        'responses': ['Satisfait', 'Moyenement satisfait', 'Pas satisfait']
    }, 
}
DEFAULT_MAX_ANSWERS =  "réponse"
DEFAULT_MAX_ANSWERS = 1
DEFAULT_MIN_ANSWERS = 1

NUMBER_MAX_FORM     = 100
NUMBER_MAX_QUESTION = 50
NUMBER_MAX_ANSWER   = 50

DEFAULT_QUESTION_TYPE = 'Choix unique'
QUESTION_TYPES = [
    "choix multiple",
    "Choix unique",
    "question ouverte",
    "Question à échelle",
]

DEFAULT_FORM_DEFAULTS = {
    'titleForm': "Nouveau formulaire",
    'introText': "Bienvenue sur notre formulaire.",
    'concludingText': "Merci d'avoir rempli notre formulaire.",
}

#####################
#   ERROR MESSAGE   #
#####################

ERROR_MIN_ANSWER_INVALID = "Le nombre minimal de réponses doit être supérieur ou égal à 1."
ERROR_MIN_ANSWER_EXCEEDED_TOTAL = "Le nombre minimal de réponses ne peut pas dépasser le nombre total de réponses de la question."
ERROR_MAX_ANSWER_INVALID = "Le nombre maximal de réponses doit être supérieur ou égal au nombre minimal de réponses."
ERROR_MAX_ANSWER_EXCEEDED_TOTAL = "Le nombre maximal de réponses ne peut pas dépasser le nombre total de réponses de la question."

STATIC_URL_STYLE = '/static/IQB/css/'
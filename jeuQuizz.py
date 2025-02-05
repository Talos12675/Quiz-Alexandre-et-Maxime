# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 18:01:22 2023

@author: SOPHIE
"""

import json
import random

def charger_config():
    with open('quiz_config.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def selectionner_questions(config):
    toutes_questions = config['questions']
    nombre_questions = min(config['nombre_questions'], len(toutes_questions))
    return random.sample(toutes_questions, nombre_questions)

def afficher_question(question, numero):
    print(f"\nQuestion {numero}:")
    print(question['question'])
    for i, reponse in enumerate(question['reponses'], 1):
        print(f"{i}. {reponse}")
    return input("\nVotre réponse (entrez uniquement le numéro 1, 2, 3 ou 4): ")

def quiz(questions_selectionnees):
    points = 0
    resultats = []  # Liste pour stocker les résultats
    for i, question in enumerate(questions_selectionnees, 1):
        reponse_utilisateur = afficher_question(question, i)
        try:
            index_reponse = int(reponse_utilisateur) - 1
            reponse_donnee = question['reponses'][index_reponse]
            est_correct = reponse_donnee.lower() == question['reponse_correcte'].lower()
            if est_correct:
                points += 1
                print("Vous avez répondu juste.")
            else:
                print("La bonne réponse était \"{}\".".format(question['reponse_correcte']))
            # Stocker le résultat
            resultats.append({
                'question': question['question'],
                'correct': est_correct,
                'reponse_donnee': reponse_donnee,
                'reponse_correcte': question['reponse_correcte']
            })
        except (ValueError, IndexError):
            print("Réponse invalide. La bonne réponse était \"{}\".".format(question['reponse_correcte']))
            resultats.append({
                'question': question['question'],
                'correct': False,
                'reponse_donnee': "Réponse invalide",
                'reponse_correcte': question['reponse_correcte']
            })
    
    # Afficher le récapitulatif
    print("\n=== Récapitulatif de vos réponses ===")
    for i, resultat in enumerate(resultats, 1):
        statut = "✓ Correct" if resultat['correct'] else "✗ Incorrect"
        print(f"\nQuestion {i}: {resultat['question']}")
        print(f"Votre réponse : {resultat['reponse_donnee']}")
        if not resultat['correct']:
            print(f"Bonne réponse : {resultat['reponse_correcte']}")
        print(f"Statut : {statut}")
    
    # Calculer le pourcentage de réussite
    pourcentage = (points / len(questions_selectionnees)) * 100
    
    # Déterminer le niveau de réussite
    message = ""
    if pourcentage == 100:
        message = "Parfait ! Vous êtes un expert !"
    elif pourcentage >= 75:
        message = "Excellent ! Vous avez de très bonnes connaissances !"
    elif pourcentage >= 50:
        message = "Bravo ! Continuez comme ça !"
    else:
        message = "Dommage ! Révisez vos cours !"
    
    return points, pourcentage, message

def main():
    while True:
        print("*** Début du Quiz ***\n")
        nom = input("Entrez votre nom: ").title()
        print()

        try:
            config = charger_config()
            questions_selectionnees = selectionner_questions(config)
            points, pourcentage, message = quiz(questions_selectionnees)
            print("\n----------------------------------------")
            print("Vous avez repondu juste à {1} des {2} questions de ce quiz.".format(
                nom, points, len(questions_selectionnees)))
            print(f"Pourcentage de réussite : {pourcentage:.1f}%")
            print(message)
            
            # Demander si l'utilisateur veut rejouer
            rejouer = input("\nVoulez-vous rejouer ? (oui/non): ").lower()
            if rejouer != 'oui':
                print("\nMerci d'avoir joué ! À bientôt !")
                break

        except FileNotFoundError:
            print("Erreur: Le fichier de configuration n'a pas été trouvé.")
            break
        except json.JSONDecodeError:
            print("Erreur: Le fichier de configuration est mal formaté.")
            break
        except Exception as e:
            print(f"Une erreur inattendue s'est produite: {str(e)}")
            break

if __name__ == "__main__":
    main()
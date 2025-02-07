# Programme de quiz pour réviser
import json
import random

def lire_fichier_questions():
    with open('quiz_config.json', 'r', encoding='utf-8') as fichier:
        return json.load(fichier)

def poser_question_simple(question):
    print("\nQuestion:", question['question'])
    
    # On prend la bonne réponse et 2 mauvaises au hasard
    mauvaises_reponses = []
    for reponse in question['reponses_possibles']:
        if reponse != question['reponse_correcte']:
            mauvaises_reponses.append(reponse)
    
    # On mélange 2 mauvaises réponses avec la bonne
    reponses_a_afficher = random.sample(mauvaises_reponses, 2)
    reponses_a_afficher.append(question['reponse_correcte'])
    random.shuffle(reponses_a_afficher)
    
    # On affiche les 3 choix
    for i in range(3):
        print(f"{i+1}. {reponses_a_afficher[i]}")
    
    # L'utilisateur choisit une réponse
    choix = input("\nTa réponse (1, 2 ou 3): ")
    
    # On vérifie si c'est la bonne réponse
    if choix in ['1', '2', '3']:
        reponse_choisie = reponses_a_afficher[int(choix)-1]
        return reponse_choisie
    return "Réponse invalide"

def poser_question_multiple(question):
    print("\nQuestion:", question['question'])
    
    # On prend toutes les bonnes réponses
    reponses_a_afficher = question['reponses_correctes'].copy()
    
    # On ajoute des mauvaises réponses pour compléter
    nb_reponses_total = question['nombre_reponses_a_afficher']
    nb_mauvaises_reponses = nb_reponses_total - len(reponses_a_afficher)
    
    # On cherche les mauvaises réponses possibles
    mauvaises_reponses = []
    for reponse in question['reponses_possibles']:
        if reponse not in question['reponses_correctes']:
            mauvaises_reponses.append(reponse)
    
    # On ajoute le bon nombre de mauvaises réponses
    reponses_a_afficher.extend(random.sample(mauvaises_reponses, nb_mauvaises_reponses))
    random.shuffle(reponses_a_afficher)
    
    # On affiche tous les choix
    for i in range(len(reponses_a_afficher)):
        print(f"{i+1}. {reponses_a_afficher[i]}")
    
    print("\nEntrez les numéros des bonnes réponses, séparés par des espaces")
    choix = input(f"Vos réponses (1 à {nb_reponses_total}): ")
    
    # On transforme la réponse en liste de réponses
    try:
        numeros_choisis = [int(x) for x in choix.split()]
        reponses_choisies = []
        for num in numeros_choisis:
            if 1 <= num <= nb_reponses_total:
                reponses_choisies.append(reponses_a_afficher[num-1])
        return reponses_choisies
    except:
        return "Réponse invalide"

def jouer():
    print("=== QUIZ DE RÉVISION ===")
    nom = input("\nComment tu t'appelles ? ")
    print(f"Salut {nom} ! C'est parti !")
    
    try:
        # On charge les questions
        questions = lire_fichier_questions()['questions']
        
        # On prend 5 questions au hasard
        questions_quiz = random.sample(questions, 5)
        
        score = 0
        reponses_joueur = []
        
        # On pose les 5 questions
        for numero, question in enumerate(questions_quiz, 1):
            if question['type'] == 'simple':
                reponse = poser_question_simple(question)
                if reponse == "Réponse invalide":
                    print("Réponse invalide !")
                    reussi = False
                else:
                    reussi = (reponse == question['reponse_correcte'])
                    if reussi:
                        print("Bien joué !")
                        score += 1
                    else:
                        print(f"Dommage ! La bonne réponse était: {question['reponse_correcte']}")
            else:
                reponse = poser_question_multiple(question)
                if reponse == "Réponse invalide":
                    print("Réponse invalide !")
                    reussi = False
                else:
                    reussi = (sorted(reponse) == sorted(question['reponses_correctes']))
                    if reussi:
                        print("Bien joué ! Tu as trouvé toutes les bonnes réponses !")
                        score += 1
                    else:
                        print("Dommage ! Les bonnes réponses étaient:", ", ".join(question['reponses_correctes']))
            
            # On garde la réponse pour le résumé
            reponses_joueur.append({
                'question': question['question'],
                'reponse': reponse,
                'reussi': reussi,
                'correction': question['reponse_correcte'] if question['type'] == 'simple' else question['reponses_correctes']
            })
        
        # On affiche le résumé
        print("\n=== TES RÉSULTATS ===")
        for i, rep in enumerate(reponses_joueur, 1):
            print(f"\nQuestion {i}: {rep['question']}")
            if isinstance(rep['reponse'], list):
                print(f"Ta réponse: {', '.join(rep['reponse'])}")
            else:
                print(f"Ta réponse: {rep['reponse']}")
            if not rep['reussi']:
                if isinstance(rep['correction'], list):
                    print(f"Bonnes réponses: {', '.join(rep['correction'])}")
                else:
                    print(f"Bonne réponse: {rep['correction']}")
        
        # Score final
        print(f"\nTon score: {score}/5 ({score*20}%)")
        
        if score == 5:
            print("T'es trop fort !")
        elif score >= 3:
            print("Pas mal du tout !")
        else:
            print("Continue de réviser, tu vas y arriver !")
        
        # On propose de rejouer
        if input("\nTu veux rejouer ? (oui/non): ") == "oui":
            jouer()
        else:
            print("\nÀ bientôt !")
            
    except:
        print("Il y a eu un problème avec le fichier de questions...")

# On lance le jeu
if __name__ == "__main__":
    jouer()

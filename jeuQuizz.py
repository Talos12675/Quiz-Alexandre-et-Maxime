# Mon quiz pour réviser
import json
import random

def charger_questions():
    fichier = open('quiz_config.json', 'r', encoding='utf-8')
    donnees = json.load(fichier)
    fichier.close()
    return donnees

def poser_question_simple(question):
    print("\nQuestion:", question['question'])
    
    # Afficher si un indice est disponible
    if 'indice' in question:
        print("(Tu peux demander un indice en tapant 'indice')")
    
    # Liste pour stocker les réponses
    reponses = []
    bonne_reponse = question['reponse_correcte']
    
    # Je récupère les mauvaises réponses
    for reponse in question['reponses_possibles']:
        if reponse != bonne_reponse:
            reponses.append(reponse)
    
    # Je garde que 2 mauvaises réponses
    reponses = reponses[:2]
    # Je rajoute la bonne
    reponses.append(bonne_reponse)
    # Je mélange
    random.shuffle(reponses)
    
    # Affichage des choix
    print("1.", reponses[0])
    print("2.", reponses[1])
    print("3.", reponses[2])
    
    while True:
        # Réponse du joueur
        reponse = input("\nTa réponse (1, 2 ou 3): ").lower()
        
        # Gestion de l'indice
        if reponse == "indice":
            if 'indice' in question:
                print("\nIndice:", question['indice'])
                print("\n1.", reponses[0])
                print("2.", reponses[1])
                print("3.", reponses[2])
                continue
            else:
                print("Désolé, il n'y a pas d'indice pour cette question.")
                continue
        
        # Vérification
        if reponse in ["1", "2", "3"]:
            return reponses[int(reponse)-1]
        else:
            return "J'ai pas compris..."

def poser_question_multiple(question):
    print("\nQuestion:", question['question'])
    
    # Afficher si un indice est disponible
    if 'indice' in question:
        print("(Tu peux demander un indice en tapant 'indice')")
    
    # Préparation
    bonnes_reponses = question['reponses_correctes'].copy()
    nb_reponses_total = question['nombre_reponses_a_afficher']
    
    # Calcul des mauvaises réponses à ajouter
    nb_mauvaises_reponses = nb_reponses_total - len(bonnes_reponses)
    
    # Liste des mauvaises réponses
    mauvaises_reponses = []
    for reponse in question['reponses_possibles']:
        if reponse not in bonnes_reponses:
            mauvaises_reponses.append(reponse)
    
    # Je garde le bon nombre
    mauvaises_reponses = mauvaises_reponses[:nb_mauvaises_reponses]
    
    # Mélange final
    toutes_reponses = bonnes_reponses + mauvaises_reponses
    random.shuffle(toutes_reponses)
    
    # Affichage
    for i in range(len(toutes_reponses)):
        print(f"{i+1}. {toutes_reponses[i]}")
    
    while True:
        print("\nDonne les numéros des bonnes réponses avec des espaces entre")
        reponse = input(f"Tes réponses (entre 1 et {nb_reponses_total}): ").lower()
        
        # Gestion de l'indice
        if reponse == "indice":
            if 'indice' in question:
                print("\nIndice:", question['indice'])
                for i in range(len(toutes_reponses)):
                    print(f"{i+1}. {toutes_reponses[i]}")
                continue
            else:
                print("Désolé, il n'y a pas d'indice pour cette question.")
                continue
                
        # Vérification des réponses
        try:
            numeros = reponse.split()
            reponses_choisies = []
            for num in numeros:
                num = int(num)
                if num >= 1 and num <= nb_reponses_total:
                    reponses_choisies.append(toutes_reponses[num-1])
            return reponses_choisies
        except:
            return "J'ai pas compris..."

def lancer_quiz(quiz):
    try:
        # 5 questions max
        questions = quiz['questions']
        if len(questions) > 5:
            questions = random.sample(questions, 5)
        
        points = 0
        historique = []
        
        print(f"\n=== {quiz['titre'].upper()} ===")
        print(quiz['description'])
        
        # Boucle des questions
        for i, question in enumerate(questions):
            if question['type'] == 'simple':
                reponse = poser_question_simple(question)
                if reponse == "J'ai pas compris...":
                    print("Je n'ai pas compris ta réponse!")
                    reussite = False
                else:
                    if reponse == question['reponse_correcte']:
                        print("Bravo !")
                        points += 1
                        reussite = True
                    else:
                        print(f"Dommage... La bonne réponse était: {question['reponse_correcte']}")
                        reussite = False
            else:
                reponse = poser_question_multiple(question)
                if reponse == "J'ai pas compris...":
                    print("Je n'ai pas compris ta réponse!")
                    reussite = False
                else:
                    # Comparaison des réponses
                    reponse.sort()
                    bonnes = question['reponses_correctes'].copy()
                    bonnes.sort()
                    if reponse == bonnes:
                        print("Bravo ! Tu as tout trouvé !")
                        points += 1
                        reussite = True
                    else:
                        print("Dommage... Les bonnes réponses étaient:", ", ".join(question['reponses_correctes']))
                        reussite = False
            
            # Sauvegarde pour le récap
            historique.append({
                'question': question['question'],
                'reponse': reponse,
                'reussite': reussite,
                'correction': question['reponse_correcte'] if question['type'] == 'simple' else question['reponses_correctes']
            })
        
        # Récap final
        print("\n=== RÉCAP DE TES RÉPONSES ===")
        for i, rep in enumerate(historique):
            print(f"\nQuestion {i+1}: {rep['question']}")
            if type(rep['reponse']) == list:
                print(f"Tu as répondu: {', '.join(rep['reponse'])}")
            else:
                print(f"Tu as répondu: {rep['reponse']}")
            if not rep['reussite']:
                if type(rep['correction']) == list:
                    print(f"Il fallait répondre: {', '.join(rep['correction'])}")
                else:
                    print(f"Il fallait répondre: {rep['correction']}")
        
        # Note
        print(f"\nTa note: {points}/{len(questions)} ({points*20}%)")
        
        if points == len(questions):
            print("T'es trop fort !")
        elif points >= len(questions)/2:
            print("Pas mal du tout !")
        else:
            print("Continue de réviser, tu vas y arriver !")
        
        # Suite du jeu
        donnees = charger_questions()
        return fin_quiz(quiz, donnees['quiz_list'])
        
    except Exception as e:
        print(f"Oups, y'a eu un bug: {str(e)}")
        return False

def fin_quiz(quiz_actuel, liste_quiz):
    while True:
        choix = input("\nTu veux :\n1. Refaire ce quiz\n2. Essayer un autre quiz\n3. Arrêter\nTon choix (1-3): ")
        if choix == "1":
            return lancer_quiz(quiz_actuel)
        elif choix == "2":
            nouveau_quiz = choisir_quiz(liste_quiz)
            return lancer_quiz(nouveau_quiz)
        elif choix == "3":
            print("\nA plus !")
            return False
        print("Je n'ai pas compris ton choix...")

def choisir_quiz(liste_quiz):
    print("\n=== CHOISIS TON QUIZ ===")
    for i, quiz in enumerate(liste_quiz, 1):
        print(f"{i}. {quiz['titre']} - {quiz['description']}")
    
    while True:
        try:
            choix = int(input("\nQuel quiz tu veux faire ? (donne le numéro): "))
            if 1 <= choix <= len(liste_quiz):
                return liste_quiz[choix-1]
        except ValueError:
            pass
        print("Je n'ai pas compris ton choix...")

def demarrer_jeu():
    print("=== QUIZ DE RÉVISION ===")
    nom = input("\nSalut ! Comment tu t'appelles ? ")
    print(f"Cool {nom}, on commence !")
    
    try:
        donnees = charger_questions()
        quiz_choisi = choisir_quiz(donnees['quiz_list'])
        return lancer_quiz(quiz_choisi)
    except Exception as e:
        print(f"Oups, il y a eu un problème: {str(e)}")
        return False

# On lance le jeu
if __name__ == "__main__":
    demarrer_jeu()
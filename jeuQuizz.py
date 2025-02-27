# Programme de quiz pour réviser
import json
import random

def charger_questions():
    with open('quiz_config.json', 'r', encoding='utf-8') as fichier:
        return json.load(fichier)

def poser_question_simple(question):
    print("\nQuestion:", question['question'])
    
    # On prend des réponses au hasard
    mauvaises_reponses = []
    bonne_reponse = question['reponse_correcte']
    
    # On fait la liste des mauvaises réponses
    for reponse in question['reponses_possibles']:
        if reponse != bonne_reponse:
            mauvaises_reponses.append(reponse)
    
    # On mélange tout
    reponses_melangees = random.sample(mauvaises_reponses, 2)
    reponses_melangees.append(bonne_reponse)
    random.shuffle(reponses_melangees)
    
    # On montre les choix
    for i in range(3):
        print(f"{i+1}. {reponses_melangees[i]}")
    
    # On demande la réponse
    reponse_utilisateur = input("\nTa réponse (1, 2 ou 3): ")
    
    # On vérifie
    if reponse_utilisateur in ['1', '2', '3']:
        choix = reponses_melangees[int(reponse_utilisateur)-1]
        return choix
    return "Pas compris ta réponse..."

def poser_question_multiple(question):
    print("\nQuestion:", question['question'])
    
    # On prépare les réponses
    bonnes_reponses = question['reponses_correctes'].copy()
    nb_total_reponses = question['nombre_reponses_a_afficher']
    
    # On cherche combien de mauvaises réponses on doit ajouter
    nb_mauvaises_reponses = nb_total_reponses - len(bonnes_reponses)
    
    # On fait la liste des mauvaises réponses possibles
    mauvaises_reponses = []
    for reponse in question['reponses_possibles']:
        if reponse not in bonnes_reponses:
            mauvaises_reponses.append(reponse)
    
    # On mélange tout
    toutes_reponses = bonnes_reponses + random.sample(mauvaises_reponses, nb_mauvaises_reponses)
    random.shuffle(toutes_reponses)
    
    # On montre les choix
    for i in range(len(toutes_reponses)):
        print(f"{i+1}. {toutes_reponses[i]}")
    
    print("\nDonne les numéros des bonnes réponses avec des espaces entre")
    reponse_utilisateur = input(f"Tes réponses (entre 1 et {nb_total_reponses}): ")
    
    # On regarde ce que l'utilisateur a choisi
    try:
        numeros_choisis = [int(x) for x in reponse_utilisateur.split()]
        reponses_choisies = []
        for num in numeros_choisis:
            if 1 <= num <= nb_total_reponses:
                reponses_choisies.append(toutes_reponses[num-1])
        return reponses_choisies
    except:
        return "Pas compris ta réponse..."

def lancer_quiz(quiz):
    try:
        questions = quiz['questions']
        nb_questions = min(5, len(questions))
        questions_du_quiz = random.sample(questions, nb_questions)
        
        points = 0
        historique = []
        
        print(f"\n=== {quiz['titre'].upper()} ===")
        print(quiz['description'])
        
        # On pose les questions une par une
        for num, question in enumerate(questions_du_quiz, 1):
            if question['type'] == 'simple':
                reponse = poser_question_simple(question)
                if reponse == "Pas compris ta réponse...":
                    print("Je n'ai pas compris ta réponse!")
                    reussite = False
                else:
                    reussite = (reponse == question['reponse_correcte'])
                    if reussite:
                        print("Super !")
                        points += 1
                    else:
                        print(f"Raté... La bonne réponse était: {question['reponse_correcte']}")
            else:
                reponse = poser_question_multiple(question)
                if reponse == "Pas compris ta réponse...":
                    print("Je n'ai pas compris ta réponse!")
                    reussite = False
                else:
                    reussite = (sorted(reponse) == sorted(question['reponses_correctes']))
                    if reussite:
                        print("Super ! Tu as tout trouvé !")
                        points += 1
                    else:
                        print("Raté... Les bonnes réponses étaient:", ", ".join(question['reponses_correctes']))
            
            # On garde en mémoire pour le récap
            historique.append({
                'question': question['question'],
                'reponse': reponse,
                'reussite': reussite,
                'correction': question['reponse_correcte'] if question['type'] == 'simple' else question['reponses_correctes']
            })
        
        # Le récap
        print("\n=== RÉCAP DE TES RÉPONSES ===")
        for i, rep in enumerate(historique, 1):
            print(f"\nQuestion {i}: {rep['question']}")
            if isinstance(rep['reponse'], list):
                print(f"Tu as répondu: {', '.join(rep['reponse'])}")
            else:
                print(f"Tu as répondu: {rep['reponse']}")
            if not rep['reussite']:
                if isinstance(rep['correction'], list):
                    print(f"Il fallait répondre: {', '.join(rep['correction'])}")
                else:
                    print(f"Il fallait répondre: {rep['correction']}")
        
        # Note finale
        print(f"\nTa note: {points}/{nb_questions} ({points*20}%)")
        
        if points == nb_questions:
            print("Parfait !")
        elif points >= nb_questions/2:
            print("Bien joué !")
        else:
            print("Courage, continue de réviser !")
        
        # On propose de continuer
        donnees = charger_questions()
        return fin_quiz(quiz, donnees['quiz_list'])
        
    except Exception as e:
        print(f"Oups, il y a eu un problème: {str(e)}")
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
# Mon super quiz pour réviser!!
import json
import random

def lire_fichier():
    with open('quiz_config.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def question_simple(q):
    print("\nQuestion:", q['question'])
    
    # Je mets la bonne réponse de côté
    bonne_rep = q['reponse_correcte']
    autres_rep = []
    
    # Je prends les mauvaises réponses
    for r in q['reponses_possibles']:
        if r != bonne_rep:
            autres_rep.append(r)
    
    # Je mélange tout
    rep_a_montrer = random.sample(autres_rep, 2)
    rep_a_montrer.append(bonne_rep)
    random.shuffle(rep_a_montrer)
    
    # J'affiche les réponses
    for i in range(3):
        print(f"{i+1}. {rep_a_montrer[i]}")
    
    # Je propose l'indice si y'en a un
    if 'indice' in q:
        print("\nTu veux un indice? Tape 'i'. Sinon, donne ta réponse!")
    
    # Je demande la réponse
    rep = input("\nTa réponse (1, 2 ou 3): ")
    
    # Si l'utilisateur veut l'indice
    if rep.lower() == 'i' and 'indice' in q:
        print(f"\nIndice: {q['indice']}")
        rep = input("Maintenant donne ta réponse (1, 2 ou 3): ")
    
    # Je vérifie si c'est bon
    if rep in ['1', '2', '3']:
        choix = rep_a_montrer[int(rep)-1]
        return choix
    return "J'ai pas compris..."

def question_multiple(q):
    print("\nQuestion:", q['question'])
    
    bonnes_rep = q['reponses_correctes'].copy()
    nb_rep_total = q['nombre_reponses_a_afficher']
    
    # Je calcule combien de mauvaises réponses je dois mettre
    nb_mauvaises = nb_rep_total - len(bonnes_rep)
    
    # Je fais la liste des mauvaises réponses
    mauvaises_rep = []
    for r in q['reponses_possibles']:
        if r not in bonnes_rep:
            mauvaises_rep.append(r)
    
    # Je mélange tout
    toutes_rep = bonnes_rep + random.sample(mauvaises_rep, nb_mauvaises)
    random.shuffle(toutes_rep)
    
    # J'affiche les choix
    for i in range(len(toutes_rep)):
        print(f"{i+1}. {toutes_rep[i]}")
    
    # Je propose l'indice si y'en a un
    if 'indice' in q:
        print("\nTu veux un indice? Tape 'i'. Sinon, donne ta réponse!")
    
    print("\nDonne les numéros des bonnes réponses avec des espaces")
    rep = input(f"Tes réponses (entre 1 et {nb_rep_total}): ")
    
    # Si l'utilisateur veut l'indice
    if rep.lower() == 'i' and 'indice' in q:
        print(f"\nIndice: {q['indice']}")
        rep = input(f"Maintenant donne tes réponses (entre 1 et {nb_rep_total}): ")
    
    # Je regarde ce que l'utilisateur a mis
    try:
        numeros = [int(x) for x in rep.split()]
        reponses = []
        for n in numeros:
            if 1 <= n <= nb_rep_total:
                reponses.append(toutes_rep[n-1])
        return reponses
    except:
        return "J'ai pas compris..."

def faire_quiz(quiz):
    try:
        # Je prends 5 questions au hasard
        mes_questions = random.sample(quiz['questions'], 5)
        score = 0
        reponses = []
        
        print(f"\n=== {quiz['titre'].upper()} ===")
        print(quiz['description'])
        
        # Je pose les questions
        for num, q in enumerate(mes_questions, 1):
            if q['type'] == 'simple':
                rep = question_simple(q)
                if rep == "J'ai pas compris...":
                    print("Je comprends pas ce que tu as écrit!")
                    ok = False
                else:
                    ok = (rep == q['reponse_correcte'])
                    if ok:
                        print("Bravo!!")
                        score += 1
                    else:
                        print(f"Raté... Fallait répondre: {q['reponse_correcte']}")
            else:
                rep = question_multiple(q)
                if rep == "J'ai pas compris...":
                    print("Je comprends pas ce que tu as écrit!")
                    ok = False
                else:
                    ok = (sorted(rep) == sorted(q['reponses_correctes']))
                    if ok:
                        print("Trop fort! T'as tout trouvé!")
                        score += 1
                    else:
                        print("Raté... Les bonnes réponses étaient:", ", ".join(q['reponses_correctes']))
            
            # Je garde en mémoire pour après
            reponses.append({
                'question': q['question'],
                'reponse': rep,
                'ok': ok,
                'correction': q['reponse_correcte'] if q['type'] == 'simple' else q['reponses_correctes']
            })
        
        # Je fais un récap
        print("\n=== CE QUE TU AS RÉPONDU ===")
        for i, r in enumerate(reponses, 1):
            print(f"\nQuestion {i}: {r['question']}")
            if isinstance(r['reponse'], list):
                print(f"T'as répondu: {', '.join(r['reponse'])}")
            else:
                print(f"T'as répondu: {r['reponse']}")
            if not r['ok']:
                if isinstance(r['correction'], list):
                    print(f"Fallait répondre: {', '.join(r['correction'])}")
                else:
                    print(f"Fallait répondre: {r['correction']}")
        
        # Je mets la note
        print(f"\nTa note: {score}/5 ({score*20}%)")
        
        if score == 5:
            print("T'es trop fort!!")
        elif score >= 3:
            print("Pas mal du tout!")
        else:
            print("Allez, faut réviser encore un peu!")
        
        # Je propose de continuer
        donnees = lire_fichier()
        return fin_du_quiz(quiz, donnees['quiz_list'])
        
    except Exception as e:
        print(f"Oups y'a un bug: {str(e)}")
        return False

def fin_du_quiz(quiz_actuel, liste_quiz):
    while True:
        choix = input("\nTu veux :\n1. Refaire ce quiz\n2. Essayer un autre quiz\n3. Arrêter\nTon choix (1-3): ")
        if choix == "1":
            return faire_quiz(quiz_actuel)
        elif choix == "2":
            nouveau_quiz = choisir_quiz(liste_quiz)
            return faire_quiz(nouveau_quiz)
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
        donnees = lire_fichier()
        quiz_choisi = choisir_quiz(donnees['quiz_list'])
        return faire_quiz(quiz_choisi)
    except Exception as e:
        print(f"Oups, il y a eu un problème: {str(e)}")
        return False

# On lance le jeu
if __name__ == "__main__":
    demarrer_jeu()
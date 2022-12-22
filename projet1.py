# Nom : Secundar
# Prénom : Ismael
# Matricule : 504017

import copy, sys

# Complétez les informations sur la fonction
glob_best_cost = -1
glob_best_cost_2 = -1
glob_best_assignments = []
glob_best_assignments_2 = []
glob_indice = 0
glob_debut = False
glob_debut_2 = False
glob_global_centers = []
glob_centers = []

def minimum_travel_cost(demand,capacity,travel_cost):
    global glob_best_cost, glob_best_assignments, glob_indice,glob_debut, glob_assignments


    if glob_debut == False:
        """
        Initialise une liste avec des None au début ( vue que c'est récursif il ne le fera qu'une fois ) d'où la 
        variable debut qui montre qu'on a bien débuté et devient True
        """
        glob_assignments = [None]*len(demand)
        glob_debut = True

    famille = len(travel_cost)                                      # Le nombre de famille peut être déterminé par la
                                                                    # longueur des lignes de travel_cost
    centre = len(travel_cost[0])                                    # Le nombre de centre peut être déterminé par la
                                                                    # longueur des colonnes de travel_cost

    if glob_indice == famille:                                      # liste de centre complet avec famille assignée
        if capacity_check(demand, capacity, glob_assignments):      # si cette liste satisfait la demande et la capacité
            cost_of_assignements = travel_cost_calcul(travel_cost, glob_assignments)    # Calcul les couts de trajets
            if glob_best_cost == -1 or cost_of_assignements < glob_best_cost:
                glob_best_cost = cost_of_assignements               # si le cout de trajet est meilleur on garde ce cout
                glob_best_assignments = copy.copy(glob_assignments) # on garde aussi l'assignments de ce coup

    else:                                                           # sinon on cherche une autre liste d'assignements
        for i in range(centre):
            glob_assignments[glob_indice] = i
            glob_indice += 1                                        # indice change permet d'avoir une autre liste
                                                                    # d'assignments
            minimum_travel_cost(demand, capacity, travel_cost)
            glob_indice -= 1
    return glob_best_cost, glob_best_assignments


def capacity_check(demand,capacity,assignements):
    """
    Fonction qui vérifie si la demande de chaque famille entre dans la capacité de chaque centre,
    Cette fonction permettra d'éliminer les assignments inutiles
    :param demand: Liste qui contient la demande de chaque famille
    :param capacity: Liste qui contient la capacité de chaque centre
    :param assignements: Liste d'affectation des familles aux centres
    :return: True qui la demande de chaque famille est bien dans la capacité de chaque centre
    """

    #demande par famille en focntion du centre assigné

    capacity_current = [i for i in capacity]                # initialise une liste avec la capacité courrante

    for i in range(len(assignements)):

        current_center = assignements[i]
        current_family = demand[i]
        capacity_current[current_center] -= current_family   # soustrait la demande de la famille courante
                                                             # en fonction du centre qui lui a été affecté

        if capacity_current[current_center] < 0 :            # si la demande est plus élevée que la capacité
                                                             # alors l'assignments n'est pas bon

            return False

    return True

def travel_cost_calcul(travel_cost,assignements):
    """
    Fonction qui permet de calculer le cout de trajet de chaque famille en fonction des centres assignés
    :param travel_cost: liste qui contient les couts de trajets de chaque famille/centre
    :param assignements: liste d'affectation des familles aux centres
    :return: le coup total des trajets de chaque famille en fonction du centre qui lui a été assigné
    """
    cost = 0

    for i in range(len(travel_cost)):
        cost += travel_cost[i][assignements[i]]             # additionne le coup de chaque famille
                                                            # en fonction du centre affecté

    return cost

# Complétez les informations sur la fonction

def cost_center(opening_cost,assignments):
    """
    Fonction qui calcule le coup de construction de chaque centre en fonction de la liste d'affectation de chaque
    famille
    :param opening_cost: liste qui contient le cout d'ouverture de chaque centre
    :param assignments: liste d'affectation des familles aux centres
    :return: le coup de construction des centres en fonction des centres qui ont été affecté aux familles
    """
    global glob_global_centers

    cost = 0
    for i in assignments:
        if i not in glob_global_centers:
            glob_global_centers.append(i)
    for i in glob_global_centers:
        cost += opening_cost[i]
    return cost

# Complétez les informations sur la fonction
def facility_location(opening_cost,demand,capacity,travel_cost):
    global glob_best_cost_2, glob_best_assignments_2, glob_indice, glob_debut_2, glob_assignments, glob_global_centers,glob_centers
    if glob_debut_2 == False:
        glob_assignments = [None] * len(demand)
        glob_debut_2 = True

    famille = len(travel_cost)
    centre = len(travel_cost[0])

    if glob_indice == famille:                                  # liste de centre complet avec famille assignée
        if capacity_check(demand, capacity, glob_assignments):
            cost_of_assignements = travel_cost_calcul(travel_cost, glob_assignments) + cost_center(opening_cost,glob_assignments)
                                                                # on ajoute le cout d'ouverture de chaque centre
            if cost_of_assignements < glob_best_cost_2 or glob_best_cost_2 == -1  :

                glob_centers = copy.copy(glob_global_centers)
                glob_best_cost_2 = cost_of_assignements
                glob_best_assignments_2 = copy.copy(glob_assignments)
            glob_global_centers = []

    else:
        for i in range(centre):
            glob_assignments[glob_indice] = i

            glob_indice += 1  # indice change
            facility_location(opening_cost, demand,capacity, travel_cost)
            glob_indice -= 1

    return (glob_best_cost_2,glob_centers,glob_best_assignments_2)

# Fonction retournant les données (opening_cost,travel_cost,demand,capacity) de l'instance file_name dont le fichier doit être situé dans le même dossier
# file_name : String
# return : (opening_cost,travel_cost,demand,capacity)
def read_instance(file_name):
    opening_cost = []
    demand = []
    capacity = []
    travel_cost = []
    try:
        file = open(file_name,'r')
        info = file.readline().split(" ")
        I = int(info[0])
        J = int(info[1])
        info = file.readline().split(" ")
        for j in range(J):
            opening_cost.append(int(info[j]))
        info = file.readline().split(" ")
        for i in range(I):
            demand.append(int(info[i]))
        info = file.readline().split(" ")
        for j in range(J):
            capacity.append(int(info[j]))
        for i in range(I):
            travel_cost.append([])
            info = file.readline().split(" ")
            for j in range(J):
                travel_cost[i].append(round(float(info[j])))
    except:
        print("Erreur lors de la lecture des données, vérifiez que le fichier de l'instance est dans le même dossier que ce fichier")
    return opening_cost,demand,capacity,travel_cost

# Résolution du FLP sur l'instance passée en ligne de commande
if __name__ == "__main__":
  if len(sys.argv) == 2:
    opening_cost,demand,capacity,travel_cost = read_instance(sys.argv[1])
    print("Instance : {}".format(sys.argv[1]))
    print("Opening costs : {}".format(opening_cost))
    print("Demand : {}".format(demand))
    print("Capacity : {}".format(capacity))
    print("Traval costs : {}".format(travel_cost))
    print("Résultats : {}".format(facility_location(opening_cost,demand,capacity,travel_cost)))
  else :
    print("Veillez fournir un nom d'instance")
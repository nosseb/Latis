import io           # Nécessaire car le fichier est encodé en 'utf-16-le'
import xmltodict    # Pour lire facillement le fichier xml

def netoyage(texte :str):
    # Le fihier ne respecte pas totalement la norme xml
    # La première partie (qui nous intéresse) est valide
    # On va donc l'extraire

    pos = texte.find("</BLOC-COURBES>")
    return texte[0:pos+15]


def decoupe(table):
    # Découpe des chaînes de caractères en mots de 16 caractères
    pass


def convertion(table):
    # Renvoie une vouvelle table avec des float au lieux de str
    # struct.unpack('d', binascii.unhexify("3F5205BC01A36E2F"))
    pass


def extract(path: str) :
    # En théorie retourne une liste de listes de liste de valeurs:
    # Chaque courbe latis pro contient deux listes de valeurs, une pour x et une pour y
    # Il y a potentiellement plusieurs courbes dans le fichier
    
    with io.open(path, 'r', encoding='utf-16-le') as file:    # Chargement du fichier
        content = netoyage(file.read())

        doc = xmltodict.parse(content)

        nb_courbes = int(doc["BLOC-COURBES"]["LESCOURBES"]["C"]["@Nb"])

        table_string = []

        # Récupération des chaines exadécimales
        for i in range(nb_courbes) :
            table_string.append([ doc["BLOC-COURBES"]["LESCOURBES"]["C"]["C" + str(i)]["DATAX"]["DonneesX"]["DONNEES"] ])
            table_string[i].append( doc["BLOC-COURBES"]["LESCOURBES"]["C"]["C" + str(i)]["DATAY"]["DonneesY"]["DONNEES"] )


import io  # Nécessaire car le fichier est encodé en 'utf-16-le'
import xmltodict  # Pour lire facilement le fichier xml
import struct
import binascii


def nettoyage(texte: str):
    # Le fishier ne respecte pas totalement la norme xml
    # La première partie (qui nous intéresse) est valide
    # On va donc l'extraire

    pos = texte.find("</BLOC-COURBES>")
    return texte[0:pos + 15]


def decoupe(table):
    # Découpe des chaînes de caractères en mots de 16 caractères
    pass


def conversion(table):
    # Renvoie une nouvelle table avec des float au lieu de str
    # struct.unpack('d', binascii.unhexify("3F5205BC01A36E2F"))
    pass


def extract(path: str):
    # En théorie retourne une liste de listes de liste de valeurs :
    # Chaque courbe latis pro contient deux listes de valeurs, une pour x et une pour y
    # Il y a potentiellement plusieurs courbes dans le fichier

    with io.open(path, 'r', encoding='utf-16-le') as file:  # Chargement du fichier
        content = nettoyage(file.read())

        doc = xmltodict.parse(content)

        nb_courbes = int(doc["BLOC-COURBES"]["LESCOURBES"]["C"]["@Nb"])

        table_string = []

        # Récupération des chaines hexadécimales
        for i in range(nb_courbes):
            table_string.append([])
            if doc["BLOC-COURBES"]["LESCOURBES"]["C"]["C" + str(i)]["DATAX"]["DonneesX"]["DONNEES"]:
                table_string[i].append(
                    doc["BLOC-COURBES"]["LESCOURBES"]["C"]["C" + str(i)]["DATAX"]["DonneesX"]["DONNEES"])
            table_string[i].append(doc["BLOC-COURBES"]["LESCOURBES"]["C"]["C" + str(i)]["DATAY"]["DonneesY"]["DONNEES"])

        table_float = []

        for i in range(len(table_string)):
            table_float.append([])
            for j in range(len(table_string[i])):
                table_float[i].append([])
                for k in range(int(len(table_string[i][j]) / 16)):
                    table_float[i][j].append(
                        struct.unpack('d', binascii.unhexlify(table_string[i][j][k * 16:(k + 1) * 16])))

    return table_float

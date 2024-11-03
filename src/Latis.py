import io           # Nécessaire, car le fichier est encodé en 'utf-16-le'
import xmltodict    # Pour lire facilement le fichier xml
import struct
import binascii


def nettoyage(texte: str):
    """Truncate text, hopefully turning it into valid xml.
    .lts don't contain a single roiot xml block, wich cause issue with parsing.
    This function extract the bloc `BLOC-COURBES`, assuming it's the first
    block in the file.

    Args:
        texte (str): the content of the .lts file as a string

    Returns:
        str: string containing the first `BLOC-COURBES` xml bloc of the file (hopefully)
    """

    # Le fishier ne respecte pas totalement la norme xml.
    # La première partie (qui nous intéresse) est valide.
    # On va donc l'extraire.

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
    """Extract the data from a .lts file.

    Args:
        path (str): path to the .lts file

    Returns:
        list: list of list of list of float, containing the data of the file
    """

    # En théorie retourne une liste de listes de liste de valeurs :
    # Chaque courbe latis pro contient deux listes de valeurs, une pour x et une pour y.
    # Il y a potentiellement plusieurs courbes dans le fichier.

    with io.open(path, 'r', encoding='utf-16-le') as file:  # Chargement du fichier

        # Gets a valid xml except from the file.
        content = nettoyage(file.read())

        # Convertion to dictionnary, to make it easier to work on.
        doc = xmltodict.parse(content)

        # Extract the number of curves, stored as a parameter of the `C` tag.
        nb_courbes = int(doc["BLOC-COURBES"]["LESCOURBES"]["C"]["@Nb"])

        # Table to store the hex strings of the various curves
        table_string = []

        # Récupération des chaines hexadécimales
        for i in range(nb_courbes):
            # Create a new sub-list for each curve
            table_string.append([])

            # Stores the x values if they exist
            if doc["BLOC-COURBES"]["LESCOURBES"]["C"]["C" + str(i)]["DATAX"]["DonneesX"]["DONNEES"]:
                table_string[i].append(
                    doc["BLOC-COURBES"]["LESCOURBES"]["C"]["C" + str(i)]["DATAX"]["DonneesX"]["DONNEES"])

            # Stores the y values
            table_string[i].append(doc["BLOC-COURBES"]["LESCOURBES"]["C"]["C" + str(i)]["DATAY"]["DonneesY"]["DONNEES"])

        # Table to store the float values of the various curves
        table_float = []

        for i in range(len(table_string)):
            table_float.append([])
            for j in range(len(table_string[i])):
                table_float[i].append([])

                # For each 16 characters sub-string
                for k in range(int(len(table_string[i][j]) / 16)):
                    # Convert the hex string and store it as a float
                    bytes_data = binascii.unhexlify(table_string[i][j][k * 16:(k + 1) * 16])
                    float_data = struct.unpack('d', bytes_data)
                    table_float[i][j].append(float_data)

    return table_float
import hashlib
import hmac
import time
import os
import random
import matplotlib.pyplot as plt
import pandas as pd
from tabulate import tabulate

# ---------- Partie 1 : HMAC avec clé ----------
def test_hmac():
    print("\n=== Exercice 1 - Partie 1 : HMAC ===\n")
    message = b"Bonjour ceci est un message de test"
    key = b"ma_cle_secrete"
    
    # 1a) HMAC officiel
    hmac_obj = hmac.new(key, message, hashlib.sha256)
    digest_hmac = hmac_obj.hexdigest()
    print(f"HMAC (SHA256) avec clé : {digest_hmac}")
    
    # 1b) Simulation avec hash simple (non équivalente, pour illustration)
    hash_simple = hashlib.sha256(key + message).hexdigest()
    hash_double = hashlib.sha256(key + hashlib.sha256(key + message).digest()).hexdigest()
    print(f"Hash simple (key+message) : {hash_simple}")
    print(f"Hash double (key + H(key+message)) : {hash_double}")
    print("NB : La vraie formule HMAC est plus complexe (opad/ipad).")
    print("Ceci n'est qu'une démonstration.\n")

# ---------- Partie 2a : Courbe temps vs taille pour HMAC ----------
def mesurer_temps_hmac(tailles, algo=hashlib.sha256):
    temps = []
    key = b"clef_test"
    for taille in tailles:
        data = os.urandom(taille)
        debut = time.perf_counter()
        hmac.new(key, data, algo).digest()
        fin = time.perf_counter()
        temps.append((fin - debut) * 1000)  # ms
    return temps

def tracer_courbe_hmac(tailles, temps):
    plt.figure(figsize=(10,6))
    plt.plot(tailles, temps, marker='o', label='HMAC SHA256')
    plt.xlabel("Taille des données (octets)")
    plt.ylabel("Temps (ms)")
    plt.title("Temps de HMAC en fonction de la taille des données")
    plt.grid(True)
    plt.xscale('log')
    plt.legend()
    plt.show()

# ---------- Partie 2b : Tableau des fichiers avec HMAC ----------
def creer_fichiers_echantillons(nb=5, dossier="echantillons_hmac"):
    if not os.path.exists(dossier):
        os.makedirs(dossier)
    fichiers = []
    for i in range(nb):
        taille = random.randint(1024, 5*1024*1024)  # entre 1 Ko et 5 Mo
        nom = f"fichier_{i+1}.txt"
        chemin = os.path.join(dossier, nom)
        with open(chemin, 'wb') as f:
            f.write(os.urandom(taille))
        fichiers.append(chemin)
    return fichiers

def calculer_hmac_fichier(chemin, key=b"clef_secrete", algo=hashlib.sha256):
    h = hmac.new(key, digestmod=algo)
    with open(chemin, 'rb') as f:
        for bloc in iter(lambda: f.read(4096), b''):
            h.update(bloc)
    return h.hexdigest()

def afficher_tableau_hmac(fichiers, key=b"clef_secrete"):
    donnees = []
    for chemin in fichiers:
        taille = os.path.getsize(chemin)
        hmac_val = calculer_hmac_fichier(chemin, key)
        nom = os.path.basename(chemin)
        donnees.append([nom, taille, hmac_val])
    df = pd.DataFrame(donnees, columns=["Nom", "Taille (octets)", "HMAC SHA256"])
    print("\n=== Tableau des fichiers avec HMAC ===")
    print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
    return df

# ---------- Effet avalanche ----------
def effet_avalanche():
    print("\n=== Effet avalanche (SHA256) ===\n")
    msg1 = b"bonjour"
    msg2 = b"Bonjour"
    h1 = hashlib.sha256(msg1).hexdigest()
    h2 = hashlib.sha256(msg2).hexdigest()
    print(f"SHA256 de '{msg1.decode()}' : {h1}")
    print(f"SHA256 de '{msg2.decode()}' : {h2}")
    # Compter les bits différents
    bits1 = bin(int(h1, 16))[2:].zfill(256)
    bits2 = bin(int(h2, 16))[2:].zfill(256)
    diff = sum(b1 != b2 for b1, b2 in zip(bits1, bits2))
    print(f"Nombre de bits différents : {diff} sur 256 (soit {diff/256*100:.1f}%)")
    print("L'effet avalanche est bien vérifié.\n")

# ---------- Exécution principale ----------
if __name__ == "__main__":
    test_hmac()
    
    print("=== Partie 2a : Courbe HMAC ===")
    tailles = [1024, 10*1024, 100*1024, 1024*1024, 10*1024*1024]  # 1 Ko à 10 Mo
    temps = mesurer_temps_hmac(tailles)
    tracer_courbe_hmac(tailles, temps)
    
    print("=== Partie 2b : Tableau HMAC sur fichiers ===")
    fichiers = creer_fichiers_echantillons(nb=5)
    afficher_tableau_hmac(fichiers)
    
    effet_avalanche()
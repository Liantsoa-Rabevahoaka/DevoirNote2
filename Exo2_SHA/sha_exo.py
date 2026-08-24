import hashlib
import time
import os
import random
import matplotlib.pyplot as plt
import pandas as pd
from tabulate import tabulate

# ---------- Exercice 2 : SHA-256 et SHA-3 (Keccak) ----------

def test_sha_algorithms():
    print("\n=== Exercice 2 : Test SHA-256 et SHA-3 (Keccak) ===\n")
    message = b"Bonjour test"
    sha256_hash = hashlib.sha256(message).hexdigest()
    sha3_256_hash = hashlib.sha3_256(message).hexdigest()
    print(f"SHA-256   : {sha256_hash}")
    print(f"SHA-3-256 : {sha3_256_hash}\n")

def mesurer_temps_sha(tailles, algo):
    temps = []
    for taille in tailles:
        data = os.urandom(taille)
        debut = time.perf_counter()
        algo(data).digest()
        fin = time.perf_counter()
        temps.append((fin - debut) * 1000)
    return temps

def tracer_courbe_sha(tailles, temps_sha256, temps_sha3):
    plt.figure(figsize=(10,6))
    plt.plot(tailles, temps_sha256, marker='o', label='SHA-256')
    plt.plot(tailles, temps_sha3, marker='s', label='SHA-3-256')
    plt.xlabel("Taille des données (octets)")
    plt.ylabel("Temps (ms)")
    plt.title("Comparaison SHA-256 vs SHA-3 (Keccak)")
    plt.grid(True)
    plt.xscale('log')
    plt.legend()
    plt.show()

def creer_fichiers(nb=5, dossier="echantillons_sha"):
    if not os.path.exists(dossier):
        os.makedirs(dossier)
    fichiers = []
    for i in range(nb):
        taille = random.randint(1024, 5*1024*1024)
        nom = f"fichier_{i+1}.txt"
        chemin = os.path.join(dossier, nom)
        with open(chemin, 'wb') as f:
            f.write(os.urandom(taille))
        fichiers.append(chemin)
    return fichiers

def calculer_hash_fichier(chemin, algo):
    h = algo()
    with open(chemin, 'rb') as f:
        for bloc in iter(lambda: f.read(4096), b''):
            h.update(bloc)
    return h.hexdigest()

def afficher_tableau_sha(fichiers):
    donnees = []
    for chemin in fichiers:
        taille = os.path.getsize(chemin)
        sha256_val = calculer_hash_fichier(chemin, hashlib.sha256)
        sha3_val = calculer_hash_fichier(chemin, hashlib.sha3_256)
        nom = os.path.basename(chemin)
        donnees.append([nom, taille, sha256_val, sha3_val])
    df = pd.DataFrame(donnees, columns=["Nom", "Taille (octets)", "SHA-256", "SHA-3-256"])
    print("\n=== Tableau des fichiers avec SHA-256 et SHA-3 ===")
    print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
    return df

if __name__ == "__main__":
    test_sha_algorithms()
    
    print("=== Courbe comparée SHA-256 vs SHA-3 ===")
    tailles = [1024, 10*1024, 100*1024, 1024*1024, 10*1024*1024]
    temps_sha256 = mesurer_temps_sha(tailles, hashlib.sha256)
    temps_sha3 = mesurer_temps_sha(tailles, hashlib.sha3_256)
    tracer_courbe_sha(tailles, temps_sha256, temps_sha3)
    
    print("=== Tableau des fichiers ===")
    fichiers = creer_fichiers(nb=5)
    afficher_tableau_sha(fichiers)
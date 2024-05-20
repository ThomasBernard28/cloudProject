from matplotlib.pyplot import imread
import matplotlib.pyplot as plt
import operator
import math
import os
import sys
import csv
import warnings


def euclidianDistance(l1,l2):
    distance = 0
    length = min(len(l1),len(l2))
    for i in range(length):
        distance += pow((int(l1[i]) - int(l2[i])), 2)
    return math.sqrt(distance)

def getkVoisins(lfeatures, test, k) :
    ldistances = []
    for i in range(len(lfeatures)):
        dist = euclidianDistance(test[1], lfeatures[i][1])
        ldistances.append((lfeatures[i][0], lfeatures[i][1], dist))
    ldistances.sort(key=operator.itemgetter(2))
    lvoisins = []
    for i in range(k):
        lvoisins.append(ldistances[i])
    return lvoisins

def recherche(image_req,top, features1):
  top=20
  voisins = getkVoisins(features1, features1[image_req],top)
  #print(voisins)
  nom_images_proches = []
  nom_images_non_proches = []
  for k in range(top):
      nom_images_proches.append(voisins[k][0])
      #print("done")
  plt.figure(figsize=(5, 5))
  plt.imshow(imread(features1[image_req][0]), cmap='gray', interpolation='none')
  plt.title("Image requête")
  nom_image_requete=os.path.splitext(os.path.basename(features1[image_req][0]))[0]
  print(nom_image_requete)
  plt.figure(figsize=(25, 25))
  plt.subplots_adjust(hspace=0.2, wspace=0.2)

  for j in range(top):
      plt.subplot(int(top/4),int(top/5),j+1)
      plt.imshow(imread(nom_images_proches[j]), cmap='gray', interpolation='none')
      nom_images_non_proches.append(os.path.splitext(os.path.basename(nom_images_proches[j]))[0])
      title = "Image proche n°"+str(j)
      plt.title(title)
  return nom_image_requete, nom_images_proches, nom_images_non_proches

def compute_RP(RP_file, top, nom_image_requete, nom_images_non_proches):
    rappel_precision=[]
    rp=[]
    position1=int(nom_image_requete)//100
    for j in range(top):
        position2=int(nom_images_non_proches[j])//100
        if position1==position2:
            rappel_precision.append("pertinent")
        else:
            rappel_precision.append("non pertinent")

    for i in range(top):
        j=i
        val=0
        while j>=0:
            if rappel_precision[j]=="pertinent":
                val+=1
            j-=1
        rp.append(str((val/(i+1))*100)+ " " + str((val/top)*100))

    with open(RP_file, 'w') as f:
        for a in rp:
            f.write(str(a) + '\n')


def display_RP(fichier):
    x = []
    y = []
    with open(fichier) as csvfile:
        plots = csv.reader(csvfile, delimiter=' ')
        for row in plots:
            x.append(float(row[0]))
            y.append(float(row[1]))
            fig = plt.figure()

    plt.plot(y, x,'C1', label='VGG16')
    plt.xlabel('Rappel')
    plt.ylabel('Précision')
    plt.title('Courbe Rappel-Précision')
    plt.legend()
    plt.savefig('RP.png')


if __name__ == "__main__":
    warnings.filterwarnings('ignore')
    files = "image.orig"         #Chemin vers la base d'images
    big_folder="Features_train/" #Dossier pour stocker les caractéristiques
    if not os.path.exists(big_folder):
        os.makedirs(big_folder)
    folder_model1="Features_train/VGG16/"
    if not os.path.exists(folder_model1):
        os.makedirs(folder_model1)
    
    features1 = []
    try:
        for i in range(1000):
            with open(folder_model1+str(i)+".txt", 'r') as f:
                name = f"image.orig/{i}.jpg"
                data = [float(line) for line in f.read().strip().split('\n')]
                features1.append((name, data))

    except Exception as e:
        print(f"Error reading file: {e}")

    if len(sys.argv) > 1:
        nom_image_requete, nom_images_proches, nom_images_non_proches = recherche(int(sys.argv[1]), 20, features1)
        compute_RP("VGG_RP.txt",20,nom_image_requete,nom_images_non_proches)
        display_RP("VGG_RP.txt")

    print("Image requête : ",nom_image_requete)
    print("Images proches : ",nom_images_proches)
    print("Images non proches : ",nom_images_non_proches)
    print("done")


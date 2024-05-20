from matplotlib.pyplot import imread
import matplotlib.pyplot as plt
import operator
import math
import os
import sys
import csv

from django.shortcuts import redirect, render
from django.conf import settings

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
    voisins = getkVoisins(features1, features1[image_req],top)
    #print(voisins)
    nom_images_proches = []
    nom_images_non_proches = []
    for k in range(top):
        nom_images_proches.append(voisins[k][0])
        #print("done")
    print(features1[image_req][0])
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

def home_view(request):
    return render(request, "home.html")

def submit(request):
    if request.method == 'POST':
        img = int(request.POST.get("img")[:-4])
        top = int(request.POST.get("top"))

        # perform the search
        big_folder = "Features_train/"

        if not os.path.exists(big_folder):
            print(f"{big_folder} do not exist, creating it")
            os.makedirs(big_folder)

        folder_model1=f"{big_folder}VGG16/"
        if not os.path.exists(folder_model1):
            print(f"{folder_model1} do not exist, creating it")
            os.makedirs(folder_model1)

        features1 = []
        try:
            for i in range(1000):
                path = os.path.join(settings.BASE_DIR, f"{folder_model1}{str(i)}.txt")
                with open(path, 'r') as f:
                    name = os.path.join(settings.BASE_DIR, f"media/image_orig/{i}.jpg")
                    data = [float(line) for line in f.read().strip().split('\n')]
                    features1.append((name, data))

        except Exception as e:
            print(f"Error reading file: {e}")

        nom_image_requete, nom_images_non_proches, nom_images_proches = recherche(img, top, features1)
        # compute_RP("VGG_RP.txt",20,nom_image_requete,nom_images_non_proches)
        # display_RP("VGG_RP.txt")
        context = {
            "nom_img_request" : nom_image_requete,
            "nom_img_proches" : nom_images_proches,
            "nom_img_non_proches" : nom_images_non_proches,
        }

        return render(request, "result.html", context)
    else:
        return render(request, "home.html")

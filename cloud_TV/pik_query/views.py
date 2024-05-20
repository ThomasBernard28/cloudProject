from matplotlib.pyplot import imread
import matplotlib.pyplot as plt
import operator
import math
import os
import sys

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

def home_view(request):
    return render(request, "home.html")

def submit(request):
    if request.method == 'POST':
        img = int(request.POST.get("img")[:-4])
        top = int(request.POST.get("top"))

        # perform the search
        files = "../image_orig"
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
                    name = f"{files}/{i}.jpg"
                    data = [float(line) for line in f.read().strip().split('\n')]
                    features1.append((name, data))

        except Exception as e:
            print(f"Error reading file: {e}")

        nom_image_requete, nom_images_proches, nom_images_non_proches = recherche(img, top, features1)
        print("Image requête : ",nom_image_requete)
        print("Images proches : ",nom_images_proches)
        print("Images non proches : ",nom_images_non_proches)
        print("done")

        context = {
            "nom_img_request" : nom_image_requete,
            "nom_img_proches" : nom_images_proches,
            "nom_img_non_proches" : nom_images_non_proches,
        }

        return render(request, "result.html", context)
    else:
        return render(request, "home.html")

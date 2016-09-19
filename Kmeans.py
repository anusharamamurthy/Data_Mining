import numpy as np
import random as rp

class Centroids:
    centroid = np.array([])
    blks = []

    def __init__(self,cv,datapoints):
        self.centroid = cv
        self.blks.append(datapoints)


def create_blocks(cv,datapoint):


    d_centroids={}

    # for each data point , compute the distance from each centroid

    for d in datapoint:
        lst = {}
        temp = []
        #print ("datapoint:",str(d))

        for c in cv:
            #print ("centroid:",str(c))

            # find the euclidean distance between the centroid and datapoint

            e_dist = euclidean(c,d)

            # store in a dictionary with centroid as the key

            lst[str(c)] = e_dist

            #print e_dist

        # find the centroid to which datapoint is closest

        c_v = find_min(lst)

        if c_v in d_centroids.keys():
            d_centroids[c_v].append(d)
        else:
            d_centroids[c_v] = [d];

    return d_centroids


def euclidean(cv,datapoint):

    r = np.power((cv-datapoint),2)
    e_dist = np.sqrt(r.sum())
    return e_dist


def find_min(lst):

    min = np.min(lst.values())
    key = [key for key,value in lst.items() if value == min]

    return key[0]


def initialize_centroids(k,datapoints):

    centers = []
    centroids = []
    #min_data = np.minimum.reduce(datapoints)
    #max_data = np.maximum.reduce(datapoints)

    #print datapoints.shape[1]

    for ndim in range(datapoints.ndim):
        min_data = np.minimum.reduce(datapoints)[ndim]
        max_data = np.maximum.reduce(datapoints)[ndim]
        #print rp.sample(range(min_data,max_data),1)
        centers.append(np.array(rp.sample(range(min_data,max_data),k)))
    #print centers

    for i in range(len(centers)):
        #print ("i is")
        #print i
        for j in range(len(centers[i])):
            #print("j is")
            #print j
            if (i+1 < len(centers) and j < len(centers[i])):
                #print centers[i][j]
                #print centers[i+1][j]
                centroids.append(np.array([centers[i][j],centers[i+1][j]]))

    return centroids




#main

datapoints = np.array([[2,5],[1,5],[22,55],[42,15],[15,16]])

centroids = initialize_centroids(3,datapoints)

#print centroids
blocks = create_blocks(centroids,datapoints)

print blocks

import numpy as np
import csv
import random as rp
import sys


def get_data(fname):

    fd = open(fname)
    try:
        reader = csv.reader(fd)
        s_data = [row for row in reader]
        # for e in s_data[1:]:
        #     e = map(int,e)
        #     data.append(e)
    except Exception, e:
        print(e.message)
        exit()
    finally:
        fd.close()

    return s_data

def initialize_centroid(len_data,k):

    # select k number of indices from the number of data points

    cen = rp.sample(range(0,len_data),k)

    #print("center",len(cen))
    return cen

def get_distance(c,d):

    #n = len(d)
    #print n
    cen = np.array(c)
    dval = np.array(d)
    r = np.power(cen-dval,2)
    e_dist = np.power(r.sum(),(float(1)/2))
    return e_dist

def find_min(lst):

    min = np.min(lst.values())

    #print min

    key = [key for key,value in lst.items() if value == min]

    return key[0]

def create_blocks(cv,datadict):


    d_centroids={}

    # for each data point , compute the distance from each centroid

    for key,d in datadict.items():
        lst = {}
        temp = []
        #print ("datapoint:",str(d))

        for c in cv:
            #print ("centroid:",str(c))

            # find the euclidean distance between the centroid and datapoint

            e_dist = get_distance(c,d[0:8])

            # store in a dictionary with centroid as the key

            lst[str(c)] = e_dist

            #print e_dist

        # find the centroid to which datapoint is closest

        c_v = find_min(lst)

        if c_v in d_centroids.keys():
            d_centroids[c_v].append((key,d[0:8]))
        else:
            d_centroids[c_v] = [(key,d[0:8])];

    return d_centroids

def recalculate_centroids(prev_blks):

    n = 0
    new_keys = []
    #print prev_blks
    for keys in prev_blks.keys():
        #print ("keys")
        n = len(prev_blks[keys])
        sum_val = [0,0,0,0,0,0,0,0]
        for k,values in prev_blks[keys]:

            sum_val = np.array(values[0:8]) + np.array(sum_val)

        temp = sum_val/n

        #print temp
        new_keys.append(temp)
    #print new_keys
    return new_keys

#main


fname ="Delta2Clean.csv"
dpoints = get_data(fname)
datapoints = []

data_dict = {}

data = [map(int,e) for e in dpoints[1:]] ## skip the column names
iter = 0
for e in data:
    data_dict[str(iter)] = e
    iter +=1

#print len(data_dict)

#class_dict = class_labels(data)
#print class_dict

for e in data_dict.values():

        #skip the class label

        key = str(e[0:8])
        datapoints.append(e[0:8])
        #print len(e[0:8])
        #print e[0:9]

#print class_dict
# clusters retured are indexes generated at random
k=7



# dist = get_distance(clusters[0],data[0])
# print clusters[0]
# print data[0]
# print dist


#print blocks
delta = 2000
threshold = 0.025

clusters = []
clusters_prev = []
iter_count = 0

blocks = {}
while(delta >= threshold):

    #print iter_count
    if(iter_count == 0):

        #print("I should run only once")
        # pick k clusters from datapoints
        c_index = initialize_centroid(len(data_dict),k)


        for e in c_index:
            clusters.append(data_dict[str(e)][0:8])
        #print clusters

        blocks = create_blocks(clusters,data_dict)
        #print blocks

        iter_count += 1

    else:

        clusters_prev = clusters
        #print clusters_prev
        blocks_prev = blocks

        clusters = recalculate_centroids(blocks_prev)


        #print iter_count
        sum_cluster_dist = 0

        new_k = len(clusters)
        old_k = len(clusters_prev)
        if new_k != old_k:

            print("Legnth of old k:",len(clusters))
            print("Length of new k:",len(clusters_prev))

            print("collapse of centroids")

        #To handle collapsing of centroids
        for i in range(0,new_k):
            #print i
            #print len(clusters)
            #print len(clusters_prev)
            sum_cluster_dist += get_distance(clusters_prev[i],clusters[i])

        delta = (sum_cluster_dist/k)
        blocks = create_blocks(clusters,data_dict)

        iter_count += 1
        #print delta

# when coverge calculate error
#print blocks
label = {} #label = "{(count_benign,count_malignant,"class" )}
no_centers = 1
total_error = 0
for cen,blks in blocks.items():
    #print blocks
    #print cen
    count_benign = 0
    count_malignant = 0
    for points in blks:
        if data_dict[str(points[0])][8]  == 2: #key and value in the tuple points
            count_benign +=1
        elif data_dict[str(points[0])][8]  == 4:
            count_malignant +=1

    if count_benign > count_malignant:
        label[str(no_centers)] = (count_benign,count_malignant,"b")
    elif count_benign <= count_malignant:
        label[str(no_centers)] = (count_benign,count_malignant,"m")

        total_count = (count_benign + count_malignant)
        total_error += (float(count_malignant)/(count_benign+count_malignant))
    #print total_error
    no_centers +=1
print ("Centroid labels:",label)
print ("Total error:",total_error)

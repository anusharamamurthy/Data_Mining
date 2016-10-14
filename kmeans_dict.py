import argparse
import numpy as np
import csv
import random as rp
import sys


parser = argparse.ArgumentParser(description="K-MEANS Algorithm")
parser.add_argument('-k', '--n_clusters', help="Include the number of clusters")
parser.add_argument('-f', '--filename', help="Include the filename with path")
parser.add_argument('-i', '--iterations', help="Include the number of iterations")
parser.add_argument('-th', '--threshold', help="Include the threshold")


try:
    args = vars(parser.parse_args())
except Exception, e:
    exit()

filename = args['filename'] or "Delta2Clean.csv"
k = args['n_clusters'] or 3
iterations = args['iterations'] or 100
threshold = args['threshold'] or 0.25


def pre_process(dpoints):

    datapoints = []

    data_dict = {}

    data = [map(int, e) for e in dpoints[1:]]  ## skip the column names
    myiter = 0
    for e in data:
        data_dict[str(myiter)] = e
        myiter += 1

    #print len(data_dict)

    # class_dict = class_labels(data)
    # print class_dict

    for e in data_dict.values():

        no_columns = len(e) - 1
        ''' assuming the last columns is the label'''
        # skip the class label

        key = str(e[0:no_columns])
        datapoints.append(e[0:no_columns])
        # print len(e[0:8])
        # print e[0:9]

    return data_dict,datapoints,no_columns

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

    #print len_data
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

def create_blocks(cv,datadict,ndim):


    d_centroids={}

    # for each data point , compute the distance from each centroid

    for key,d in datadict.items():
        lst = {}
        temp = []
        #print ("datapoint:",str(d))

        for c in cv:
            #print ("centroid:",str(c))

            # find the euclidean distance between the centroid and datapoint

            e_dist = get_distance(c,d[0:ndim])

            # store in a dictionary with centroid as the key

            lst[str(c)] = e_dist

            #print e_dist

        # find the centroid to which datapoint is closest

        c_v = find_min(lst)

        if c_v in d_centroids.keys():
            d_centroids[c_v].append((key,d))
        else:
            d_centroids[c_v] = [(key,d[0:ndim])];

    return d_centroids

def recalculate_centroids(prev_blks,ndim):

    n = 0

    new_keys = []

    for keys in prev_blks.keys():

        n = len(prev_blks[keys])

        sum_val = [np.repeat(0,ndim)]

        for k,values in prev_blks[keys]:

            sum_val = np.array(values[0:ndim]) + np.array(sum_val)

        temp = sum_val/n

        # print temp

        new_keys.append(temp)

    # print new_keys

    return new_keys


def get_error(blks):

    clist = []

    for centeroids,cblks in blks.items():

        print cblks

def kmeans():

    clusters = []

    blocks = []

    delta = 1
    """get the data from the file"""

    data = get_data(filename)

    ''' get only the required columns and the dimensions of the data'''
    data_dict, datapoints, dimensions = pre_process(data)

    c_index = initialize_centroid(len(datapoints), k)

    for e in c_index:
        clusters.append(datapoints[e])

    blocks = create_blocks(clusters, data_dict, int(dimensions))

    i = 0


    while(i <= iterations and delta > threshold):

        clusters_prev = clusters
        blocks_prev = blocks

        clusters = recalculate_centroids(blocks_prev,int(dimensions))
        sum_cluster_dist = 0

        new_k = len(clusters)
        old_k = len(clusters_prev)
        if new_k != old_k:
            print("Legnth of old k:", len(clusters))
            print("Length of new k:", len(clusters_prev))

            print("collapse of centroids")

        # To handle collapsing of centroids
        for i in range(0, new_k):
            # print i
            # print len(clusters)
            # print len(clusters_prev)
            sum_cluster_dist += get_distance(clusters_prev[i], clusters[i])

        delta = (sum_cluster_dist / k)
        blocks = create_blocks(clusters, data_dict,int(dimensions))

        i += 1

        print delta

    print (get_error(blocks))

'''get main method'''
kmeans()

# print(args)





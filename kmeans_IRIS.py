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

filename = args['filename'] or "iris.data.txt"
k = int(args['n_clusters'])
iterations = args['iterations'] or 100
threshold = args['threshold'] or 0.25


def pre_process(dpoints):

    datapoints = []

    data_dict = {}

    # for i in dpoints:
    #     print i[0:3]

    # data = [map(int, e) for e in dpoints[1:]]  ## skip the column names

    data = [map(float,e[0:4]) for e in dpoints]  ## no the column names
    # print data
    myiter = 0
    for e in dpoints:

        data_dict[str(myiter)] = e
        myiter += 1

    # print data_dict
    # print len(data_dict)

    #class_dict = class_labels(data)
    #print class_dict

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
        s_data = [row for row in reader if len(row) is not 0]
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
    cen = np.array(map(float,c))

    dval = np.array(map(float,d))

    try:
        r = (cen-dval)**2
        #s = np.sqrt(r.sum())

        e_dist = np.sqrt(r.sum())
        return e_dist
    except:
        print c,d

def find_min(lst):

    min = np.min(lst.values())

    #print min

    key = [key for key,value in lst.items() if value == min]

    return key[0]

def create_blocks(cv,datadict,ndim):


    d_centroids={}
    blks = []

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

            if len(d) == 0:
                print "exception"


        # find the centroid to which datapoint is closest

        c_v = find_min(lst)

        if c_v in d_centroids.keys():

            d_centroids[c_v].append((key,d[0:ndim]))

        else:

            d_centroids[c_v] = [(key,d[0:ndim])]


    return d_centroids

def recalculate_centroids(prev_blks,ndim):

    n = 0

    new_keys = []

    for keys in prev_blks.keys():

        n = len(prev_blks[keys])


        sum_val = np.array([0.0 for i in range(ndim)])

        for k,values in prev_blks[keys]:

            values = np.array(map(float,values[0:ndim]))
            sum_val = values + sum_val

        temp = sum_val/n

        # print temp

        new_keys.append(temp)

    # print new_keys

    return new_keys


def get_error(data_dict,blks):


    err_list = []
    for center,c_blk in blks.items():
        c_max = []
        c_s = 1
        c_vi = 1
        c_ve = 1
        for l in c_blk:

            lbl = data_dict[l[0]][-1]

            if lbl == 'Iris-setosa':
                c_s+=1
            elif lbl == 'Iris-virginica':
                c_vi +=1
            else: c_ve +=1

        c_max.append(c_s)
        c_max.append(c_vi)
        c_max.append(c_ve)
        max_lbl = max(c_max)

        err = float(max_lbl)/(c_s+c_vi+c_ve)

        err_list.append(err)

    return err_list


    # clist = []
    # label_dict = {}
    # count_label = {}
    #
    #
    # for centeroids, cblks in blks.items():
    #
    #     for blkid,value in cblks:
    #
    #         label = str(data_dict[blkid][-1])
    #
    #         clist.append(label)
    #
    # label_dict[str(centeroids)] = clist
    #
    # c_ver = 0
    # c_set = 0
    # c_vir = 0
    # id_k = 1
    # temp = {}
    # for i in label_dict.keys():
    #
    #     for labels in label_dict[i]:
    #
    #         if(labels == 'Iris-setosa'):
    #             c_set +=1
    #         elif(labels == 'Iris-versicolor'):
    #             c_ver +=1
    #         else: c_vir +=1
    #
    #     l=[]
    #     temp['0'] = c_set
    #     temp['1'] = c_ver
    #     temp['2'] = c_vir
    #     l.append(temp)
    #     count_label[id_k] = l
    #
    # return label_dict


def kmeans():

    clusters = []

    blocks = []

    delta = 1
    """get the data from the file"""

    data = get_data(filename)

    ''' get only the required columns and the dimensions of the data'''
    data_dict, datapoints, dimensions = pre_process(data)


    c_index = initialize_centroid(len(datapoints),int(k))


    for e in c_index:
        clusters.append(datapoints[e])

    #print clusters

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

            sum_cluster_dist += get_distance(clusters_prev[i], clusters[i])

        delta = (sum_cluster_dist / k)
        blocks = create_blocks(clusters, data_dict,int(dimensions))

        i += 1

        # print blocks

    print ("Number of clusters is "+str(k))
    print ("Average Accuracy is "+str(round(np.mean(get_error(data_dict,blocks))*100,2))+'%')

'''get main method'''
kmeans()

# print(args)




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

filename = args['filename'] or "iris.data.txt"
k = int(args['n_clusters'])
iterations = int(args['iterations']) or 100
threshold = float(args['threshold']) or 0.25


def pre_process(dpoints):

    datapoints = []

    data_dict = {}

    # for i in dpoints:
    #     print i[0:3]

    # data = [map(int, e) for e in dpoints[1:]]  ## skip the column names

    data = [map(float,e[0:4]) for e in dpoints]  ## no the column names
    # print data
    myiter = 0
    for e in dpoints:

        data_dict[str(myiter)] = e
        myiter += 1

    # print data_dict
    # print len(data_dict)

    #class_dict = class_labels(data)
    #print class_dict

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
        s_data = [row for row in reader if len(row) is not 0]
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
    cen = np.array(map(float,c))

    dval = np.array(map(float,d))

    try:
        r = (cen-dval)**2
        #s = np.sqrt(r.sum())

        e_dist = np.sqrt(r.sum())
        return e_dist
    except:
        print c,d

def find_min(lst):

    min = np.min(lst.values())

    #print min

    key = [key for key,value in lst.items() if value == min]

    return key[0]

def create_blocks(cv,datadict,ndim):


    d_centroids={}
    blks = []

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

            if len(d) == 0:
                print "exception"


        # find the centroid to which datapoint is closest

        c_v = find_min(lst)

        if c_v in d_centroids.keys():

            d_centroids[c_v].append((key,d[0:ndim]))

        else:

            d_centroids[c_v] = [(key,d[0:ndim])]


    return d_centroids

def recalculate_centroids(prev_blks,ndim):

    n = 0

    new_keys = []

    for keys in prev_blks.keys():

        n = len(prev_blks[keys])


        sum_val = np.array([0.0 for i in range(ndim)])

        for k,values in prev_blks[keys]:

            values = np.array(map(float,values[0:ndim]))
            sum_val = values + sum_val

        temp = sum_val/n

        # print temp

        new_keys.append(temp)

    # print new_keys

    return new_keys


def get_error(data_dict,blks):


    err_list = []
    for center,c_blk in blks.items():
        c_max = []
        c_s = 1
        c_vi = 1
        c_ve = 1
        for l in c_blk:

            lbl = data_dict[l[0]][-1]

            if lbl == 'Iris-setosa':
                c_s+=1
            elif lbl == 'Iris-virginica':
                c_vi +=1
            else: c_ve +=1

        c_max.append(c_s)
        c_max.append(c_vi)
        c_max.append(c_ve)
        max_lbl = max(c_max)

        err = float(max_lbl)/(c_s+c_vi+c_ve)

        err_list.append(err)

    return err_list


    # clist = []
    # label_dict = {}
    # count_label = {}
    #
    #
    # for centeroids, cblks in blks.items():
    #
    #     for blkid,value in cblks:
    #
    #         label = str(data_dict[blkid][-1])
    #
    #         clist.append(label)
    #
    # label_dict[str(centeroids)] = clist
    #
    # c_ver = 0
    # c_set = 0
    # c_vir = 0
    # id_k = 1
    # temp = {}
    # for i in label_dict.keys():
    #
    #     for labels in label_dict[i]:
    #
    #         if(labels == 'Iris-setosa'):
    #             c_set +=1
    #         elif(labels == 'Iris-versicolor'):
    #             c_ver +=1
    #         else: c_vir +=1
    #
    #     l=[]
    #     temp['0'] = c_set
    #     temp['1'] = c_ver
    #     temp['2'] = c_vir
    #     l.append(temp)
    #     count_label[id_k] = l
    #
    # return label_dict


def kmeans():

    clusters = []

    blocks = []

    delta = 1
    """get the data from the file"""

    data = get_data(filename)

    ''' get only the required columns and the dimensions of the data'''
    data_dict, datapoints, dimensions = pre_process(data)


    c_index = initialize_centroid(len(datapoints),int(k))


    for e in c_index:
        clusters.append(datapoints[e])

    #print clusters

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

            sum_cluster_dist += get_distance(clusters_prev[i], clusters[i])

        delta = (sum_cluster_dist / k)
        blocks = create_blocks(clusters, data_dict,int(dimensions))

        i += 1

        # print blocks

    print ("Number of clusters is "+str(k))
    print ("Average Accuracy is "+str(round(np.mean(get_error(data_dict,blocks))*100,2))+'%')

'''get main method'''
kmeans()

# print(args)





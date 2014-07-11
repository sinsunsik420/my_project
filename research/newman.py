# -*- coding:utf-8 -*-
# -*- encodin:utf-8 -*-

from collections import defaultdict as dd
from argparse import ArgumentParser

def getargs():

    parser = ArgumentParser(description='Newman Clustering Program.')
    parser.add_argument('-f', dest='input_file', help='input file(network data)', required=True)
    parser.add_argument('-o', dest='output_file', help='output file(cluster data)', required=True)
    args = parser.parse_args()
    return args

def newman_community_detection(g_dic):

# deltaQ values
    deltaQ = {}	
# H values
    H = {}	
# the a values
    a = {}
    
    q = 0
    maxQ = 0.0
    backupQ = 0.0
    maxCommunities = []
    
# m is the number of edges or sum of edge's weights.
    m = sum([v  for value in g_dic.values() for v in value.values()])
    
    for node in g_dic.keys():
        dqr = {}
        ki = sum([v for v in g_dic[node].values()])
        # assign row values
        for neighbor in g_dic[node].keys():
            kj = sum([v for v in g_dic[neighbor].values()])
            result = sum([g_dic[node][n] - (ki * kj)/(2*m) for n in neighbor]) / (2*m)
            dqr[(neighbor,)] = result

        H[(node,)] = max(dqr.items(), key=lambda x:x[1])
        deltaQ[(node,)] = dqr
        av = ki/(2.0 * m)
        a[(node,)] = av
        q -= av**2

    #initialize Qvalues
    maxQ = q

    while len(deltaQ) > 1:
        # find the max H value
        (i, (j,mdq)) = max(H.items(),key=lambda x:x[1][1])
        # merge communities i and j
        ci = deltaQ.pop(i)
        cj = deltaQ.pop(j)
        ai = a.pop(i)
        aj = a.pop(j)
        # create a label for our parent node as a joined tuple
        li = i
        lj = j
        label = li + lj
        cij = {}
        marker = {}
        
        # O( |i| log(n) )
        #pprint.pprint(deltaQ)
        for i_key in ci.keys():
            if j == i_key: continue
            del deltaQ[i_key][i]
            marker[i_key] = 2

        # O( |j| log(n) )
        for j_key in cj.keys():
            if i == j_key: continue
            del deltaQ[j_key][j]
            try:
                # both are conected to k (3)
                marker[j_key] += 1
            except:
                # k is connected to j
                marker[j_key] = 1
	
        for m_key,markerkey in marker.items():
            if markerkey == 3:
                newDeltaQ = ci[m_key] + cj[m_key]
            elif markerkey == 2:
                newDeltaQ = ci[m_key] - (2 * aj * a[m_key])
            else:
                newDeltaQ = cj[m_key] - (2 * ai * a[m_key])
                
            # get the last best maxQ
            (col, maxDeltaQ) = H[m_key]
            cij[m_key] = newDeltaQ
            deltaQ[m_key][label] = newDeltaQ
            if col == j or col == i: H[m_key] = max(deltaQ[m_key].items(), key=lambda x:x[1])
	
        # cleanup the old stuff
        #maxCommunities = H.keys()
        del H[i]
        del H[j]
        deltaQ[label] = cij
        try:
            H[label] = max(cij.items(),key=lambda x:x[1])
        except ValueError:
            pass

        a[label] = ai + aj
        q += mdq

        if q > maxQ:
            maxQ = q
            if H.keys() != []: maxCommunities = H.keys()
        
    return (maxQ,maxCommunities)

if __name__ == "__main__":
    args = getargs()
    network_data = dd(lambda : dd(float))
    with open(args.input_file) as f:
        for u, line in enumerate(f):
            neighbors = line.strip().split()
            for n_e in neighbors:
                n, e = n_e.split(":")
                network_data[u+1][int(n)] = float(e)
                network_data[int(n)][u+1] = float(e)

    maxQ, communities = newman_community_detection(network_data)
    print("max modularity: %f\n" % (maxQ))

    with open(args.output_file, "w") as f:
        for community in communities: f.write("%s\n" % (json.dumps(community)))

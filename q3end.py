import numpy as np
from collections import Counter
import settings

def get_parent_ids(n_id):
    # get parent ids for a node stop at any backbone chain
    res = [n_id]

    while n_id > settings.parent_bbone:
        n_id = settings.parents[n_id]
        res.append(n_id)
    return res

def readfile(filename, bb=1):
    #  for test5 and test6

    # test5 - readfile("test5", 120001)
    # test6 - readfile("test6", 1)

    # for test 5 = 120001, for test 6 = 1
    # it is used in other functions but could be found
    # during the loading of parents
    settings.parent_bbone = bb

    # open the file to read
    infile = open(filename, "r")

    # get the number of vertices
    settings.V = int(infile.readline().strip())
    print(settings.V)

    # load in the parents line
    # set the first two values for vertices 0 and 1
    # this makes all the numbering 1-based
    parent_line = infile.readline()
    settings.parents = [0]
    settings.parents.append(0)
    settings.parents.extend([int(v) for v in parent_line.split()])

    # ICs are loaded into a list and shifted for 1-based
    ic_line = infile.readline()
    settings.IC = [int(i)/1000 for i in ic_line.split()]
    settings.IC.insert(0, 0)

    # get the number of diseases and print out
    settings.nD = int(infile.readline().strip())
    print("Number of diseases:", settings.nD)

    # set diseases[0] to 0
    settings.diseases = [0]

    # load in each disease line
    for dd in range(1, settings.nD + 1):
        # loads .. 2 3435 34566 46777 etc
        # first is number of phenotypes
        d_spot = [int(c) for c in infile.readline().split()]

        # get first phenotype 
        # this is why i am amazed it worked for test6
        # because we only look at the first phenotype
        # but this can be looped for test6 as there are
        # only 1-3 phenos per disease
        d_v = d_spot[1]
        
        # get a reversed sorted list of parent ids
        # add to dictionary settings.vd
        # vd[vertex] = [disease ID list]
        dset = sorted(set(get_parent_ids(d_v)), reverse=True)
        for d in dset:
            if not d in settings.vd.keys():
                settings.vd[d] = [dd]
            else:
                (settings.vd[d]).append(dd)
        # also append to diseases list but this not needed
        # left over from previous code?
        settings.diseases.append(d_v)

    # get number of patients and print
    settings.nP = int(infile.readline().strip())
    print("Number of patients:", settings.nP)

    # left over - settings.patients isn't needed
    settings.patients=[0]

    # this is the answer list = patient's diseases 
    # settings.pat_dis[patient] = disease
    settings.pat_dis=[]

    # for each patient line read the line from the file
    for pp in range(1, settings.nP + 1):
        p_spot = [int(c) for c in infile.readline().split()]

        # again - amazed this works for test6 because only taking first symptom
        v = p_spot[1]

        # not needed
        settings.patients.append(v)

        # initialise disease to 0
        d = 0

        # is the patient phenotype vertex in the vd.keys
        # this is the easy case - take the first disease
        if v in settings.vd.keys():
            d = settings.vd[v][0]

        # get the patient's vertex tree
        # search down to the chain/backbone if it exists
        # if any of the vertices are in settings.vd take the first disease
        if d == 0:
            pps = sorted(set(get_parent_ids(v)), reverse=True)
            for ppsi in pps:
                if ppsi in settings.vd.keys():
                    d = settings.vd[ppsi][0]
                    break

        # search up the chain for diseases on any vertex
        # any disease whose parent ids end at the chain will have
        # inserted itself in settings.vd at the chain
        # in test 5 this is required - in test 6 bbone is 1
        if d == 0:
            for ppsi in range(v, settings.parent_bbone + 1):
                if ppsi in settings.vd.keys():
                    d = settings.vd[ppsi][0]
                    break
        
        # if all that fails walk down the bbone/chain to node1
        # take the first vertex with a disease on it
        if d == 0:
            for ppsi in range(v, 0, -1):
                if ppsi in settings.vd.keys():
                    d = settings.vd[ppsi][0]
                    break

        # used to set d to 1 to submit unfinished answers 
        if d == 0:
            d = 0
        
        settings.pat_dis.append(d)
    infile.close()

def save_answers(filename):
    # save settings.pat_dis to a text file
    np.savetxt(filename, settings.pat_dis, delimiter="\n", fmt="%s")

def readfile_v2():
    # for test 7
    infile = open("test7", "r")

    settings.V = int(infile.readline().strip())
    print(settings.V)

    # this uses nodepaths in a dict
    settings.nodepath = {}
    settings.nodepath[1] = [0]
    # using bbone is not really necessary but left from
    # previous code
    settings.parent_bbone = 1
    is_bbone = False

    # read the parent line
    # for each vertex add the vertex to nodepath as a list
    # set nodepath to same as parent + self
    parent_line = [int(p) for p in infile.readline().split()]
    bbone = 0
    for i in range(2,settings.V+1):
        if is_bbone and parent_line[i-2] == i-1:
            settings.nodepath[i] = [i]
            bbone = i
        else:
            settings.nodepath[i] = [*settings.nodepath[parent_line[i-2]], i]
            is_bbone = False

    # IC as list
    ic_line = infile.readline()
    settings.IC = [int(i)/1000 for i in ic_line.split()]
    settings.IC.insert(0, 0)

    # get number of diseases
    settings.nD = int(infile.readline().strip())
    print("Number of diseases:", settings.nD)

    # Create the dis_paths dictionary
    # dis_paths[vertex] = [list of diseases]
    settings.dis_paths = {}
    for d in range(1, settings.nD + 1):
        d_phenos = [int(c) for c in infile.readline().split()]
        # n_pheno = d_pheno[0]  # == 1

        # add disease ID to all phenotype nodes/vertices
        # and add the ID to all parent nodes/vertices
        # just the second block should work alone...?
        for d_pheno in d_phenos[1:]:
            if d in settings.dis_paths.keys():
                settings.dis_paths[d].extend(settings.nodepath[d_pheno])
            else:
                settings.dis_paths[d] = settings.nodepath[d_pheno]

            for dn in settings.nodepath[d_pheno]:
                if not dn in settings.vd.keys():
                    settings.vd[dn] = [d]
                else:
                    (settings.vd[dn]).append(d)

    # from old code.. needed?
    settings.diseases = list(sorted(settings.dis_paths.items(), key=lambda item: item[1]))

    # read in patients
    settings.nP = int(infile.readline().strip())
    print("Number of patients:", settings.nP)

    # this is the answer list:
    # settings.pat_dis[patient] = disease
    settings.pat_dis = []

    # read in each line and process to find disease 'pd'
    for q in range(1, settings.nP + 1):
        q_phenos = [int(c) for c in infile.readline().split()]
        # n_pheno = q_pheno[0]  # == 1

        pd = 0

        # this code was in development at the 11th hour
        # and I've not had the opportunity to correct it
        # you might be able to finish it off...

        ICdict = Counter()
        for q_pheno in q_phenos[1:]: 
            potentials = Counter()
            if q_pheno in settings.vd.keys():
                potentials.update({i:settings.IC[q_pheno] for i in settings.vd[q_pheno]})
                ICdict.update(settings.vd[q_pheno])

            # this prints the diseases for patients 39-60
            # edit to print sections of answers
            if q > 38 and q < 61:
                print(q, "IC", (ICdict.most_common(3)), "POT", (potentials.most_common(5)))
                print(q, "int", set(ICdict.most_common()).intersection(set(potentials.most_common())))

            # take the most common disease
            # this catches most of them
            pd = (ICdict.most_common(1))[0][0]

            # in process of editing...
            # (of course len(most_common(3)) = 3)
            if len(ICdict.most_common(3)) == 3:
                pass
            else:
                # grps = [list(item[1]) for item in it.groupby(sorted(potentials), key=lambda x: x[0])]
                if q < 10:
                    print("2", potentials.most_common(1))
                pd = 0
        
        # missing 596? cases in which i probably need
        # to compare total IC for each q_pheno

        settings.pat_dis.append(pd)
        # settings.patients.append(q_pheno)

    infile.close()

    # save the answers with saveanswers(filename)

class node:
    # Unused - start of idea for optimal solution
    leftJoin = (1, 1)
    rightJoin = ()
    IC = 0
    diseases = []
    def __init__(self, rightjoin, idx):
        self.rightJoin = rightjoin
    
    def add(node, index):
        pass

    def split(node):
        pass


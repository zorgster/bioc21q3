
def init():
    global V, vd, pat_dis, nodepath, nD, nP, parent_bbone, parents, IC, diseases, patients, pat_paths, dis_paths, edges
    V = 0
    nD = 0
    nP = 0
    parent_bbone = 2
    parents = []
    IC = []
    diseases = []
    patients = []
    vd = {}
    nodepath = {}
    pat_dis = []
    pat_paths = {}
    dis_paths = {}
    edges = []
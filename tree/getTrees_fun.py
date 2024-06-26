import logging
from ete3 import Tree
from config import TAXO_DIRECTORY

logger = logging.getLogger("LifemapBuilder")


def getTheTrees():
    ##DOWNLOAD taxdump and store in taxo folder
    ##DOWNLOAD TAXREF BY HAND! and put it in taxo/

    class Trans:
        def __init__(self):
            self.common_name_FR = []

    logger.info("Getting french translations...")
    TRANS = {}  ##translations in french
    with open(TAXO_DIRECTORY / "TAXREFv11.txt") as f:
        for line in f:
            sciname = line.split("\t")[14]
            comnameFR = line.split("\t")[19]
            if (sciname not in TRANS) and line.split("\t")[19] != "":
                TRANS[sciname] = Trans()
            if line.split("\t")[19] != "":
                TRANS[sciname].common_name_FR.append(comnameFR)

    # get translation of ranks
    logger.info("\nGetting rank names in french...")
    RANKS = {}
    with open(TAXO_DIRECTORY / "ranks.txt") as f:
        for line in f:
            rank_en = line.split("\t")[0]
            rank_fr = line.split("\t")[1].rstrip()  ##to remove \n
            RANKS[rank_en] = rank_fr

    class Taxid:
        def __init__(self):
            self.sci_name = ""
            self.authority = ""
            self.synonym = ""
            # 			self.common_name = ""
            self.common_name = []
            # 			self.common_name_FR = ""
            self.common_name_FR = []

    cpt = 0
    cptfr = 0
    ATTR = {}  ##here we will list attribute of each species per taxid
    logger.info("Reading NCBI taxonomy...")
    with open(TAXO_DIRECTORY / "names.dmp") as f:
        for line in f:
            taxid = line.split("|")[0].replace("\t", "")
            tid_val = line.split("|")[1].replace("\t", "")
            tid_type = line.split("|")[3].replace("\t", "")
            if taxid not in ATTR:
                ATTR[taxid] = Taxid()
            if tid_type == "scientific name":
                ATTR[taxid].sci_name = tid_val
                # and get translation in french (if any)
                if tid_val in TRANS:
                    ATTR[taxid].common_name_FR = TRANS[tid_val].common_name_FR
                    cptfr += 1
            if tid_type == "authority":
                if ATTR[taxid].authority != "":
                    ATTR[taxid].authority = ATTR[taxid].authority + ", " + tid_val
                else:
                    ATTR[taxid].authority = tid_val
            if tid_type == "synonym":
                if ATTR[taxid].synonym != "":
                    ATTR[taxid].synonym = ATTR[taxid].synonym + ", " + tid_val
                else:
                    ATTR[taxid].synonym = tid_val
            if tid_type == "common name":
                cpt += 1
                ATTR[taxid].common_name.append(tid_val)
                # if (ATTR[taxid].common_name!=""):
                # 	ATTR[taxid].common_name = ATTR[taxid].common_name + ", " + tid_val
                # else:
                # 	ATTR[taxid].common_name = tid_val

    T = {}

    filepath = TAXO_DIRECTORY / "nodes.dmp"
    logger.info("Building the NCBI taxonomy tree...")
    with open(filepath) as fp:
        _ = fp.readline()  ## remove the 1 | 1 edge
        for line in fp:
            dad = line.split("|")[1].replace("\t", "")
            son = line.split("|")[0].replace("\t", "")
            rank = line.split("|")[2].replace("\t", "")
            if dad not in T:
                T[dad] = Tree()
                T[dad].name = dad
                # 				T[dad].rank = rank
                # 				T[dad].rank_FR = RANKS[rank]
                T[dad].taxid = dad
                T[dad].sci_name = ATTR[dad].sci_name
                T[dad].common_name = ATTR[dad].common_name
                T[dad].synonym = ATTR[dad].synonym
                T[dad].authority = ATTR[dad].authority
                T[dad].common_name_FR = ATTR[dad].common_name_FR
            if son not in T:
                T[son] = Tree()
                T[son].name = son
                T[son].rank = rank
                T[son].rank_FR = RANKS[rank]
                T[son].taxid = son
                T[son].sci_name = ATTR[son].sci_name
                T[son].common_name = ATTR[son].common_name
                T[son].synonym = ATTR[son].synonym
                T[son].authority = ATTR[son].authority
                T[son].common_name_FR = ATTR[son].common_name_FR
            else:
                if not hasattr(T[son], "rank"):
                    T[son].rank = rank
            # 					T[son].rank_FR = RANKS[rank]
            T[dad].add_child(T[son])
    return T


# ##we save T entirely so that we do not hacve to write it to a file.
# logger.info("\n>>> Writing ARCHAEA tree...")
# with open('ARCHAEA.pkl', 'wb') as output:
#     pickle.dump(T['2157'], output, pickle.HIGHEST_PROTOCOL)
# logger.info("\n>>> Writing BACTERIA tree...")
# with open('BACTERIA.pkl', 'wb') as output:
#     pickle.dump(T['2'], output, pickle.HIGHEST_PROTOCOL)
# logger.info("\n>>> Writing EUKA tree...")
# with open('EUKARYOTES.pkl', 'wb') as output:
#     pickle.dump(T['2759'], output, pickle.HIGHEST_PROTOCOL)
# logger.info(">>> DONE")


# #t = T['1']
# tarc = T['2157']
# tbac = T['2']
# teuc = T['2759']

# logger.info("\n>>> Writing ARCHAEA tree...")
# tarc.write(outfile = "ARCHAEA", features = ["name", "taxid", "sci_name","common_name","rank", "authority","synonym","common_name_FR", "rank_FR"], format_root_node=True)
# logger.info("\n>>> Writing BACTERIA tree...")
# tbac.write(outfile = "BACTERIA", features = ["name", "taxid", "sci_name","common_name","rank", "authority","synonym","common_name_FR", "rank_FR"], format_root_node=True)
# logger.info("\n>>> Writing EUKA tree...")
# teuc.write(outfile = "EUKARYOTES", features = ["name", "taxid", "sci_name","common_name","rank", "authority","synonym","common_name_FR", "rank_FR"], format_root_node=True)
# logger.info(">>> DONE")


# RANKS = {}

# for n in t.traverse():
# 	if RANKS.has_key(n.rank)== False:
# 		RANKS[n.rank] = 1
# 	else:
# 		RANKS[n.rank] = RANKS[n.rank] + 1

# ranks = open("ranks.txt", "w")
# for k in RANKS:
# 	ranks.write("%s\t%s\n" % (k,RANKS[k]))

# ranks.close()

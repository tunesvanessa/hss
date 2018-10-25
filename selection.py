''' ===================== HYBRID SELECTION STRATEGY (HSS) ======================
        Universidade Federal de Sao Carlos - UFSCar, Sorocaba - SP - Brazil

        Master of Science Project       Artificial Intelligence

        Prof. Tiemi Christine Sakata    (tiemi@ufscar.br)
        Author: Vanessa Antunes         (tunes.vanessa@gmail.com)
   
    ============================================================================ '''

import numpy as np
import math

from sklearn.metrics.cluster import adjusted_rand_score
from sklearn.metrics.cluster import adjusted_mutual_info_score
from sklearn.metrics.cluster import completeness_score
from sklearn.metrics import jaccard_similarity_score
from sklearn.metrics.cluster import fowlkes_mallows_score

def similarity(reg, partitions, namePartitions):
    fx = []
    limm = len(reg)  
    for __ in range(0, limm):
        #aux = f1[namePartitions.index(reg[_][__]['id'])] + f2[namePartitions.index(reg[_][__]['id'])]
        #fx.append(aux)
        fmAux = 0
        ariAux = 0
        nmiAux = 0
        jaccardAux = 0
        for ___ in range(0, limm):
            ariAux += adjusted_rand_score(partitions[namePartitions.index(reg[__]['id'])]['cluster'], partitions[namePartitions.index(reg[___]['id'])]['cluster'])
            #fmAux += fowlkes_mallows_score(partitions[namePartitions.index(reg[__]['id'])]['cluster'], partitions[namePartitions.index(reg[___]['id'])]['cluster'])
            #nmiAux += adjusted_mutual_info_score(partitions[namePartitions.index(reg[__]['id'])]['cluster'], partitions[namePartitions.index(reg[___]['id'])]['cluster'])
        
        fx.append(round((ariAux / limm),2))
    
    return fx

def region_solution(reg, ari, final, max_fx, regNum):
    # Busca a lista de ARI para a particao _
    x=0
    for __ in range(0, len(ari)):
        if ari['id'][__] == reg[final]['id']:
            x = __
            break
    print '\n -> Region %d: %s %.2f' %(regNum, reg[final]['id'], max_fx),
    print ari[x][1]

    straux = ''
    for __ in range(0, len(ari['ari'][x])):
        straux += str('{0:.12f}'.format(ari['ari'][x, __])) + ' '

    return straux

def selection(reg, partitions, namePartitions, p_frontX, p_frontY, p_frontName, ari, output, y_pred):

    lim = len(reg)  
    fileout = open(output, 'w')
    regNum = 1
    utX = p_frontX[0]
    utY = p_frontY[-1]
    selected = []
    print 'Final Solutions:'

    for _ in range(0, lim):
        fx = similarity(reg[_], partitions, namePartitions)
        max_fx = max(fx)
        
        final = fx.index(max_fx)
        straux = region_solution(reg[_], ari, final, max_fx, _)
        fileout.write(reg[_][final]['id'] + ' ' + straux + '\n')
        selected.append(reg[_][final]['id'])
        
        '''
        final = [i for i, x in enumerate(fx) if x == max_fx]
        lesser = []

        if len(final) > 1:
            for __ in range(0, len(final)):
                x = final[__]
                nameSolution = namePartitions[namePartitions.index(reg[_][x]['id'])]
                idxSolution = p_frontName.index(nameSolution)
                lesser.append((p_frontX[idxSolution] - utX) + (p_frontY[idxSolution] - utY))
            
            x = lesser.index(min(lesser))
            straux = region_solution(reg[_], ari, final[x], max_fx, _)
            fileout.write(reg[_][final[x]]['id'] + ' ' + straux + '\n')
        else:
            straux = region_solution(reg[_], ari, final[0], max_fx, _)
            fileout.write(reg[_][final[0]]['id'] + ' ' + straux + '\n')
        '''
    fileout.close()
    return selected
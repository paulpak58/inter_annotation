import numpy as np
import torch
from torchmetrics.classification import MulticlassCohenKappa

def cohen_kappa_score(y1,y2,num_classes):
    target = torch.tensor(y1)
    preds = torch.tensor(y2)
    cohenkappa = MulticlassCohenKappa(num_classes=num_classes)
    score = cohenkappa(target,preds)
    # score = sklearn.metrics.cohen_kappa_score(y1,y2,labels=num_classes)
    return score

def cohen_kappa(y1,y2):
    '''
    y1: first annotations
    y2: second annotations

    Modified from: https://towardsdatascience.com/inter-annotator-agreement-2f46c6d37bf3
    '''
    count = 0
    y1 = y1.tolist()
    y2 = y2.tolist()
    for an1,an2 in zip(y1,y2):
        if an1==an2:
            count+=1
    A = count/len(y1)                       # observed agreement A
    unique = set(y1+y2)

    # if len(unique) == 1:
    #     kappa =  1.0
    # else:
    E = 0                                   # expected agreement
    for item in unique:
        count1 = y1.count(item)
        count2 = y2.count(item)
        count = ((count1/len(y1))*(count2/len(y2)))
        E += count
    # kappa = round((A-E)/(1-E+1e-4),10)
    kappa = round(1 - (1 - A)/(1-E+1e-10),3)

    return kappa

def jaccard_index(y1,y2):
    '''
    y1: first annotations
    y2: second annotations

    Modified from: https://towardsdatascience.com/inter-annotator-agreement-2f46c6d37bf3
    '''
    count = 0
    y1 = y1.tolist()
    y2 = y2.tolist()
    for an1,an2 in zip(y1,y2):
        if an1==an2:
            count+=1
    A = count/len(y1)  # observed agreement A
    A = round(A,3)
    return A

def fleiss_kappa(M):
    '''
    M: matrix of shape (N,k) where N=# items, k=# categories
    M[i,j]: # of raters who assigned ith subject to jth category

    Modified from: https://towardsdatascience.com/inter-annotator-agreement-2f46c6d37bf3
    '''
    M = np.array(M)
    N,k = M.shape
    num_annotators = float(np.sum(M[0,:]))
    total_annotations = N*num_annotators
    sum_categories = np.sum(M,axis=0)       # sum of each category over all items

    # Chance agreement
    p = sum_categories/total_annotations    # distribution of each category over all annotations
    pbar_E = np.sum(p*p)                    # average chance agreement

    # Observed agreement
    P = (np.sum(M*M,axis=1)-num_annotators)/(num_annotators*(num_annotators-1))
    pbar_O = np.sum(P)/N

    return round((pbar_O-pbar_E)/(1-pbar_E),4)

def confusion_matrix(y1,y2, N):
    cm = np.zeros((N,N))
    for i in range(len(y1)):
        cm[int(y1[i]),int(y2[i])] += 1

    return cm

if __name__=='__main__':
    target = np.array([0,2,2,2,2])
    preds = np.array([2,2,2,2,2])
    # score1 = cohen_kappa(target,preds)
    score1 = jaccard_index(target,preds)
    print(score1)
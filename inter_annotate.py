import numpy as np
import sklearn
# from sklearn.metrics import cohen_kappa_score
import torch
import torchmetrics
from torchmetrics.classification import MulticlassCohenKappa
import ipdb;

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
    # ipdb.set_trace()
    count = 0
    y1 = y1.tolist()
    y2 = y2.tolist()
    for an1,an2 in zip(y1,y2):
        if an1==an2:
            count+=1
    A = count/len(y1)                       # observed agreement A
    unique = set(y1+y2)
    E = 0                                   # expected agreement
    for item in unique:
        count1 = y1.count(item)
        count2 = y2.count(item)
        count = ((count1/len(y1))*(count2/len(y2)))
        E += count

    return round((A-E)/(1-E+1e-4),4)


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

if __name__=='__main__':
    target = np.array([2,1,0,0])
    preds = np.array([2,1,0,1])
    score1 = cohen_kappa(target,preds)
    print(score1)
   
    an1 = np.array([2,1,0,0])
    an2 = np.array([2,1,0,1])
    an3 = np.array([2,1,0,1])
    an4 = np.array([1,1,0,1])
    print(np.shape(np.concatenate((an1,an2,an3,an4))))

    '''
    target = torch.tensor([2,1,0,0])
    preds = torch.tensor([2,1,0,1])
    cohenkappa = MulticlassCohenKappa(num_classes=3)
    score = 0
    count = 0
    for i in range(len(target)):
        score += cohen_kappa([target[i]],[preds[i]])
        count += 1
    score /= count
    print(score)

    print(cohenkappa(preds,target))
    target = torch.tensor([2,1,0,0])
    preds = torch.tensor([2,1,0,1])
    cohenkappa = cohen_kappa_score(target,preds)
    print(round(cohenkappa,4))
    '''

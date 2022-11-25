import numpy as np
import sklearn
from sklearn.metrics import cohen_kappa_score
import torch
import torchmetrics
from torchmetrics.classification import MulticlassCohenKappa

'''
def cohen_kappa_score(y1,y2):
    # SKLearn
    score = cks(y1,y2)

    # Manual
    count = 0
    for an1,an2 in zip(y1,y2):
        if an1==an2:
            count += 1
    A = count/len(an1)
    unique = set(an1+an2)
    E = 0
    for elem in unique:
        c1 = y1.count(elem)
        c2 = y2.count(elem)
        count = ((c1/len(y1))*(c2/len(y2)))
        E += count
    score2 =round((A-E)/(1-E),4)

    return score,score2
'''


if __name__=='__main__':
    # score,score2 = cohen_kappa_score()
    target = torch.tensor([2,1,0,0])
    preds = torch.tensor([2,1,0,1])
    cohenkappa = MulticlassCohenKappa(num_classes=3)
    print(cohenkappa(preds,target))

    target = torch.tensor([2,1,0,0])
    preds = torch.tensor([2,1,0,1])
    cohenkappa = cohen_kappa_score(target,preds)
    print(round(cohenkappa,4))

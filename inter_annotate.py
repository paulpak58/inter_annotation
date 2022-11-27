import numpy as np
import sklearn
# from sklearn.metrics import cohen_kappa_score
import torch
import torchmetrics
from torchmetrics.classification import MulticlassCohenKappa

def cohen_kappa_score(y1,y2,num_classes):
    target = torch.tensor(y1)
    preds = torch.tensor(y2)
    cohenkappa = MulticlassCohenKappa(num_classes=num_classes)
    score = cohenkappa(target,preds)
    # score = sklearn.metrics.cohen_kappa_score(y1,y2,labels=num_classes)
    return score

if __name__=='__main__':
    target = torch.tensor([2,1,0,0])
    preds = torch.tensor([2,1,0,1])
    cohenkappa = MulticlassCohenKappa(num_classes=3)
    print(cohenkappa(preds,target))

    target = torch.tensor([2,1,0,0])
    preds = torch.tensor([2,1,0,1])
    cohenkappa = cohen_kappa_score(target,preds)
    print(round(cohenkappa,4))

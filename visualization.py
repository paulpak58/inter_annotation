import matplotlib.pyplot as plt
import numpy as np
import os
import cv2


def plot_confusion_matrix(cm, classes,
                          normalize='Recall',
                          title=None,
                          cmap=plt.cm.Greens,
                          res_dir='./results_plot/cm/',
                          res_filename = 'Confusion_Matrix'):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    os.makedirs(res_dir, exist_ok=True)
    if not title:
        if normalize == 'Recall':
            title = 'Confusion matrix: Recall'
        elif normalize == 'Precision':
            title = 'Confusion matrix: Precision'
        else:
            title = 'Confusion matrix'
    if normalize == 'Recall':
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    elif normalize == 'Precision':
        cm = cm.astype('float') / cm.sum(axis=0)
        cm[np.isnan(cm)] = 0

    fig, ax = plt.subplots(figsize=(8, 8))
    scale = 200
    cm = cv2.resize(cm, (scale * cm.shape[0], scale * cm.shape[1]), interpolation=cv2.INTER_NEAREST)
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    #ax.clim(0, 1)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(0 + 100, cm.shape[1] + 100, scale),
           yticks=np.arange(0 + 100, cm.shape[0] + 100, scale),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    plt.setp(ax.get_yticklabels(), va="top")


    # Loop over data dimensions and create text annotations.
    if normalize == 'Recall' or normalize == 'Precision':
        fmt = '.1f'
    else:
        fmt = '.1f'
    thresh = cm.max() / 2.
    for i in range(0, cm.shape[0], scale):
        for j in range(0, cm.shape[1], scale):
            if cm[i, j] > 0.1:
                ax.text(j + scale / 2, i + scale / 2, format(cm[i, j], fmt),
                        ha="center", va="center",
                        color="white" if cm[i, j] > thresh else "black",
                        fontsize='small')
    fig.tight_layout()
    fig.savefig(res_dir + res_filename + '_' + normalize + '.png')
    plt.close()
    return ax
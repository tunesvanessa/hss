''' ===================== HYBRID SELECTION STRATEGY (HSS) ======================
        Universidade Federal de Sao Carlos - UFSCar, Sorocaba - SP - Brazil

        Master of Science Project       Artificial Intelligence

        Prof. Tiemi Christine Sakata    (tiemi@ufscar.br)
        Author: Vanessa Antunes         (tunes.vanessa@gmail.com)
   
    ============================================================================ '''

import matplotlib.pyplot as plt
from collections import OrderedDict
import numpy as np

def plottingPartitions(plt, numFigure, ari, nameTP, f1, f2, maxx, Name, title, X, Y, figureName):
    fig = plt.figure(numFigure)
    #plt.scatter(f1, f2)
    ax = plt.axes()
    points_with_annotation = []
    
    for i in range(0, maxx):
        maxAri = float(max(ari['ari'][i]))
        if maxAri == 1:
            point, = plt.plot(f1[i], f2[i], 's', markersize=12, color='k', label='ARI = 1')
        elif  maxAri >= 0.85:
            point, = plt.plot(f1[i], f2[i], '^', markersize=11, color='b', label='0.85 <= ARI < 1')
        elif  maxAri >= 0.70:
            point, = plt.plot(f1[i], f2[i], 'v', markersize=11, color='m', label='0.70 <= ARI < 0.85')
        else:
            point, = plt.plot(f1[i], f2[i], 'o', markersize=9, color='#848482', label='0 <= ARI < 0.70')

        textAnnotation = []
        ari_med = 0
        for auxi, auxj in zip(nameTP, ari['ari'][i]):
            textAnnotation.append(auxi + ' '+ str(auxj))
            ari_med = ari_med + float(auxj)

        annotation = annotationPlot(ax, Name[i] + '\n' + '\n'.join(textAnnotation) + '\nARI medio: ' + str(ari_med), f1[i], f2[i])
        # by default, disable the annotation visibility
        annotation.set_visible(False)

        points_with_annotation.append([point, annotation])

    points_with_annotation = points_with_annotation + plot_true_partitions(ax, f1[maxx:], f2[maxx:], nameTP)
    
    def on_move(event):
        visibility_changed = False
        for point, annotation in points_with_annotation:
            should_be_visible = (point.contains(event)[0] == True)

            if should_be_visible != annotation.get_visible():
                visibility_changed = True
                annotation.set_visible(should_be_visible)

        if visibility_changed:        
            plt.draw()

    #x1,x2,y1,y2 = plt.axis()
    #plt.axis((x1-10,x2+10,y1-10,y2+10))
    plt.plot(X, Y, linewidth=1.5, color='g')
    plt.xlabel('Variance')
    plt.ylabel('Connectivity')
    plt.title(title)
    #plt.grid(True)
    
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc='upper right', shadow=True, fontsize='medium', numpoints=1)
    #legend = plt.legend(loc='upper right', shadow=True, fontsize='small')

    on_move_id = fig.canvas.mpl_connect('motion_notify_event', on_move)
    plt.savefig(figureName, format='png', dpi=1000)
    
    return plt

def plot_true_partitions(ax, f1TP, f2TP, nameTP):
    points_with_annotation = []

    for i in range(len(f1TP)):
        point, = plt.plot(f1TP[i], f2TP[i], 'd', markersize=11, color='r', label='TP')

        annotation = annotationPlot(ax, nameTP[i], f1TP[i], f2TP[i])
        
        # by default, disable the annotation visibility
        annotation.set_visible(False)

        points_with_annotation.append([point, annotation])

    return points_with_annotation

def annotationPlot(ax, text, f1, f2):
    bbox_annotation = dict(boxstyle="round", facecolor="w", edgecolor="0.5", alpha=0.9)
    arrowprops_style = dict(arrowstyle="simple", connectionstyle="arc3,rad=-0.2")

    annotation = ax.annotate("%s" % (text),
    xy=(f1, f2), xycoords='data',
    xytext=(float(f1) - float(f1) / 100, float(f2) + float(f2) / 10), textcoords='data',
    horizontalalignment="left",
    arrowprops=arrowprops_style,
    size = 10,
    bbox=bbox_annotation
    )

    return annotation

def plotRegionDivision(plt, numFigure, ari, nameTP, reduced_p_frontX, reduced_p_frontY, reduced_p_frontName, y_pred, title):

    fig = plt.figure(numFigure)
    ax = plt.axes()

    colors = np.array(['#808080', '#FF0000', '#0000FF', '#808000', '#008000', '#00FF00', '#008080', '#FF00FF', '#800080', '#FFFF00', '#00FFFF'])
    colors = np.hstack([colors] * 10)   
    
    maxx = len(reduced_p_frontX)
    array = []
    for i in range(0, maxx):
        aux = y_pred[i]
        aux1 = '$\Omega_{' + str(aux) + '}$'
        plt.plot(reduced_p_frontX[i], reduced_p_frontY[i], 'o', markersize=9, color=colors[y_pred][i], label=aux1)

        # Plot para artigo, solucoes selecionadas em vermelho
        '''if reduced_p_frontName[i] in namePartitionsSelected:
            array.append(i)
        else:
            plt.plot(reduced_p_frontX[i], reduced_p_frontY[i], 'o', markersize=5, color='b')
        

    for _ in array:
        plt.plot(reduced_p_frontX[_], reduced_p_frontY[_], 'o', markersize=5, color='r')
    '''
    #plt.scatter(reduced_p_frontX, reduced_p_frontY, color=colors[y_pred].tolist(), s=45)
    plt.xlabel('Variance')
    plt.ylabel('Connectivity')
    plt.title(title)

    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc='upper right', shadow=True, fontsize='large', numpoints=1)
    
    return plt

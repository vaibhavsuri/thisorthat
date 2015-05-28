__author__ = "sreeram"
import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
from pylab import savefig
from matplotlib import rcParams


rcParams["axes.labelsize"] = "20" 
rcParams["axes.labelweight"] = "bold" 
rcParams["font.size"] = "20" 
rcParams["font.weight"] = "bold" 
#===============================================================================
# rcParams["ytick.major.size"] = "20"
#===============================================================================

def bar_plot(x_axis_labels,y_axis_values,fig_name="blah.jpg",width=0.6,
             x_axis_offset=1,y_label="count",bar_title="count vs people",
             x_label="Users"):
    
    #===========================================================================
    # y_axis_values = [1,2,3,1,1]
    #===========================================================================
    
    y_axis_values = [float(i) for i in y_axis_values]
    
    " number of bars in the bar graph"
    num_items = len(x_axis_labels)
    
    " x axis locations of the bars"
    x_axis_locs = np.arange(num_items) + x_axis_offset
    
    colors = ['blue',  'green','red', 'brown','black']
    
    
    p1 = plt.bar(x_axis_locs,y_axis_values,width,color=colors)
    
    " setting the labels of bar graph"
    plt.ylabel(y_label,fontsize=20)
    plt.title(bar_title,fontsize=20)
    plt.xlabel(x_label,fontsize=20)
    
    " setting the tick locations of x-axis points"
    plt.xticks(x_axis_locs + width/2., tuple(x_axis_labels), rotation="60",
               fontsize=18 )    
    #===========================================================================
    # plt.yticks(np.array(y_axis_values))
    #===========================================================================
    
    plt.subplots_adjust(bottom=0.2)
        
    "setting the x-axis and y-axis limits"
    plt.xlim([x_axis_offset/2.0,num_items + x_axis_offset/2.0 + width])
    #===========================================================================
    # plt.ylim(0,max(y_axis_values)+2)
    #===========================================================================
    
    "saving the figure"
    print x_axis_labels
    print y_axis_values
    savefig(fig_name)
    plt.close()
    #===========================================================================
    # savefig(fig_name, bbox_inches='tight')
    #===========================================================================
    
    "displaying the figure"
    #===========================================================================
    # plt.show()
    #===========================================================================
    
if __name__ == '__main__':
    x_axis_labels = ['a','b','c']
    y_axis_values = [100,40,70]
    
    bar_plot(x_axis_labels, y_axis_values)
    


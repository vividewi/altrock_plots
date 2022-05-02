# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 02:44:19 2021

@author: user
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as  np
import sys

def TAS_plot_data():
    
    diagram_data = {'X': {0: 41.0, 1: 41.0, 2: 41.0, 3: 45.0, 4: 48.4, 5: 52.5, 6: 49.0, 7: 52.5, 8: 57.6, 9: 63.0, 10: 57.6, 11: 63.0, 12: 57.6, 13: 53.0, 14: 48.4, 15: 53.0, 16: 57.0, 17: 53.0, 18: 49.4, 19: 45.0, 20: 49.4, 21: 52.0, 22: 49.4, 23: 45.0, 24: 45.0, 25: 45.0, 26: 41.0, 27: 45.0, 28: 45.0, 29: 52.0, 30: 52.0, 31: 52.0, 32: 57.0, 33: 57.0, 34: 57.0, 35: 63.0, 36: 63.0, 37: 63.0, 38: 69.0, 39: 69.0, 40: 69.0, 41: 77.0},
                    'Y': {0: 0.0, 1: 3.0, 2: 7.0, 3: 9.4, 4: 11.5, 5: 14.0, 6: 15.5, 7: 14.0, 8: 11.7, 9: 14.56, 10: 11.7, 11: 7.0, 12: 11.7, 13: 9.3, 14: 11.5, 15: 9.3, 16: 5.9, 17: 9.3, 18: 7.3, 19: 9.4, 20: 7.3, 21: 5.0, 22: 7.3, 23: 5.0, 24: 0.0, 25: 3.0, 26: 3.0, 27: 3.0, 28: 5.0, 29: 5.0, 30: 0.0, 31: 5.0, 32: 5.9, 33: 0.0, 34: 5.9, 35: 7.0, 36: 0.0, 37: 7.0, 38: 8.0, 39: 13.0, 40: 8.0, 41: 0.0}}
    
    names_dictionary = {'Foidite' : [45, 13],
                        'Phonolite' : [55.7, 14],
                        'Tephriphonolite' : [50.2, 11.5],
                        'Phonotephrite' : [46.3, 9.2],
                        'Tephrite if IO<10%' : [42, 7],
                        'Basanite' : [41.3, 4.5],
                        'if OI>10%' : [41.3, 4.0],
                        'Picrobasalt' : [41.05, 1.5],
                        'Basalt' : [47.3, 2],
                        'Basaltic- ' : [52.7, 2],
                        'andesite' : [52.7, 1.5],
                        'Andesite' : [58, 1.5],
                        'Dacite' : [65, 1.5],
                        'Trachybasal' : [46.8, 5.4],
                        'Basaltic-' : [50.3, 7.3],
                        'trachyandesite' : [50.3, 6.7],
                        'Trachyandesite' : [54.4, 9],
                        'Trachyte' : [60, 12.5],
                        'if Q<20% in QAPF' : [60, 12],
                        'Trachydacite' : [61.5, 9.5],
                        'if Q>20% in QAPF' : [61.5, 9],
                        'Rhyolite' : [74, 4],
                        }
    return diagram_data, names_dictionary

def TAS_plot(filename):
    
    colorbar_thickness = 0.03
    headers = ['Normalized Na2O', 'Normalized K2O','IA']
    
    #Data acquisition
    diagram_data, names_dictionary = TAS_plot_data()
    data = pd.read_excel(filename,sheet_name='Sheet2')
    
    if set(headers).issubset(set( data.columns)):

        #Plot setup
        fig, ax = plt.subplots(dpi = 600)
        colormap = mpl.cm.winter_r
        ax.set_xlabel( '$Normalized \ SiO_2 \, (wt.\, \%)$', fontsize = 8)
        ax.set_ylabel( '$Normalized \ Na_2 O + K_2 O \ (wt.\, \%)$', fontsize = 8)
        
        #Creating a color map based on the values from 'IA' column
        colors = [colormap(i) for i in np.linspace(0, 1,len(data['IA'].unique()))]
        
        #Creating a dictionary based on the color map and 'IA' values
        color_dictionary = {}
        for k in range(len(sorted(data['IA'].unique()))):
            color_dictionary[str(sorted(data['IA'].unique())[k])] = colors[k]
        
        norm = mpl.colors.Normalize(vmin=0, vmax=max(data['IA']))
        
        #Plotting the lines for the diagram classifications
        for i, item in enumerate(diagram_data['X']):
            if i + 1 < len(diagram_data['X']) :
                ax.plot([diagram_data['X'][i], diagram_data['X'][i+1]],  [diagram_data['Y'][i], diagram_data['Y'][i+1]], '-k', lw = 0.5)

        #Plotting the names 
        for name in names_dictionary:
            ax.text(names_dictionary[name][0], names_dictionary[name][1], name, fontsize = 6)
        
        #Plotting each data point
        for i, item in enumerate(data['SiO2']):
            ax.scatter(data['Normalized SiO2'][i],data['Normalized Na2O'][i]+data['Normalized K2O'][i],
                        marker=data['symbol'][i], s = 25, edgecolor = 'black', linewidth = 0.3 , label = data['texture'][i], color = color_dictionary[str(data['IA'][i])])
                    
        #Removing the duplicate labels
        handles, labels = ax.get_legend_handles_labels()               
        unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]
        lg = ax.legend(*zip(*unique), fontsize = 5)
        
        #Setting the legend
        for i_l in range(len(unique)):
          lg.legendHandles[i_l].set_color('white')
          lg.legendHandles[i_l].set_edgecolor('black')
    
        #Creating the color bar
        cax = fig.add_axes([0.79, 0.5, colorbar_thickness, 0.25]) #([Xmin, Ymin, thickness, Ymax])
        cbar = mpl.colorbar.ColorbarBase(cax, cmap =colormap, norm = norm )
        cbar.set_label('Alteration intensity (%)', rotation = 90, fontsize = 5)
        cbar.ax.tick_params(labelsize=5)
        
        ax.set_ylim([0,max(diagram_data['Y'].values())])
        
        fig.savefig('TAS/TAS_diagram.png', dpi = 600)
        
        plt.show()

    else:
         sys.exit("The headers %s,  %s, and %s were not found on the input file"%(headers[0],headers[1],headers[2]))

def plot(filename):
    
    x_columns = ['SiO2','FeO', 'MgO'] #'loss of ignition (%)','loss of H2O+OH (%)', 'loss of CO2 (%)'
    
    colorbar_thickness = 0.03
    
    data = pd.read_excel(filename,sheet_name='Sheet2')
    
    data_ac = pd.read_excel(filename,sheet_name='ac')
    dont_plot = ['symbol','color','alteration','depth','texture',\
                 'Totaloxide','Normalized SiO2', 'Normalized Na2O', 'Normalized K2O']
     
    headers = ['IA']
    
    #Data acquisition
    diagram_data, names_dictionary = TAS_plot_data()
    data = pd.read_excel(filename,sheet_name='Sheet2')
    
    if set(headers).issubset(set(data.columns)):
            
        colormap = mpl.cm.winter_r
        colors = [colormap(i) for i in np.linspace(0, 1,len(data['IA'].unique()))]
        
        color_dictionary = {}
    
        for k in range(len(sorted(data['IA'].unique()))):
            color_dictionary[str(sorted(data['IA'].unique())[k])] = colors[k]
        
        norm = mpl.colors.Normalize(vmin=0, vmax=max(data['IA']))
        
        for column_x in x_columns:
            if column_x not in dont_plot:
                for column in  data.columns:
                    if column not in dont_plot and column != column_x:
                        
                        fig  = plt.figure(dpi = 600)
                        ax = fig.add_axes([0.1, 0.12, 0.75, 0.75])
                        
                        print(column, column_x)
                        
                        instrument = str(data_ac.loc[data_ac['Element'] == column_x, 'Instrument'].values[0]) 
                        
                        for i, item in enumerate(data[column]):
                            ax.scatter(data[column_x][i],data[column][i],
                                               marker=data['symbol'][i], s = 30, edgecolor = 'black',
                                               linewidth = 0.3 , label = data['texture'][i],  color = color_dictionary[str(data['IA'][i])],
                                               zorder=2)
                            
                            try:
                                y_error = data_ac.loc[(data_ac['Element'] == column) & (data_ac['Instrument'] == instrument), 'Accucracy']
                                if len(y_error) ==0:
                                    y_error = 0
                            except IndexError:
                                y_error = 0

                            try:
                                x_error = data_ac.loc[(data_ac['Element'] == column_x) & (data_ac['Instrument'] == instrument), 'Accucracy']
                                if len(x_error) ==0:
                                    x_error = 0
                            except IndexError:
                                x_error = 0
                                
                        
                        #dummy error bar
                        
                        ax.errorbar(max(data[column_x])*1.05,max(data[column])*1.05,
                                    yerr = y_error,
                                    xerr = x_error,
                                    fmt ='none',
                                    elinewidth = 0.5,
                                    capsize = 2,
                                    capthick = 0.5,
                                    barsabove = False,
                                    ecolor = 'black',
                                    zorder=1)
                        
                        ax.set_xlabel(column_x +' (' +str(data_ac.loc[data_ac['Element'] == column_x, 'Unit'].values[0]) + ')', fontsize = 8)
                        ax.set_ylabel(column +' (' +str(data_ac.loc[data_ac['Element'] == column, 'Unit'].values[0]) + ')', fontsize = 8)
                        
                        #To adjust the X_Y axis zooming for wt% data
                        ax.set_xlim([min(data[column_x])*0.9, max(data[column_x])*1.1])  #using min-max value plus some extent in X
                        
                        handles, labels = ax.get_legend_handles_labels()               
                        unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]
                        lg = ax.legend(*zip(*unique), fontsize = 6, bbox_to_anchor=(0.95, -0.15), ncol=4, frameon=False)
                        
                        for i_l in range(len(unique)):
                           lg.legendHandles[i_l].set_color('white')
                           lg.legendHandles[i_l].set_edgecolor('black')
                        
                    
                        

        
                        #CReates the colorbar
                        cax = fig.add_axes([0.87, 0.12, colorbar_thickness, 0.75]) #colorbar position
                        cbar = mpl.colorbar.ColorbarBase(cax, cmap =colormap,  norm =norm )
                        cbar.set_label('Alteration intensity (%)', rotation = 90, fontsize = 8)
                        cbar.ax.tick_params(labelsize=8)
                
                        fig.savefig('plots/'+column+'_vs_'+column_x+'.png',bbox_inches='tight',dpi=600)
                
        plt.show()
    else:
        sys.exit("Fail")

plot('data.xlsx')
#TAS_plot('data.xlsx')

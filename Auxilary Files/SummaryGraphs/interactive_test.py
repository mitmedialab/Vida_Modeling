#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 13:00:59 2021

@author: jackreid
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv
from screeninfo import get_monitors
import dateutil
from datetime import datetime


#Set filepath of data


filepaths = ['/home/jackreid/Documents/School/Research/Space Enabled/Code/Decisions/Auxilary Files/SummaryGraphs/Rio de Janeiro/NightlightsRelativeAnomaly_2020.csv',
             '/home/jackreid/Documents/School/Research/Space Enabled/Code/Decisions/Auxilary Files/SummaryGraphs/Rio de Janeiro/NightlightsRelativeAnomaly_Complete_NoIncrement.csv',
             '/home/jackreid/Documents/School/Research/Space Enabled/Code/Decisions/Auxilary Files/SummaryGraphs/Rio de Janeiro/NightlightsMean_Complete.csv']

filepath = filepaths[1]
    
#Get screen resolution, used for sizing the graphs later on
for m in get_monitors():
    print(str(m))
my_dpi = m.width/(m.width_mm*0.0393701)


#Extract data from the csv
datalist = []
with open(filepath, encoding='ISO-8859-15') as csvfile:
    readCSV1 = csv.DictReader(csvfile, delimiter=',')
    for row in readCSV1:
        newrow = dict()
        for entry in row.keys():
            if row[entry]:
                if entry not in ['Date_Name','Policy_Name']:
                    newrow[entry] = float(row[entry])
                elif entry in ['Date_Name']:
                    newrow[entry] = enddate = dateutil.parser.parse(row[entry])
            else:
                newrow[entry] = np.nan
        
        datalist.append(newrow)

#Convert data into a DataFrame for plotting purposes
df_data = pd.DataFrame(datalist)

#Sort the DataFrame by date
df_data = df_data[df_data['Date_Name'].notnull()].sort_values(by='Date_Name')

def main():
    x = np.array(df_data['Date_Name'])
    fig, ax = plt.subplots()
    nightlight_places = []
    for key in df_data.keys():
        if key not in ['Date_Name']:
            nightlight_places.append(key)
            
    for place in nightlight_places:
        y = np.array(df_data[place])
        ymask = np.isfinite(y)
        ax.plot(x[ymask], y[ymask], label=place)

    ax.legend(loc='upper left', bbox_to_anchor=(1.05, 1),
              ncol=2, borderaxespad=0)
    fig.subplots_adjust(right=0.55)
    fig.suptitle('Right-click to hide all\nMiddle-click to show all',
                 va='top', size='large')

    leg = interactive_legend()
    return fig, ax, leg

def interactive_legend(ax=None):
    if ax is None:
        ax = plt.gca()
    if ax.legend_ is None:
        ax.legend()

    return InteractiveLegend(ax.get_legend())

class InteractiveLegend(object):
    def __init__(self, legend):
        self.legend = legend
        self.fig = legend.axes.figure

        self.lookup_artist, self.lookup_handle = self._build_lookups(legend)
        self._setup_connections()

        self.update()

    def _setup_connections(self):
        for artist in self.legend.texts + self.legend.legendHandles:
            artist.set_picker(10) # 10 points tolerance

        self.fig.canvas.mpl_connect('pick_event', self.on_pick)
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)

    def _build_lookups(self, legend):
        labels = [t.get_text() for t in legend.texts]
        handles = legend.legendHandles
        label2handle = dict(zip(labels, handles))
        handle2text = dict(zip(handles, legend.texts))

        lookup_artist = {}
        lookup_handle = {}
        for artist in legend.axes.get_children():
            if artist.get_label() in labels:
                handle = label2handle[artist.get_label()]
                lookup_handle[artist] = handle
                lookup_artist[handle] = artist
                lookup_artist[handle2text[handle]] = artist

        lookup_handle.update(zip(handles, handles))
        lookup_handle.update(zip(legend.texts, handles))

        return lookup_artist, lookup_handle

    def on_pick(self, event):
        handle = event.artist
        if handle in self.lookup_artist:

            artist = self.lookup_artist[handle]
            artist.set_visible(not artist.get_visible())
            self.update()

    def on_click(self, event):
        if event.button == 3:
            visible = False
        elif event.button == 2:
            visible = True
        else:
            return

        for artist in self.lookup_artist.values():
            artist.set_visible(visible)
        self.update()

    def update(self):
        for artist in self.lookup_artist.values():
            handle = self.lookup_handle[artist]
            if artist.get_visible():
                handle.set_visible(True)
            else:
                handle.set_visible(False)
        self.fig.canvas.draw()

    def show(self):
        plt.show()

if __name__ == '__main__':
    fig, ax, leg = main()
    plt.show()
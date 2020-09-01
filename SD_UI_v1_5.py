#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 11:08:59 2020

@author: jackreid
"""

#Import tkinter and other visualization packages
import tkinter as tk
import tkinter.font
import tkinter.ttk
from tkinter import Widget
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
style.use('ggplot')
import matplotlib.pyplot as plt

#Import other auxilary pacakges
import csv
import numpy as np
import shapefile

#Import custom packages
import SDlib_v1_4 as SDlib
import MapWindow_v4 as MapWindow



# =============================================================================
#  SD_UI Class               
# =============================================================================

class SD_UI(tk.Tk):
    
    def __init__(self, master=None, **kwargs):        
        """INITIATE SD_UI CLASS
        
        Args:
            SD_Map: an instance of a SD_System class which represents the system dyanmics causal map
            master: optional argument identifying a parent tkinter window. If omited, the SD_UI class will be the parent window
        
        Returns:
            N/A
        """
        
        #Generate window and assign to appropriate master        
        tk.Tk.__init__(self, master)
        
        #Set default colors for windows and widgets
        self.default_background='#856ff8'
        self.highlight_color='#0711a3'
        self.button_color='#b1a4f5'
        self.configure(bg=self.default_background)
                
                  

        #Load keyword arguments
        if 'tuning' in kwargs:
            self.tuning_flag = kwargs.pop('tuning')
        else:
            self.tuning_flag = 0
        if 'location' in kwargs:
            self.location = kwargs.pop('location')
        else:
            self.location = 'Rio de Janeiro'
            
        if self.location == 'Rio de Janeiro':
            # self.shpfilepath = './Data/Brazil/Shapefiles/Bairros_AQ.shp'
            # self.background_image = self.map_image.filepaths[self.map_image.setting_index.get()]
            self.color_range =  'PM10'
            self.default_graph1 = 'Measured Total Infected Population'
            self.default_graph2 = 'Hospitalized Population'
            self.map_loc = [-43.1, -23.0, 0.01]
            # self.data_filepath = './Data/Brazil/Brazil_Data.csv'
            # self.shp_fields =  './Data/Brazil/shp_fields.csv'
            self.language = 'portuguese'
        elif self.location == 'Chile':
            # self.shpfilepath = './Data/Chile/Shapefiles/Regions_data_simple.shp'
            # self.background_image = self.map_image.filepaths[self.map_image.setting_index.get()]
            self.color_range =  'Población'
            self.default_graph1 = 'Measured Total Infected Population'
            self.default_graph2 = 'Hospitalized Population'
            self.map_loc = [-35.0, -50.0, 0.0001]
            # self.data_filepath = './Data/Chile/Chile_Data.csv'
            # self.shp_fields =  './Data/Chile/shp_fields.csv'
            self.language = 'spanish'
        elif self.location == 'Indonesia':
            # self.shpfilepath = './Data/Indonesia/Shapefiles/Regions_data.shp'
            # self.background_image = self.map_image.filepaths[self.map_image.setting_index.get()]
            self.color_range =  'Total Cases'
            self.default_graph1 = 'Measured Infected Population'
            self.default_graph2 = "'True' Infected Population"
            self.map_loc = [140.0,-12.0, 0.00016]
            # self.data_filepath = './Data/Indonesia/Indonesia_Data.csv'
            # self.shp_fields =  './Data/Indonesia/shp_fields.csv'
            self.language = 'english'
        elif self.location == 'Santiago':
            # self.shpfilepath = './Data/Santiago/Shapefiles/Metro_comunas_simple_data.shp'
            self.color_range = 'PM10'
            self.default_graph1 = 'Measured Infected Population'
            self.default_graph2 = "'True' Infected Population"
            self.map_loc = [-69.0, -34.0, 0.0025]
            # self.data_filepath = './Data/Santiago/Santiago_Data.csv'
            # self.shp_fields =  './Data/Santiago/shp_fields.csv'
            self.language = 'spanish'
            
        self.translations = './translations.csv' 
        self.data_filepath = './Data/' + self.location + '/temporal_data.csv'
        self.shp_fields = './Data/' + self.location + '/shp_fields.csv'
        self.shpfilepath = './Data/' + self.location + '/Shapefiles/geographic_data.shp'
        
    
        if 'language' in kwargs:
            self.language = kwargs.pop('language')
            
        #Set geometry and other parameters of the window
        self.title(self.translate('System Dynamics Visualization'))
        default_font = tk.font.nametofont("TkDefaultFont")
        default_font.configure(size=20)
        pad=3
        self._geom='200x200+0+0'
        self.geometry("{0}x{1}+0+0".format(
            self.winfo_screenwidth()-pad, self.winfo_screenheight()-pad))
        self.bind('<Escape>',self.toggle_geom)  
    
    
        #Label the SD_Map input for easy reference
        self.SD_Map = SDlib.SD_System(tuning_flag=self.tuning_flag,
                                      location=self.location,
                                      data_filepath=self.data_filepath)
        
        #Initialize the time series list and associated function(s)
        if self.tuning_flag == 1:
            self.timeSeries=[0]
        else:
            maxtimelist = []
            
            SD_dict = self.SD_Map.__dict__.copy()
#            del SD_dict['location']

            for SDattribute in SD_dict:
                maxtimelist.append(len(self.SD_Map.__dict__[SDattribute].values))
            maxtime = max(maxtimelist)
            self.timeSeries = list(range(0,maxtime))
            
            for SDattribute in SD_dict:
                vallen = len(self.SD_Map.__dict__[SDattribute].values)
                timelen = len(self.timeSeries)
                if vallen < timelen:
                    timedif = timelen - vallen
                    list_add = [self.SD_Map.__dict__[SDattribute].values[-1]] * timedif
                    self.SD_Map.__dict__[SDattribute].values[0:0] = list_add
        
        self.timestep = lambda: self.timeSeries[-1] - self.timeSeries[-2]

        #Generate the top menus
        self.make_top_menus()
        
        #Pull from the SD_Map various attributes for easy reference
        self.ClosureDict = self.SD_Map.ClosureDict(self.location) #dictionary relating string closure policy to numerical value
        self.ClosureDictInv = self.SD_Map.ClosureDictInv(self.location) #dictionary relating numerical closure policy to string value
        self.SocialDisDict = self.SD_Map.SocialDisDict() #dictionary relating string social distancing policy to numerical value
        self.SocialDisDictInv = self.SD_Map.SocialDisDictInv() #dictionary relating numerical social distancing policy to string value
        self.CatColorDict, self.colormap, self.norm = self.SD_Map.CatColor() #information relating categories to colors for visualization
        
        #Generate the four graphs and their associated dropdown menus
        self.graph_setting_list = [[],[]]
        self.graph_canvas_list = [[],[]]
        self.graph_optionlist_list = [[],[]]
        self.graph_frame_L = self.make_graph_frame(self.default_graph1, self.default_graph2, 0) #left pair of graphs
        # self.graph_frame_R = self.make_graph_frame('Employment Rate', 'Daily Emissions Rate', 1) #right pair of graphs
        # self.graph_frame_L = self.make_graph_frame('Closure Policy', 'Hospitalized Population', 0) #left pair of graphs

        #Generate the policy action controls
        self.control_frame = self.make_control_frame()
        
        #Generate the decision rules and their associated display
        self.make_rules()
        self.info_frame = self.make_rule_display()
        
        self.frame_map, self.subframe_map, self.MAP = self.make_map_frame()
        

    def toggle_geom(self,event):
        """TOGGLE FULL SCREEN DISPLAY
        
        Args:
            event: triggering event
    
        Returns:
            N/A
        """
        
        geom=self.winfo_geometry()
        print(geom,self._geom)
        self.geometry(self._geom)
        self._geom=geom
        
    def translate(self,phrase, **kwargs):
        """TRANSLATES STRINGS TO APPROPRIATE LANGUAGE
        
        Args:
            phrase: string to be translated
            input_language: optional, specifies the original language of the phrase. Defaults to English
            output_language: optional, specifies the output language of the phrase. Defaults to whatever self.language is set to.
    
        Returns:
            N/A
        """
        
        #Load the input and output languages
        if 'output_language' in kwargs:
            out_lang = kwargs.pop('output_language')
        else:
            out_lang = self.language
            
        if 'input_language' in kwargs:
            in_lang = kwargs.pop('input_language')
        else:
            in_lang = 'english'
            
        #Identify the language based on intput
        if out_lang in ['Spanish', 'spanish', 'Espanol', 'espanol', 's', 'S']:
            output_language = 'spanish'
        elif out_lang in ['Portuguese', 'portuguese', 'Português', 'português', 'p', 'P']:
            output_language = 'portuguese'
        elif out_lang in ['English', 'english', 'E', 'e']:
            output_language = 'english'
        else:
            output_language = 'english'
            print('Unable to find language:', out_lang)
        
        #Open CSV with translations
        with open(self.translations) as csv_file:
           csvread = csv.DictReader(csv_file)
           found = 0
           for row in csvread:
               if row[in_lang] == phrase:
                   output_phrase = row[output_language] #translate phrase
                   found = 1 #set flag indicating that the phrase was successfully translated

        #If no translation was found, return original phrase and present an error message
        if found == 0:
            output_phrase = phrase
            print('Unable to find phrase ', phrase, "in language ", out_lang)
            
        return output_phrase

# =============================================================================
#  Generate the Top Menu             
# =============================================================================   

    def make_top_menus(self):
        menubar = tk.Menu(self)

        # create a pulldown menu, and add it to the menu bar
        language_menu = tk.Menu(menubar, tearoff=0)
        language_menu.add_command(label=self.translate("English"), command=lambda: self.replace_language('english'))
        language_menu.add_command(label=self.translate("Spanish"), command=lambda: self.replace_language('spanish'))
        language_menu.add_command(label=self.translate("Portuguese"), command=lambda: self.replace_language('portuguese'))
        menubar.add_cascade(label=self.translate("Languages"), menu=language_menu)
        
        # create more pulldown menus
        menubar.add_command(label=self.translate("Exit"), command=self.destroy)
        
        # display the menu
        self.config(menu=menubar)
        
    def replace_language(self, new_language):
        
        self.destroy()
        
        #Generate user interface
        UI = SD_UI(tuning = self.tuning_flag,
                    location = self.location,
                    language = new_language)
    
        #Run the user interface
        UI.mainloop()
        
# =============================================================================
#  Generate the Graphs             
# =============================================================================

    def make_graph_frame(self, firstgraph, secondgraph, col):
        """GENERATE A FRAME WITH A PAIR OF GRAPHS AND ASSOCIATED DROPDOWN MENUS
        
        Args:
            firstgraph: name of the top graph to be generated
            secondgraph: name of the bottom graph to be generated
            col: index of the column that these graphs will appear in
    
        Returns:
            graph_frame: parent frame for the vertical pair of graphs and their associated dropdown menus
        """
        
        #Generate frame to house graphs and dropdowns, situate in appropriate column
        #self.screenwidth = self.winfo_screenwidth()
        #self.screenheight = self.winfo_screenwidth()
        #width=self.screenwidth*.75, height=self.screenheight*.75
        graph_frame = tk.Frame(self, width=500, height=300,
                               padx = 5, pady = 5, 
                               # borderwidth=1, relief='groove',
                               bg=self.default_background)
        graph_frame.grid(column=col, row=0)
        # graph_frame.grid_propagate(0)
        
        #Generate the top graph label and dropdown menu
        index = 0
        graph_label = tk.Label(graph_frame, text=self.translate('Graph 1: '), font=('Aria',24),
                               bg=self.default_background)
        graph_label.grid(column=0, row=0)
        graph_optionlist = self.make_graph_dropdown(graph_frame, firstgraph, index, col)
        graph_optionlist.grid(column=1, row=0)
        self.graph_optionlist_list[col].append(graph_optionlist)
        self.figures = []
        #Generate the top graph
        canvas, fig = self.make_graph(graph_frame, firstgraph)
        self.graph_canvas_list[col].append(canvas)
        self.figures.append(fig)
        
        #Generate the bottom graph label and dropdown menu
        index = 1
        graph_label = tk.Label(graph_frame, text=self.translate('Graph 2: '), font=('Arial',24),
                               bg=self.default_background)
        graph_label.grid(column=0, row=3)        
        graph_optionlist = self.make_graph_dropdown(graph_frame, secondgraph, index, col)
        graph_optionlist.grid(column=1, row=3)
        self.graph_optionlist_list[col].append(graph_optionlist)
        
        #Generate the bottom graph
        canvas,fig = self.make_graph(graph_frame, secondgraph)
        self.graph_canvas_list[col].append(canvas)
        self.figures.append(fig)
        
        return graph_frame
    
    def make_graph_dropdown(self, frame, defaultsetting, index, col):
        """GENERATE A DROPDOWN MENU FOR CONTROLLING A GRAPH
        
        Args:
            frame: frame to situate the dropdown menu in
            defaultsetting: name of the initial graph to be displayed
            index: indicator for if the graph is top (index = 0) or bottom (index = 1)
            col: index of the column that these graphs will appear in
    
        Returns:
            graph_optionlist: tkinter dropdown menu object
        """
        
        #Get all SD objects from the SD Map
        SD_dict = self.SD_Map.__dict__.copy()
#        del SD_dict['location']
        
        #Generate a list of the categories of all the SD objects
        categorylist = []
        for SDobject in SD_dict:
            categoryname = self.SD_Map.__dict__[SDobject].category
            categorylist.append(categoryname)
        
        #Filter the category list for only unique entries (one of each category)
        uniquecategories = list(set(categorylist))
        uniquecategories.sort()
        
        #Initalize an empty dictionary where each key is a category
        catdict=dict()
        for entry in uniquecategories:
            catdict[entry] = []
        
        #Fill the dictionary with all of the SD objects associated with each category
        for SDobject in SD_dict:
            categoryname = self.SD_Map.__dict__[SDobject].category
            obname = self.SD_Map.__dict__[SDobject].name
            catdict[categoryname].append(self.translate(obname))
                            
        #Initalize the tkinter variable associated with the dropdown menu
        graph_setting_default = defaultsetting
        graph_setting_name = tk.StringVar()
        graph_setting_name.set(self.translate(graph_setting_default))
        
        
        #Identify the initial background color of the dropdown menu
        normvalue = self.norm(self.CatColorDict[self.SD_Map.retrieve_ob(graph_setting_default).category])
        fill1 = self.colormap(normvalue)[0:3]
        fill = [int(x*255) for x in fill1]
        fill = self.rgb2hex(fill)
        
        #Initialize the dropdown menu
        graph_optionlist = tk.Menubutton(frame, textvariable=graph_setting_name, 
                                        indicatoron=False,
                                        background=fill,
                                        width=52)
        
        #Fill the dropdown menu with the category cascade menus and the specific objects in the appropriate categories
        topMenu = tk.Menu(graph_optionlist, tearoff=False)
        graph_optionlist.configure(menu=topMenu)
        graph_optionlist.configure(width=45)
        for key in sorted(catdict.keys()):
            
            #Identify the color of each category in menu
            normvalue = self.norm(self.CatColorDict[key])
            fill1 = self.colormap(normvalue)[0:3]
            fill = [int(x*255) for x in fill1]
            fill = self.rgb2hex(fill)
            
            #Add a cascade menu for the category
            menu = tk.Menu(topMenu)
            topMenu.add_cascade(label=self.translate(key), menu=menu, background=fill)

            #Populate the cascade menu with each specific object button
            for value in catdict[key]:
                menu.add_radiobutton(label=value, variable = graph_setting_name, 
                                      value=value,
                                      background=fill,
                                      command=lambda : self.replace_fig(index, col) 
                                      )
                
        #Store the dropdown setting variable for future reference
        self.graph_setting_list[col].append(graph_setting_name)
        
        return graph_optionlist

    def make_graph(self, frame, obname, **kwargs):
        """GENERATE A FIGURE AND A CANVAS FOR IT TO RESIDE IN
        
        Args:
            frame: frame to situate the figure frame in
            obname: name of the SD object to be graphed
            gridpos: optional argument identifying the row to place the frame, default is at the bottom of the parent frame
    
        Returns:
            canvas: the canvas housing an individual graph
        """
        
        #Generate the figure
        fig = self.make_fig(obname)
        
        #Identify the location to place the figure
        if 'gridpos' in kwargs:
            newrow = kwargs.pop('gridpos')
        else:
            newrow = frame.grid_size()[1]      
            
        #Generate a frame specifically for the figure (this prevents resizing when the figure is updated)
        canvas_frame = tk.Frame(frame,width=500, height=300)
        canvas_frame.grid(column=0, row=newrow+1, columnspan=2)
        
        #Generate a canvas and place the figure in it
        canvas = FigureCanvasTkAgg(fig, master=canvas_frame)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().grid(column=0, row=0)

        return canvas, fig
    
    def make_fig(self, graph_setting):
        """GENERATE FIGURE PLOTTING OBJECT VALUES OVER TIME
        
        Args:
            graph_setting: name of SD object to be plotted
    
        Returns:
            fig: matplotlib figure object
        """
        
        #Initialize Figure
        self.screenwidth = self.winfo_screenwidth()
        self.screenheight = self.winfo_screenwidth()
        # fig = Figure(figsize=(self.screenwidth/202.5, self.screenheight/372.4), dpi=100)
        #fig = Figure(figsize=(7.75, 2.5), dpi=100)
        # fig, ax1 = plt.subplots(figsize=(self.screenwidth/495.48, self.screenheight/1536))
        fig, ax1 = plt.subplots(figsize=(self.screenwidth/384, self.screenheight/1097))

        # fig, ax1 = plt.subplots(figsize=(7.75, 2.5))
        # (7.75 and 2.5 are the values that work on Shea's monitor)
        
        
        #Retrieve SD Object based on name
        SDob = self.SD_Map.retrieve_ob(graph_setting)
        
        plotval = []
        if type(SDob.values) is list:
            plotval.extend(SDob.values)
        else:
            plotval.append(SDob.values)
        if True in [True if x==[] else False for x in plotval]:
            # print(SDob.name)
            # print(SDob.values)
            plotval[:] = [x if x != [] else np.nan for x in plotval]
            
        
        #Identify color to use for plotting based on SD object's category
        normvalue = self.norm(self.CatColorDict[SDob.category])
        fill1 = np.array([self.colormap(normvalue)[0:3]])

        #Generate scatterplot
        # ax1 = fig.add_subplot(111)
        
        histTime = list(range(0,len(SDob.history)))
        histval = []
        histval.extend(SDob.history)
        if True in [True if x==[] else False for x in histval]:
            histval[:] = [x if x != [] else np.nan for x in histval]
            
        if self.tuning_flag == 1:
            ax1.scatter(self.timeSeries, plotval, c=fill1, marker="s", label = self.translate('Simulation'))
            ax1.scatter(histTime, histval, edgecolors=fill1, marker="o", label = self.translate('History'), facecolors='none')
            
        else:
            ax1.scatter(histTime, histval, edgecolors=fill1, marker="o", label = self.translate('History'), facecolors='none')
            
            if len(self.timeSeries) > len(histTime):
                ax1.scatter(self.timeSeries[len(histTime):], plotval[len(histTime):], c=fill1, marker="s", label = self.translate('Simulation'))
            # ax1.scatter(self.timeSeries, plotval, c=fill1)
            # ax1.set_ylim(min(0, np.nanmin(plotval)), 1.2*np.nanmax(plotval))
        
        ax1.legend(loc='upper right')
        ax1.set_ylim(min(0, np.nanmin(plotval), np.nanmin(histval)), 1.2*max(np.nanmax(plotval), np.nanmax(histval)))
        endtime = max(self.timeSeries[-1], 200)
        ax1.set_xlim(0, endtime)
        ax1.set_ylabel(self.translate(SDob.units))
        ax1.set_xlabel(self.translate('Days'))
        fig.tight_layout()
        
        return fig
        
    def replace_fig(self, index, col):
        """REPLACE A GRAPH
        
        Args:
            index: index of vertical position of graph to be replaced, 0=top graph, 1=bottom graph
            col: column of the graph to be replaced, 0=left, 1=right
    
        Returns:
            N/A
        """
        
        #Identify the frame housing the specific graph and delete it
        framename = self.graph_canvas_list[col][index].get_tk_widget().master
        self.figures[index].clear()
        plt.close(self.figures[index])
        self.graph_canvas_list[col][index].get_tk_widget().destroy()
        
        
        #Identify the proper SD object to plot in replacement
        graph = self.translate(self.graph_setting_list[col][index].get(),
                          input_language = self.language,
                          output_language = 'english')
        
        #Generate the new graph and store it for future reference
        canvas,fig = self.make_graph(framename, graph,
                        gridpos = index*2+1)
        self.graph_canvas_list[col][index] = canvas
        self.figures[index] = fig
        
        #Set the dropdown menu background to its proper color
        SDob = self.SD_Map.retrieve_ob(graph)
        normvalue = self.norm(self.CatColorDict[SDob.category])
        fill1 = self.colormap(normvalue)[0:3]
        fill = [int(x*255) for x in fill1]
        fill = self.rgb2hex(fill)
        self.graph_optionlist_list[col][index].configure(background=fill)
        
    def rgb2hex(self,color):
        """CONVERTS A LIST OR TUPLE OF RGB COORDINATES TO A HEX STRING
    
        Args:
            color (list|tuple): the list or tuple of integers (e.g. (127, 127, 127))
    
        Returns:
            str:  the rgb string
        """
        
        return f"#{''.join(f'{hex(c)[2:].upper():0>2}' for c in color)}"
 
# =============================================================================
#  Generate the Map Frame             
# =============================================================================     
    def make_map_frame(self):
        frame_map = tk.Frame(self, width=500, height=400,
                             # borderwidth=1, relief='groove',
                             bg=self.default_background)
        frame_map.grid(column=1, row=0)
        # frame_map.grid_propagate(0)
        #Select specific UOA shapefile

            
            
        self.shps = [shapefile.Reader(self.shpfilepath)]
        
        
        # Make Color Fill Dropdown Menu
        self.color_optionlist =  self.make_fill_list(frame_map, self.shps[0])
        self.color_optionlist.configure(bg=self.button_color,
                                        highlightbackground=self.highlight_color)
        self.color_optionlist['menu'].config(bg=self.button_color)
        # self.color_optionlist.grid(column=0, row=0)
        self.color_optionlist.pack()
        
        
        color_title = self.translate(self.color_setting_name.get(),
                                     input_language = self.language,
                                     output_language = 'english')
        print(color_title)
        color_range = self.color_field_modes[self.color_longname_modes_inverted[color_title]]
        
        
        #Create Map and bind commands to it
        subframe_map = tk.Frame(frame_map,
                                bg=self.default_background)
        # subframe_map.grid(column=0, row=1)
        subframe_map.pack()
        MAP = MapWindow.Map(subframe_map,
                            self.shps,
                            # background_image = self.background_image, 
                            color_range= [color_range],
                            color_title= color_title,
                            lat_lon_zoom= self.map_loc,
                            null_zeros=1)
        
        MAP.configure(bg='white')
        
        # MAP.bind("<Button-1>", self.print_coords)
        # MAP.bind("<Double-Button-1>", lambda e: self.uoa_type(self.clickname))
        return frame_map, subframe_map, MAP
    
    def make_fill_list (self, root, shp):    
        """CREATE UOA FILL COLOR TOGGLE
    
        Args:
            root: tk frame for the dropdown to to be situated in.
               
        Returns:
            zoneoptionlist: the dropdown list
        """
        
        #Identify fields, longnames, and categories to be added to the dropdown
        shortfieldlist = []
        longfieldlist = []
        categorylist = []
        for field in shp.fields:
            fieldname = field[0]
            testfield = self.fieldnamelookup(fieldname, self.shp_fields)
            if testfield.fieldname != []:
                shortfieldlist.append(testfield.fieldname)
                longfieldlist.append(testfield.longname)
                categorylist.append(testfield.category)
            
            
        #Create a index:field dictionary and a index:longname dictionary (and inverses)
        self.color_field_modes = dict(list(enumerate(shortfieldlist)))
        # self.color_field_modes[0] = 'Nenhum'
        self.color_field_modes_inverted = dict(map(reversed, self.color_field_modes.items()))
        
        self.color_longname_modes = dict(list(enumerate(longfieldlist)))
        # self.color_longname_modes[0] = 'Nenhum'
        self.color_longname_modes_inverted = dict(map(reversed, self.color_longname_modes.items()))

        
        #Create UOA Color Fill Dropdown
        self.color_setting_name = tk.StringVar()
        self.color_setting_name.set(self.translate(self.color_range))
    
        translated_color_list = []
        for entry in self.color_longname_modes_inverted.keys():
            translated_color_list.append(self.translate(entry))
        
        color_optionlist = tk.OptionMenu(root, self.color_setting_name,
                           *list(translated_color_list),
                            command=lambda e: self.replace_map_image(self.subframe_map)
                            )
                           
                           
        
    
        #Return dropdown for future reference
        return color_optionlist 
    
    class fieldnamelookup:
    
        def __init__(self, fieldname, shp_fields, **kwargs):
            
            import csv
            self.fieldname = []
            self.longname = []
            self.type = []
            self.choices = []
            self.category = []
            
               
            #Appropriately label Other field
            with open(shp_fields) as csv_file:
               csvread = csv.DictReader(csv_file)
               for row in csvread:
                   if row['FieldName'] == fieldname:
                       self.fieldname = fieldname
                       self.longname = row['LongName']
                       self.category = row['Category']
                       self.type = 'Other'
    
    def replace_map_image(self, mapframe, **kwargs):
        """UPDATE MAP TO CURRENT SETTINGS
    
        Args:
            N/A
            [Note, this function depends primarily on the current values for 
            mapsetting, zone_color_metricsetting, and mangrovesetting]
               
        Returns:
            N/A
        """
        

        
        #Pull settings into more usable formats
        fill_color_title = self.translate(self.color_setting_name.get(),
                                          input_language=self.language,
                                          output_language='english')
        fill_color = self.color_field_modes[self.color_longname_modes_inverted[fill_color_title]]
        
        #Delete exisiting map
        self.MAP.delete("all")
        slaveitems = mapframe.slaves()
        for item in slaveitems:
            item.destroy()    
        griditems = mapframe.grid_slaves()
        for item in griditems:
            item.destroy()
            
        self.MAP = MapWindow.Map(mapframe,
                            self.shps,
                            # background_image = self.background_image, 
                            color_range = [fill_color],
                            color_title = fill_color_title,
                            lat_lon_zoom = self.map_loc,
                            null_zeros=1)
                
        self.MAP.configure(bg='white')
        # #Bind commands to the map
        # self.MAP.bind("<Button-1>", self.print_coords)       
        # self.MAP.bind("<Double-Button-1>", lambda e: self.uoa_type(self.clickname))
        
        
        


       
# =============================================================================
#  Generate the Control Frame             
# =============================================================================

    def make_control_frame(self):
        """GENERATE THE POLICY CONTROLS FOR THE SIMULATION
        
        Args:
            N/A
    
        Returns:
            control_frame: tkinter frame housing the controls
        """
        
        #Generate and place the frame for housing the controls
        control_frame = tk.Frame(self, padx = 0,
                                 bg=self.default_background)
        control_frame.grid(column=0, row=4, columnspan = 1)
        
        #Generate the time indicator
        time_label = tk.Label(control_frame, text=self.translate('Day')+': ', font=('Arial',24),
                              bg=self.default_background)
        time_label.grid(column=0, row=0)
        self.timev = tk.StringVar()
        self.timev.set(str(self.timeSeries[-1]))
        self.time_value_label = tk.Label(control_frame, textvariable=self.timev, font=('Arial',24),
                                         bg=self.default_background)
        self.time_value_label.grid(column=1, row=0, sticky='W')
        
        boxwidth = 30
        
        #Generate the Closure Policy control dropdown
        option1_label = tk.Label(control_frame, text=self.translate('Closure Policy')+': ', font=('Arial',24),
                                 bg=self.default_background)
        option1_label.grid(column=0, row=1)
        option1_list = list(self.ClosureDict.keys())
        
        self.option1_var = tk.StringVar()
        self.option1_var.set(option1_list[0])
        option1_menu = tk.OptionMenu(control_frame, self.option1_var, 
                          *option1_list, 
                           command=lambda _: self.update_ClosureP()
                          )
        option1_menu.config(width=boxwidth, anchor='w',
                            bg=self.button_color,
                            highlightbackground=self.highlight_color)
        option1_menu['menu'].config(bg=self.button_color)
        option1_menu.grid(column=1, row=1, columnspan=2)
        
        #Generate the Social Distancing Policy control dropdown
        option2_label = tk.Label(control_frame, text=self.translate('Social Distancing Policy')+': ', font=('Arial',24),
                                 bg=self.default_background)
        option2_label.grid(column=0, row=2)
        option2_list = list(self.SocialDisDict.keys())
        
        self.option2_var = tk.StringVar()
        self.option2_var.set(option2_list[0])
        option2_menu = tk.OptionMenu(control_frame, self.option2_var, 
                          *option2_list, 
                           command=lambda _: self.update_SocialDisP()
                          )
        option2_menu.config(width=boxwidth, anchor='w',
                            bg=self.button_color,
                            highlightbackground=self.highlight_color)
        option2_menu['menu'].config(bg=self.button_color)
        option2_menu.grid(column=1, row=2, columnspan=2)
        
        #Generate the ventilator ordering entry box
        option3_label = tk.Label(control_frame, text=self.translate('Order New Ventilators')+': ', font=('Arial',24),
                                 bg=self.default_background)
        option3_label.grid(column=0, row=3)
        self.option3_var = tk.IntVar()
        self.option3_var.set(0)
        FontOfEntryList=tkinter.font.Font(family="Arial", size=24)
        self.option3_menu = tk.Entry(control_frame, font=FontOfEntryList,
                                     highlightbackground=self.highlight_color)
        self.option3_menu.insert(0,self.option3_var.get())
        self.option3_menu.configure(width=5)
        self.option3_menu.grid(column=1, row=3, sticky='W')

        #Generate the Next Week simulation button
        run_button = tk.Button(control_frame, text=self.translate('Next Week'), 
                               command = lambda: self.increment_time(),
                               font=('Arial',24),
                               bg=self.button_color,
                               highlightbackground=self.highlight_color)
        run_button.grid(column=0, row=4, columnspan=2)
        
        #Generate the Run Autonomously button
        automatic_button = tk.Button(control_frame, text=self.translate('Run Autonomously'), 
                               command = lambda: self.automatic_window(),
                               font=('Arial',24),
                               bg=self.button_color,
                               highlightbackground=self.highlight_color)
        automatic_button.grid(column=0, row=5, columnspan=2)
        
        #Generate the Clear Simulation Button
        clear_button = tk.Button(control_frame, text = self.translate('Clear Simulation'),
                                 command = lambda: self.clear_simulation(),
                                 font=('Arial',24),
                                 bg=self.button_color,
                                 highlightbackground=self.highlight_color)
        clear_button.grid(column=0, row=6, columnspan=2)
        
        return control_frame
    
    def update_ClosureP(self):
        """UPDATES THE CURRENT CLOSURE POLICY
        
        Args:
            N/A
    
        Returns:
            N/A
        """
        
        self.SD_Map.ClosureP.values[-1] = self.ClosureDict[self.option1_var.get()]
    
    def update_SocialDisP(self):
        """UPDATES THE SOCIAL DISTANCING POLICY
        
        Args:
            N/A
    
        Returns:
            N/A
        """
        
        self.SD_Map.SocialDisP.values[-1] = self.SocialDisDict [self.option2_var.get()]

    def increment_time(self, **kwargs):
        """RUN SIMULATION FOR SPECIFIED NUMBER OF TIME INCREMENTS
        
        Args:
            timerange: optional, specifies the number of times to simulate into the future, default is 7 (1 week)
            display: optional, flag indicating whether to update the graphs, default is 1 (yes)
            auto: optional, flag indicating whether the simulation is being run autonomously, default is 0 (no)
            triggered: optional, list of decision rules that have been trigerred, default is [] (no rules)
    
        Returns:
            N/A
        """
        
        #Pull all optional keyword arguements
        if 'timerange' in kwargs:
            timerange = kwargs.pop('timerange')
        else:
            timerange = 7
            
        if 'display' in kwargs:
            displayflag = kwargs.pop('display')
        else:
            displayflag = 1
            
        if 'auto' in kwargs:
            autoflag = kwargs.pop('auto')
        else:
            autoflag = 0
        
        if 'triggered' in kwargs:
            triggered_rules = kwargs.pop('triggered')
        else:
            triggered_rules = []
            
        #Run simulation one day at a time until specified end point is reached
        count = range(0,timerange)
        for i in count:
            
            #If being run manually, read the new vent orders once and then clear the entry box
            if autoflag != 1:
                if i == 0:
                    self.SD_Map.NewOVents.values[-1] = int(self.option3_menu.get())
                    self.option3_menu.delete(0, tk.END)
                    self.option3_menu.insert(0, 0)
           
            #Increment one day if at least one infected person remains. If not, end the simulation
            if self.SD_Map.IPop.value() > 1:
                time = self.timeSeries[-1]
                self.timeSeries.append(time+1)
                self.SD_Map.update_all(self.timestep(), len(self.timeSeries)-2)
            else:
                print('Done!')
                
        #Update the time display
        self.timev.set(self.timeSeries[-1])
               
        #Add any triggered rules to the rule log display
        if triggered_rules != []:
            day_text = self.translate('Day')+'  ' + str(self.timeSeries[-1]) 
            rule_text = '; ' + self.translate('Rules') + ': ' + str(triggered_rules)[1:-1]
            log_text = day_text + rule_text
            self.list_info_boxes['Log'].insert(tk.END, log_text)
        
        #If appropriate, update all of the graphs
        if displayflag == 1:
            index = 0
            
            #Select all of the graphs
            canvaslist = []
            for entrylist in self.graph_canvas_list:
                for entry in entrylist:
                    canvaslist.append(entry)
            
            #For each graph, delete it and replace it with an update graph
            for canvas in canvaslist:

                if index < 2:
                    col = 0
                    inputindex = index
                    self.figures[index].clear()
                    plt.close(self.figures[index])
                else:
                    col = 1
                    inputindex = index - 2
                framename = canvas.get_tk_widget().master
                canvas.get_tk_widget().destroy()
                graph = self.translate(self.graph_setting_list[col][inputindex].get(),
                                       input_language=self.language,
                                       output_language='english')
                canvas,fig = self.make_graph(framename, graph,
                            gridpos = inputindex*2+1)
                self.graph_canvas_list[col][inputindex]=canvas
                self.figures[index] = fig
                index += 1
           
    def automatic_window(self):
        """GENERATE RUN AUTONOMOUSLY DURATION INPUT WINDOW
        
        Args:
            N/A
    
        Returns:
            N/A
        """
        
        #Create window and label
        automatic_window = tk.Toplevel(self)
        windowtext = self.translate('How many days do you want the simulation to run for?') 
        automatic_window.title(windowtext)
        automatic_window.config(bg=self.default_background)
        lbl_text = tk.Label(automatic_window, text=windowtext,font=('Arial',24),
                            bg=self.default_background)
        lbl_text.grid(column=0, row=0)
            
        #Create input box
        self.auto_var = tk.IntVar()
        self.auto_var.set(1)
        FontOfEntryList=tkinter.font.Font(family="Arial",size=24)
        auto_menu = tk.Entry(automatic_window, font=FontOfEntryList)
        auto_menu.insert(0,0)
        auto_menu.configure(width=5)
        auto_menu.grid(column=0, row=1)

        #Create button to initate the simulation
        auto_run_button = tk.Button(automatic_window, text=self.translate('Run Simulation'), 
                               command = lambda: self.auto_run(automatic_window, int(auto_menu.get())),
                               font=('Arial',24),
                               bg=self.button_color,
                               highlightbackground=self.highlight_color)
        auto_run_button.grid(column=0, row=2)
        
        #Center the window on the screen (only works with 1 monitor)
        automatic_window.withdraw()
        automatic_window.update_idletasks()  # Update "requested size" from geometry manager
        x = (automatic_window.winfo_screenwidth() - automatic_window.winfo_reqwidth()) / 2
        y = (automatic_window.winfo_screenheight() - automatic_window.winfo_reqheight()) / 2
        automatic_window.geometry("+%d+%d" % (x, y))
        automatic_window.deiconify()
        
    def auto_run(self, wind, runtime):
        """RUN SIMULATION AUTONOMOUSLY
        
        Args:
            wind: tkinter window for inputing run duration
            runtime: the input run duration
    
        Returns:
            N/A
        """
        
        #Save runtime
        self.auto_var.set(runtime)
        
        #Define class for storing all conditional decision inputs
        class RuleInputs:
            def __init__(self, mIPop,
                         ClosureVal,
                         SocialDisVal,
                         mInfectR,
                         HPop,
                         Vents):
                
                self.mIPop = mIPop
                self.ClosureVal = ClosureVal
                self.SocialDisVal = SocialDisVal
                self.mInfectR = mInfectR
                self.HPop = HPop
                self.Vents = Vents
        
        
        #Run simulation for specified number of timesteps
        if runtime > 0:
            displayflag = 0
            for i in range(0,runtime):
                
                #Store all conditional decision inputs in class
                if self.location in ['Chile', 'Rio de Janeiro']:
                    mIPop = self.SD_Map.mTotIPop.value()
                    HPop = self.SD_Map.HPop.value()
                    Vents = self.SD_Map.Vents.value()
                elif self.location in ['Santiago', 'Indonesia']:
                    mIPop = self.SD_Map.mIPop.value()
                    HPop = 0
                    Vents = 0

                ClosureVal = self.ClosureDictInv[self.SD_Map.ClosureP.value()]
                SocialDisVal = self.SocialDisDictInv[self.SD_Map.SocialDisP.value()]
                mInfectR = self.SD_Map.mInfectR.value()
                
                rule_input = RuleInputs(mIPop,
                                         ClosureVal,
                                         SocialDisVal,
                                         mInfectR,
                                         HPop,
                                         Vents)
                
                #Identify any decision rules that have been triggered
                triggered_rules = []
                for rule in self.Rules:
                    rule_flag = rule.func(rule_input)
                    if rule_flag == 1:
                        triggered_rules.append(rule.number)
                
                #At final timestep, update the graphs
                if i == runtime-1:
                    displayflag = 1
                   
                #Run the simulation one timestep
                self.increment_time(timerange = 1,
                                display = displayflag,
                                auto = 1,
                                triggered = triggered_rules)
                
        #Remove the run autonomously duration input window
        wind.destroy()
    
    def clear_simulation(self):
        
        self.SD_Map = SDlib.SD_System(tuning_flag=self.tuning_flag,
                                      location=self.location,
                                      data_filepath=self.data_filepath)
        
        #Initialize the time series list and associated function(s)
        if self.tuning_flag == 1:
            self.timeSeries=[0]
        else:
            maxtimelist = []
            
            SD_dict = self.SD_Map.__dict__.copy()
#            del SD_dict['location']

            for SDattribute in SD_dict:
                maxtimelist.append(len(self.SD_Map.__dict__[SDattribute].values))
            maxtime = max(maxtimelist)
            self.timeSeries = list(range(0,maxtime))
            
            for SDattribute in SD_dict:
                vallen = len(self.SD_Map.__dict__[SDattribute].values)
                timelen = len(self.timeSeries)
                if vallen < timelen:
                    timedif = timelen - vallen
                    list_add = [self.SD_Map.__dict__[SDattribute].values[-1]] * timedif
                    self.SD_Map.__dict__[SDattribute].values[0:0] = list_add
        
        self.timestep = lambda: self.timeSeries[-1] - self.timeSeries[-2]
        
        index = 0
        
        #Select all of the graphs
        canvaslist = []
        for entrylist in self.graph_canvas_list:
            for entry in entrylist:
                canvaslist.append(entry)
        
        #For each graph, delete it and replace it with an update graph
        for canvas in canvaslist:

            if index < 2:
                col = 0
                inputindex = index
                self.figures[index].clear()
                plt.close(self.figures[index])
            else:
                col = 1
                inputindex = index - 2
            framename = canvas.get_tk_widget().master
            canvas.get_tk_widget().destroy()
            graph = self.translate(self.graph_setting_list[col][inputindex].get(),
                                   input_language=self.language,
                                   output_language='english')
            canvas,fig = self.make_graph(framename, graph,
                        gridpos = inputindex*2+1)
            self.graph_canvas_list[col][inputindex]=canvas
            self.figures[index] = fig
            index += 1
            
        #Update the time display
        self.timev.set(self.timeSeries[-1])
            
        #Clear the Log
        self.list_info_boxes['Log'].delete(0, tk.END)
# =============================================================================
#  Generate the Info Display Frame             
# =============================================================================
 
    def make_rule_display(self):
        """MAKE RULE LIST AND LOG DISPLAY BOX
        
        Args:
            N/A
    
        Returns:
            info_frame: tkinter frame housing the rule display box
        """
        
        #Make and place Frame
        info_frame = tk.Frame(self,
                              bg=self.default_background)
        info_frame.grid(column=1, row=4)
        
        #Define Colors and Style for Rule Info Box
        style = tk.ttk.Style()
        style.theme_create( "yummy", parent="alt", settings={
                "TNotebook": {"configure": {"background": self.default_background } },
                "TNotebook.Tab": {
                    "configure": {"background": self.button_color ,
                                  "bordercolor": self.highlight_color},
                    "map":       {"background": [("selected",'#F0F0F0')]}   } } )
        
        style.theme_use("yummy")
        
        #Make Label and Tabs for the Rule Info Box
        list_tabparent = tk.ttk.Notebook(info_frame)
        list_tabparent.config(height=250)
        list_tabparent.grid(column=0, row=0)
        self.list_info_boxes=dict()
        self.list_info_boxes['Rules'] = tk.Listbox(list_tabparent, width=50)
        self.list_info_boxes['Log'] = tk.Listbox(list_tabparent, width=50)
        list_tabparent.add(self.list_info_boxes['Rules'], text = self.translate('Rules'))
        list_tabparent.add( self.list_info_boxes['Log'], text = self.translate('Log'))
        
        #Populate list of rules
        for rule in self.Rules:
            self.list_info_boxes['Rules'].insert(tk.END, self.translate('Rules') + ' ' + str(rule.number) + ': ' + self.translate(str(rule.name)))
            
        #Add scrollbar to the rule log display
        self.scrollbar = tk.Scrollbar(info_frame, orient='vertical',
                                          command=self.list_info_boxes['Log'].yview)
        self.scrollbar.grid(column=1, row=0, sticky='ns')
        self.list_info_boxes['Log'].config(yscrollcommand=self.scrollbar.set)
        
        return info_frame
 
 
# =============================================================================
#  Define the Catalog of Decision Rules             
# =============================================================================
    """Each decision rules follows a pattern, as follows
        
        Args:
            rule_intput: class holding all of the relevant input values for the decision conditions

        Conditional: Condition identifying when the rule is triggered
        
        Policy Effect: Policy changes that occur when the conditional is met
    
        Returns:
            output: a flag indicating if the conditional has been met (0=no, 1=yes)
        """
    
    """ BRAZIL RULES """
    def Br_Rule1func(self, rule_input):
        output = 0
        ClosureVal = self.ClosureDict[rule_input.ClosureVal]
        if rule_input.mIPop >= 20 and ClosureVal == 'No Closures' and rule_input.SocialDisVal == 'No Distancing':
            # print('Rule 1 Triggered')
            self.SD_Map.ClosureP.values[-1] = self.ClosureDict['Fase 3A']
            self.SD_Map.SocialDisP.values[-1] = self.SocialDisDict['Voluntary Social Distancing']
            output = 1
        return output
    def Br_Rule2func(self, rule_input):
        output = 0
        if rule_input.mIPop >= 100 and (rule_input.ClosureVal in ['No Closures', 'Fase 6', 'Fase 5', 'Fase 4', 'Fase 3B', 'Fase 3A']):
            # print('Rule 2 Triggered')
            self.SD_Map.ClosureP.values[-1] = self.ClosureDict['Fase 1'] 
            output = 1
        return output
    def Br_Rule3func(self, rule_input):
        output = 0
        if rule_input.mInfectR >= 100 and (rule_input.ClosureVal in ['No Closures', 'Fase 6', 'Fase 5', 'Fase 4', 'Fase 3B', 'Fase 3A', 'Fase 2', 'Fase 1' ]):
            # print('Rule 3 Triggered')
            self.SD_Map.ClosureP.values[-1] = self.ClosureDict['Lockdown']
            self.SD_Map.SocialDisP.values[-1] = self.SocialDisDict['Mandatory Social Distancing'] 
            output = 1
        return output
    def Br_Rule4func(self,rule_input):
        output = 0
        if rule_input.mIPop <= 500 and (rule_input.ClosureVal in ['Fase 2', 'Fase 1', 'Lockdown' ]):
            # print('Rule 4 Triggered')
            self.SD_Map.ClosureP.values[-1] = self.ClosureDict['Fase 3A']
            output = 1
        return output
    def Br_Rule5func(self, rule_input):
        output = 0
        if rule_input.mIPop <= 500 and rule_input.SocialDisVal == 'Mandatory Social Distancing':
            # print('Rule 5 Triggered')
            self.SD_Map.SocialDisP.values[-1] = self.SocialDisDict['Voluntary Social Distancing']   
            output = 1
        return output
    def Br_Rule6func(self, rule_input):
        output = 0
        if rule_input.HPop > 2.5 * rule_input.Vents:
            # print('Rule 6 Triggered')
            self.SD_Map.NewOVents.values[-1] = 5
            output = 1
        return output
    def Br_Rule7func(self, rule_input):
        output = 0
        if rule_input.HPop > 7 * rule_input.Vents:
            # print('Rule 7 Triggered')
            self.SD_Map.VWTP.values[-1] = 50000
            output = 1
        return output
    
    """ CHILE AND SANTIAGO RULES """
    def Ch_Rule1func(self, rule_input):
        output = 0
        ClosureVal = self.ClosureDict[rule_input.ClosureVal]
        if rule_input.mIPop >= 20 and ClosureVal == 'No Closures' and rule_input.SocialDisVal == 'No Distancing':
            # print('Rule 1 Triggered')
            self.SD_Map.ClosureP.values[-1] = self.ClosureDict['Paso 3']
            self.SD_Map.SocialDisP.values[-1] = self.SocialDisDict['Voluntary Social Distancing']
            output = 1
        return output
    def Ch_Rule2func(self, rule_input):
        output = 0
        if rule_input.mIPop >= 100 and (rule_input.ClosureVal in ['No Closures', 'Paso 5', 'Paso 4']):
            # print('Rule 2 Triggered')
            self.SD_Map.ClosureP.values[-1] = self.ClosureDict['Paso 1'] 
            output = 1
        return output
    def Ch_Rule3func(self, rule_input):
        output = 0
        if rule_input.mInfectR >= 100 and (rule_input.ClosureVal in ['No Closures', 'Paso 6', 'Paso 5', 'Paso 4', 'Paso 3', 'Paso 1' ]):
            # print('Rule 3 Triggered')
            self.SD_Map.ClosureP.values[-1] = self.ClosureDict['Lockdown']
            self.SD_Map.SocialDisP.values[-1] = self.SocialDisDict['Mandatory Social Distancing'] 
            output = 1
        return output
    def Ch_Rule4func(self,rule_input):
        output = 0
        if rule_input.mIPop <= 500 and (rule_input.ClosureVal in ['Paso 2', 'Paso 1', 'Lockdown' ]):
            # print('Rule 4 Triggered')
            self.SD_Map.ClosureP.values[-1] = self.ClosureDict['Paso 3']
            output = 1
        return output
    def Ch_Rule5func(self, rule_input):
        output = 0
        if rule_input.mIPop <= 500 and rule_input.SocialDisVal == 'Mandatory Social Distancing':
            # print('Rule 5 Triggered')
            self.SD_Map.SocialDisP.values[-1] = self.SocialDisDict['Voluntary Social Distancing']   
            output = 1
        return output
    
    """ MULTIPLE CONTEXT RULES """
    def M_Rule6func(self, rule_input):
        output = 0
        if rule_input.HPop > 2.5 * rule_input.Vents:
            # print('Rule 6 Triggered')
            self.SD_Map.NewOVents.values[-1] = 5
            output = 1
        return output
    def M_Rule7func(self, rule_input):
        output = 0
        if rule_input.HPop > 7 * rule_input.Vents:
            # print('Rule 7 Triggered')
            self.SD_Map.VWTP.values[-1] = 50000
            output = 1
        return output
    
    def make_rules(self):
        """PUT EACH DECISION RULE INTO A RULE CLASS AND STORE THEM AS A LIST
        
        Args:
            N/A
    
        Returns:
            N/A
        """
        self.Rules = []
        if self.location in ['Rio de Janeiro', 'Indonesia']:

            self.Rules.append(SDlib.Rule('Initial Closures', 1, 
                                 func = lambda rule_input: self.Br_Rule1func(rule_input)))
            self.Rules.append(SDlib.Rule('Additional Closures', 2, 
                                 func = lambda rule_input: self.Br_Rule2func(rule_input)))
            
            self.Rules.append(SDlib.Rule('Complete Lockdown', 3, 
                                 func = lambda rule_input: self.Br_Rule3func(rule_input)))
            
            self.Rules.append(SDlib.Rule('Re-open Some Businesses', 4, 
                                 func = lambda rule_input: self.Br_Rule4func(rule_input)))
            self.Rules.append(SDlib.Rule('Relax Mandatory Social Distancing', 5, 
                                 func = lambda rule_input: self.Br_Rule5func(rule_input)))
            
        elif self.location in ['Chile', 'Santiago']:
            self.Rules.append(SDlib.Rule('Initial Closures', 1, 
                                 func = lambda rule_input: self.Ch_Rule1func(rule_input)))
            self.Rules.append(SDlib.Rule('Additional Closures', 2, 
                                 func = lambda rule_input: self.Ch_Rule2func(rule_input)))
            
            self.Rules.append(SDlib.Rule('Complete Lockdown', 3, 
                                 func = lambda rule_input: self.Ch_Rule3func(rule_input)))
            
            self.Rules.append(SDlib.Rule('Re-open Some Businesses', 4, 
                                 func = lambda rule_input: self.Ch_Rule4func(rule_input)))
            self.Rules.append(SDlib.Rule('Relax Mandatory Social Distancing', 5, 
                                 func = lambda rule_input: self.Ch_Rule5func(rule_input)))
            
        if self.location in ['Chile', 'Rio de Janeiro', 'Indonesia']:
            self.Rules.append(SDlib.Rule('Order More Ventilators', 6, 
                                 func = lambda rule_input: self.M_Rule6func(rule_input)))
            self.Rules.append(SDlib.Rule('Pay More for Ventilators to Accelerate Delivery', 7, 
                                 func = lambda rule_input: self.M_Rule7func(rule_input)))
                       


# =============================================================================
#  Run UI            
# =============================================================================
if str.__eq__(__name__, '__main__'):

    #Avoids the "pyimage not found" error that is thrown if an error occured on the previous run attempt. 
    #This is certainly a janky method, but I don't know of another way, sadly
    root = tk.Tk()
    root.after(1000, root.destroy) 
    root.mainloop()

    #Load system dynamics causal map
    # SD_Map = SDlib.SD_System(tuning_flag=1)




    #Generate user interface
    UI = SD_UI(tuning = 0,
                location = 'Rio de Janeiro')

    #Run the user interface
    UI.mainloop()
    
    



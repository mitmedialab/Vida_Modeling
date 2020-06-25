#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 11:08:59 2020

@author: jackreid
"""
import tkinter as tk
import tkinter.font
import tkinter.ttk

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
style.use('ggplot')
# from PyQt5 import QtGui    # or PySide
import math
from tkinter import Widget
import numpy as np
import SDlib_v1_2 as SDlib
        

# =============================================================================
#  SD_UI Class               
# =============================================================================

class SD_UI(tk.Tk):
    
    def __init__(self, SD_Map, master=None, **kwargs):
        
        """INITIATE SD_UI CLASS
        
        Args:
            SD_Map: an instance of a SD_System class which represents the system dyanmics causal map
            master: optional argument identifying a parent tkinter window. If omited, the SD_UI class will be the parent window
        
        Returns:
            N/A
        """
        
        #Generate window and assign to appropriate master        
        tk.Tk.__init__(self, master)
        
        #Set geometry and other parameters of the window
        self.title('System Dynamics Visualization')
        default_font = tk.font.nametofont("TkDefaultFont")
        default_font.configure(size=20)
        pad=3
        self._geom='200x200+0+0'
        self.geometry("{0}x{1}+0+0".format(
            self.winfo_screenwidth()-pad, self.winfo_screenheight()-pad))
        self.bind('<Escape>',self.toggle_geom)            

        #Initialize the time series list and associated function(s)
        self.timeSeries = []
        self.timeSeries.append(0)
        self.timestep = lambda: self.timeSeries[-1] - self.timeSeries[-2]
    
        #Label the SD_Map input for easy reference
        self.SD_Map = SD_Map
        
        #Pull from the SD_Map various attributes for easy reference
        self.ClosureDict = self.SD_Map.ClosureDict() #dictionary relating string closure policy to numerical value
        self.ClosureDictInv = self.SD_Map.ClosureDictInv() #dictionary relating numerical closure policy to string value
        self.SocialDisDict = self.SD_Map.SocialDisDict() #dictionary relating string social distancing policy to numerical value
        self.SocialDisDictInv = self.SD_Map.SocialDisDictInv() #dictionary relating numerical social distancing policy to string value
        self.CatColorDict, self.colormap, self.norm = self.SD_Map.CatColor() #information relating categories to colors for visualization
        
        #Generate the four graphs and their associated dropdown menus
        self.graph_setting_list = [[],[]]
        self.graph_canvas_list = [[],[]]
        self.graph_optionlist_list = [[],[]]
        self.graph_frame_L = self.make_graph_frame('Measured Total Infected Population', 'Hospitalized Population', 0) #left pair of graphs
        self.graph_frame_R = self.make_graph_frame('Employment Rate', 'Daily Emissions Rate', 1) #right pair of graphs
        
        #Generate the policy action controls
        self.control_frame = self.make_control_frame()
        
        #Generate the decision rules and their associated display
        self.make_rules()
        self.info_frame = self.make_rule_display()
        
    
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
        graph_frame = tk.Frame(self, width=500, height=300, padx = 50, pady = 25)
        graph_frame.grid(column=col, row=0)

        
        #Generate the top graph label and dropdown menu
        index = 0
        graph_label = tk.Label(graph_frame, text='Graph 1: ', font=('Arial',24))
        graph_label.grid(column=0, row=0)
        graph_optionlist = self.make_graph_dropdown(graph_frame, firstgraph, index, col)
        graph_optionlist.grid(column=1, row=0)
        self.graph_optionlist_list[col].append(graph_optionlist)
        
        #Generate the top graph
        canvas = self.make_graph(graph_frame, firstgraph)
        self.graph_canvas_list[col].append(canvas)
        
        #Generate the bottom graph label and dropdown menu
        index = 1
        graph_label = tk.Label(graph_frame, text='Graph 2: ', font=('Arial',24))
        graph_label.grid(column=0, row=3)        
        graph_optionlist = self.make_graph_dropdown(graph_frame, secondgraph, index, col)
        graph_optionlist.grid(column=1, row=3)
        self.graph_optionlist_list[col].append(graph_optionlist)
        
        #Generate the bottom graph
        canvas = self.make_graph(graph_frame, secondgraph)
        self.graph_canvas_list[col].append(canvas)
        
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
        SD_dict = self.SD_Map.__dict__
        
        #Generate a list of the categories of all the SD objects
        categorylist = []
        for SDobject in SD_dict:
            categoryname = SD_dict[SDobject].category
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
            categoryname = SD_dict[SDobject].category
            obname = SD_dict[SDobject].name
            catdict[categoryname].append(obname)
                
        #Initalize the tkinter variable associated with the dropdown menu
        graph_setting_default = defaultsetting
        graph_setting_name = tk.StringVar()
        graph_setting_name.set(graph_setting_default)
        
        #Identify the initial background color of the dropdown menu
        normvalue = self.norm(self.CatColorDict[self.SD_Map.retrieve_ob(graph_setting_default).category])
        fill1 = self.colormap(normvalue)[0:3]
        fill = [int(x*255) for x in fill1]
        fill = self.rgb2hex(fill)
        
        #Initialize the dropdown menu
        graph_optionlist = tk.Menubutton(frame, textvariable=graph_setting_name, 
                                        indicatoron=False,
                                        background=fill,
                                        width=40)
        
        #Fill the dropdown menu with the category cascade menus and the specific objects in the appropriate categories
        topMenu = tk.Menu(graph_optionlist, tearoff=False)
        graph_optionlist.configure(menu=topMenu)
        for key in sorted(catdict.keys()):
            
            #Identify the color of each category in menu
            normvalue = self.norm(self.CatColorDict[key])
            fill1 = self.colormap(normvalue)[0:3]
            fill = [int(x*255) for x in fill1]
            fill = self.rgb2hex(fill)
            
            #Add a cascade menu for the category
            menu = tk.Menu(topMenu)
            topMenu.add_cascade(label=key, menu=menu, background=fill)

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

        return canvas
    
    def make_fig(self, graph_setting):
        """GENERATE FIGURE PLOTTING OBJECT VALUES OVER TIME
        
        Args:
            graph_setting: name of SD object to be plotted
    
        Returns:
            fig: matplotlib figure object
        """
        
        #Initialize Figure
        fig = Figure(figsize=(8, 3), dpi=100)
        
        #Retrieve SD Object based on name
        SDob = self.SD_Map.retrieve_ob(graph_setting)

        #Identify color to use for plotting based on SD object's category
        normvalue = self.norm(self.CatColorDict[SDob.category])
        fill1 = np.array([self.colormap(normvalue)[0:3]])

        #Generate scatterplot
        ax1 = fig.add_subplot(111)
        ax1.scatter(self.timeSeries, SDob.values, c=fill1)
        endtime = max(self.timeSeries[-1], 200)
        ax1.set_xlim(0, endtime)
        ax1.set_ylim(0, 1.2*max(self.SD_Map.retrieve_ob(graph_setting).values))
        ax1.set_ylabel(self.SD_Map.retrieve_ob(graph_setting).units)
        ax1.set_xlabel('Days')

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
        self.graph_canvas_list[col][index].get_tk_widget().destroy()
        
        #Identify the proper SD object to plot in replacement
        graph = self.graph_setting_list[col][index].get()
        
        #Generate the new graph and store it for future reference
        canvas = self.make_graph(framename, graph,
                        gridpos = index*2+1)
        self.graph_canvas_list[col][index] = canvas

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
        control_frame = tk.Frame(self, padx = 0)
        control_frame.grid(column=0, row=4, columnspan = 1)
        
        #Generate the time indicator
        time_label = tk.Label(control_frame, text='Day: ', font=('Arial',24))
        time_label.grid(column=0, row=0)
        self.timev = tk.StringVar()
        self.timev.set(str(self.timeSeries[-1]))
        self.time_value_label = tk.Label(control_frame, textvariable=self.timev, font=('Arial',24))
        self.time_value_label.grid(column=1, row=0, sticky='W')
        
        #Generate the Closure Policy control dropdown
        option1_label = tk.Label(control_frame, text='Closure Policy: ', font=('Arial',24))
        option1_label.grid(column=0, row=1)
        option1_list = ['No Closures',
                        'Large Events & Confined Spaces Closed',
                        'All Non Essential Businesses Closed',
                        'All In-Person Businesses Closed']
        self.option1_var = tk.StringVar()
        self.option1_var.set(option1_list[0])
        option1_menu = tk.OptionMenu(control_frame, self.option1_var, 
                          *option1_list, 
                           command=lambda _: self.update_ClosureP()
                          )
        option1_menu.config(width=40, anchor='w')
        option1_menu.grid(column=1, row=1, columnspan=2)
        
        #Generate the Social Distancing Policy control dropdown
        option2_label = tk.Label(control_frame, text='Social Distancing Policy: ', font=('Arial',24))
        option2_label.grid(column=0, row=2)
        option2_list = ['No Distancing',
                        'Voluntary Social Distancing',
                        'Mandatory Social Distancing'
                        ]
        self.option2_var = tk.StringVar()
        self.option2_var.set(option2_list[0])
        option2_menu = tk.OptionMenu(control_frame, self.option2_var, 
                          *option2_list, 
                           command=lambda _: self.update_SocialDisP()
                          )
        option2_menu.config(width=40, anchor='w')
        option2_menu.grid(column=1, row=2, columnspan=2)
        
        #Generate the ventilator ordering entry box
        option3_label = tk.Label(control_frame, text='Order New Ventilators: ', font=('Arial',24))
        option3_label.grid(column=0, row=3)
        self.option3_var = tk.IntVar()
        self.option3_var.set(0)
        FontOfEntryList=tkinter.font.Font(family="Arial",size=24)
        self.option3_menu = tk.Entry(control_frame, font=FontOfEntryList)
        self.option3_menu.insert(0,self.option3_var.get())
        self.option3_menu.configure(width=5)
        self.option3_menu.grid(column=1, row=3, sticky='W')

        #Generate the Next Week simulation button
        run_button = tk.Button(control_frame, text='Next Week', 
                               command = lambda: self.increment_time(),
                               font=('Arial',24))
        run_button.grid(column=0, row=4, columnspan=2)
        
        #Generate the Run Autonomously button
        automatic_button = tk.Button(control_frame, text='Run Autonomously', 
                               command = lambda: self.automatic_window(),
                               font=('Arial',24))
        automatic_button.grid(column=0, row=5, columnspan=2)
        
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
            day_text = 'Day ' + str(self.timeSeries[-1]) 
            rule_text = '; Rules: ' + str(triggered_rules)[1:-1]
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
            
            #For each graph, delete it and repalce it with an update graph
            for canvas in canvaslist:
                if index < 2:
                    col = 0
                    inputindex = index
                else:
                    col = 1
                    inputindex = index - 2
                framename = canvas.get_tk_widget().master
                canvas.get_tk_widget().destroy()
                graph = self.graph_setting_list[col][inputindex].get()
                canvas = self.make_graph(framename, graph,
                            gridpos = inputindex*2+1)
                self.graph_canvas_list[col][inputindex]=canvas
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
        windowtext = 'How many days do you want the simulation to run for?' 
        automatic_window.title(windowtext)
        lbl_text = tk.Label(automatic_window, text=windowtext,font=('Arial',24))
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
        auto_run_button = tk.Button(automatic_window, text='Run Simulation', 
                               command = lambda: self.auto_run(automatic_window, int(auto_menu.get())),
                               font=('Arial',24))
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
                mIPop = self.SD_Map.mTotIPop.value()
                ClosureVal = self.ClosureDictInv[self.SD_Map.ClosureP.value()]
                SocialDisVal = self.SocialDisDictInv[self.SD_Map.SocialDisP.value()]
                mInfectR = self.SD_Map.mInfectR.value()
                HPop = self.SD_Map.HPop.value()
                Vents = self.SD_Map.Vents.value()
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
        info_frame = tk.Frame(self)
        info_frame.grid(column=1, row=4)
        
        #Make Label and Tabs for the Rule Info Box
        list_tabparent = tk.ttk.Notebook(info_frame)
        list_tabparent.grid(column=0, row=0)
        self.list_info_boxes=dict()
        self.list_info_boxes['Rules'] = tk.Listbox(list_tabparent, width=60)
        self.list_info_boxes['Log'] = tk.Listbox(list_tabparent, width=60)
        list_tabparent.add(self.list_info_boxes['Rules'], text = 'Rules')
        list_tabparent.add( self.list_info_boxes['Log'], text = 'Log')
        
        #Populate list of rules
        for rule in self.Rules:
            self.list_info_boxes['Rules'].insert(tk.END, 'Rule ' + str(rule.number) + ': ' + str(rule.name))
            
        #Add scrollbar to the rule log display
        self.scrollbar = tk.Scrollbar(info_frame, orient='vertical',
                                          command=self.list_info_boxes['Log'].yview)
        self.scrollbar.grid(column=1, row=0, sticky='ns')
        self.list_info_boxes['Log'].config(yscrollcommand=self.scrollbar.set)
        
        return info_frame
 
 
# =============================================================================
#  Define the Decision Rules             
# =============================================================================
    """Each decision rules follows a constant, as follow
        
        Args:
            rule_intput: class holding all of the relevant input values for the decision conditions

        Conditional: Condition identifying when the rule is triggered
        
        Policy Effect: Policy changes that occur when the conditional is met
    
        Returns:
            output: a flag indicating if the conditional has been met (0=no, 1=yes)
        """
        
    def Rule1func(self, rule_input):
        output = 0
        if rule_input.mIPop >= 20 and rule_input.ClosureVal == 'No Closures' and rule_input.SocialDisVal == 'No Distancing':
            # print('Rule 1 Triggered')
            self.SD_Map.ClosureP.values[-1] = self.ClosureDict['Large Events & Confined Spaces Closed']
            self.SD_Map.SocialDisP.values[-1] = self.SocialDisDict['Voluntary Social Distancing']
            output = 1
        return output
    def Rule2func(self, rule_input):
        output = 0
        if rule_input.mIPop >= 100 and (rule_input.ClosureVal in ['No Closures', 'Large Events & Confined Spaces Closed']):
            # print('Rule 2 Triggered')
            self.SD_Map.ClosureP.values[-1] = self.ClosureDict['All Non Essential Businesses Closed'] 
            output = 1
        return output
    def Rule3func(self, rule_input):
        output = 0
        if rule_input.mInfectR >= 100 and (rule_input.ClosureVal in ['No Closures', 'Large Events & Confined Spaces Closed', 'All Non Essential Businesses Closed' ]):
            # print('Rule 3 Triggered')
            self.SD_Map.ClosureP.values[-1] = self.ClosureDict['All In-Person Businesses Closed']
            self.SD_Map.SocialDisP.values[-1] = self.SocialDisDict['Mandatory Social Distancing'] 
            output = 1
        return output
    def Rule4func(self,rule_input):
        output = 0
        if rule_input.mIPop <= 500 and rule_input.ClosureVal == 'All In-Person Businesses Closed':
            # print('Rule 4 Triggered')
            self.SD_Map.ClosureP.values[-1] = self.ClosureDict['Large Events & Confined Spaces Closed']
            output = 1
        return output
    def Rule5func(self, rule_input):
        output = 0
        if rule_input.mIPop <= 500 and rule_input.SocialDisVal == 'Mandatory Social Distancing':
            # print('Rule 5 Triggered')
            self.SD_Map.SocialDisP.values[-1] = self.SocialDisDict['Voluntary Social Distancing']   
            output = 1
        return output
    def Rule6func(self, rule_input):
        output = 0
        if rule_input.HPop > 2.5 * rule_input.Vents:
            # print('Rule 6 Triggered')
            self.SD_Map.NewOVents.values[-1] = 5
            output = 1
        return output
    def Rule7func(self, rule_input):
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
        self.Rules.append(SDlib.Rule('Initial Closures', 1, 
                             func = lambda rule_input: self.Rule1func(rule_input)))
        self.Rules.append(SDlib.Rule('Additional Closures', 2, 
                             func = lambda rule_input: self.Rule2func(rule_input)))
        
        self.Rules.append(SDlib.Rule('Complete Lockdown', 3, 
                             func = lambda rule_input: self.Rule3func(rule_input)))
        
        self.Rules.append(SDlib.Rule('Re-open Some Businesses', 4, 
                             func = lambda rule_input: self.Rule4func(rule_input)))
        self.Rules.append(SDlib.Rule('Relax Mandatory Social Distancing', 5, 
                             func = lambda rule_input: self.Rule5func(rule_input)))
        self.Rules.append(SDlib.Rule('Order More Ventilators', 6, 
                             func = lambda rule_input: self.Rule6func(rule_input)))
        self.Rules.append(SDlib.Rule('Pay More for Ventilators to Accelerate Delivery', 7, 
                             func = lambda rule_input: self.Rule7func(rule_input)))
                   


# =============================================================================
#  Run UI            
# =============================================================================
if str.__eq__(__name__, '__main__'):
    
    #Load system dynamics causal map
    SD_Map = SDlib.SD_System()

    #Generate user interface
    UI = SD_UI(SD_Map)

    #Run the user interface
    UI.mainloop()
    
    



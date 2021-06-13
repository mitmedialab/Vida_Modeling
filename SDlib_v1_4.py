#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 11:08:59 2020

@author: jackreid
"""


import math
import numpy as np
from matplotlib import cm
import matplotlib.colors as colors

# =============================================================================
#  SD_object Class                
# =============================================================================

class SD_object:
    
    def __init__(self, name, **kwargs):
        """INITIATE SD_object CLASS
        
        Args:
            name: string, name of the SD object
            init_value: initial value of the object
            units: string, units of the object
            func: function defining how to update the object at each timestep
            obtype: type of object (stock, flow, variable)
            maxval: optional, maximum allowable value of object
            minval: optional, minimum allowavle value of object
            category: category of object (e.g. Policies & Actions, Health Populations, etc.)
        
        Returns:
            N/A
        """
        
        #Load all inputs
        self.name = name
        self.values = []
        if 'init_value' in kwargs:
            init_value = kwargs.pop('init_value')
            if type(init_value) is list:
                self.values.extend(init_value)
            elif callable(init_value):
                newvals = init_value()
                self.values.extend(newvals)
                # print(self.name)
                # print(self.values)
            else:
                self.values.append(init_value)
                
        if 'units' in kwargs:
            self.units = kwargs.pop('units')
        if 'func' in kwargs:
            self.func = kwargs.pop('func')
        if 'obtype' in kwargs:
            self.type = kwargs.pop('obtype')
        if 'maxval' in kwargs:
            self.maxval = kwargs.pop('maxval')
        else:
            self.maxval = []
        if 'minval' in kwargs:
            self.minval = kwargs.pop('minval')
        else:
            self.minval = []
        if 'category' in kwargs:
            self.category = kwargs.pop('category')
        if 'history' in kwargs:
            self.history = kwargs.pop('history')
        else:
            self.history = []
        if 'datatype' in kwargs:
            self.datatype = kwargs.pop('datatype')
        else:
            self.datatype = 'numeric'
        if 'visualization' in kwargs:
            visualization = kwargs.pop('visualization')
            self.vismin = visualization[0]
            self.vismax = visualization[1]
        else:
            self.vismin = []
            self.vismax = []
                
            
      
    def value(self, **kwargs):
        """RETURN CURRENT OR SPECIFIED VALUE OF SD OBJECT
        
        Args:
            ind: optional, index of value to be obtained, default is to obtain the final value
        
        Returns:
            requested value
        """
        
        if 'ind' in kwargs:
            ind = kwargs.pop('ind')
        else:
            ind = -1
            
        outval = self.values[ind]
        if outval == []:
            while outval == []:
                ind -= 1
                outval = self.values[ind]
                if ind <= -5000:
                    break
            
        return outval
    
    def update(self, tstep, tind):
        """UPDATE THE SD OBJECT VALUE
        
        Args:
            tstep: the length of time to simulate into the future
            tind: the index of values with which to refer to other SD objects
        
        Returns:
            N/A
        """
        if self.maxval !=[] and self.minval !=[]:
            self.values.append(min(max(self.func(tstep, tind), self.minval()), self.maxval()))
        else:
            self.values.append(self.func(tstep, tind))
        

# =============================================================================
#  Rule Class                
# =============================================================================

        
class Rule:
      def __init__(self, name, number, **kwargs): 
          """INITIATE RULE CLASS
        
        Args:
            name: string, name of rule
            number: integer, index of rule
            func: function of rule
        
        Returns:
            N/A
        """
          self.name = name
          self.number = number
          # self.SD_Map = SD_Map
          if 'func' in kwargs:
            self.func = kwargs.pop('func')
         
        
# =============================================================================
#  SD_System Class                
# =============================================================================

class SD_System: 
    def __init__(self, **kwargs):
        
        """INITIATE SD_SYSTEM CLASS
        This class specifies a specific system dynamics causal map. It is constituted of numerous SD_object's of various categories
        
        Args:
            tuning_flag (optional): Flag indicating whether model is in tuning mode (1) or not (0). Default is 0.
            location (optional): String indicating application location of system. Default is 'Rio de Janeiro'
            data_filepath (optional): String indicating the filepath of historical data to pull from. Default is ./Data/Brazil/Brazil_Data.csv'
        
        Returns:
            N/A
        """
        
        #Load Inputs
        if 'tuning_flag' in kwargs:
            tuning_flag = kwargs.pop('tuning_flag')
        else:
            tuning_flag = 0
        if 'location' in kwargs:
            location = kwargs.pop('location')
            print(location)
        else:
            location = 'Rio de Janeiro'
        if 'data_filepath' in kwargs:
            filename = kwargs.pop('data_filepath')
        else:
            filename = './Data/Brazil/Brazil_Data.csv'


    # =============================================================================
    # %% 1 - Rio de Janeiro  
    # =============================================================================

        if location in ['Rio de Janeiro']:
          
            """ 1 - POLICIES & ACTIONS """
            self.ClosureP = SD_object('Closure Policy',
                                        units = 'unitless',
                                        init_value = lambda: self.historical_data('Closure Policy', location, filename),
                                        obtype = 'variable',
                                        func = lambda tstep, tind: self.ClosureP.value(),
                                        datatype = 'stringdict',
                                        category = 'Policies & Actions')
              
          
            self.SocialDisP = SD_object('Social Distancing Policy',
                                        units = 'unitless',
                                        #init_value = lambda: self.historical_data('Social Distancing Policy', location, filename),
                                        init_value = 1,
                                        obtype = 'variable',
                                        func = lambda tstep, tind: self.SocialDisP.value(),
                                        datatype = 'stringdict',
                                        category = 'Policies & Actions')
          
          
            """ 2 - HEALTH PARAMETERS """
            self.BaseContactR = SD_object('Base Contact Rate',
                            units = 'people/(day*person)',
                            init_value = 5,
                            obtype = 'variable',
                            func = lambda tstep, tind: self.BaseContactR.value(),
                            category = 'Health Parameters'
                            )
            self.ContactR = SD_object('Contact Rate',
                                    units = 'people/(day*person)',
                                    init_value = self.ClosureP.value() * self.SocialDisP.value() * self.BaseContactR.value(),
                                    obtype = 'variable',
                                    func = lambda tstep, tind: self.ClosureP.value() * self.SocialDisP.value() * self.BaseContactR.value(),
                                    category = 'Health Parameters'
                                    )
            
            self.Infectivity = SD_object('Infectivity',
                                units = 'likelihood/contact',
                                init_value = 0.05,
                                obtype = 'variable',
                                func = lambda tstep, tind: self.Infectivity.value(ind=tind),
                                maxval = lambda: 1,
                                minval = lambda: 0,
                                category = 'Health Parameters')
            
            self.AvDur = SD_object('Average Illness Duration',
                                  units = 'Days',
                                  init_value = 14,
                                  obtype = 'variable',
                                  func = lambda tstep, tind: self.AvDur.value(ind=tind),
                                  maxval = lambda: 300,
                                  minval = lambda: 0,
                                  category = 'Health Parameters')  
            
            self.HosL = SD_object('Hospitalization Likelihood',
                          units = 'probability',
                          init_value = 0.05,
                          obtype = 'variable',
                          func = lambda tstep, tind: self.HosL.value(ind=tind),
                          maxval = lambda: 1,
                          minval = lambda: 0,
                          category = 'Health Parameters')
              
            self.UHML = SD_object('Unhospitalized Mortality Likelihood',
                          units = 'probability',
                          init_value = 0.3,
                          obtype = 'variable',
                          func = lambda tstep, tind: self.UHML.value(ind=tind),
                          maxval = lambda: 1,
                          minval = lambda: 0,
                          category = 'Health Parameters')
              
            self.UHRL = SD_object('Unhospitalized Recovery Likelihood',
                          units = 'probability',
                          init_value = 1-self.UHML.value(),
                          obtype = 'variable',
                          func = lambda tstep, tind: 1 - self.UHML.value(ind=tind),
                          maxval = lambda: 1,
                          minval = lambda: 0,
                          category = 'Health Parameters')
                
            self.HRL = SD_object('Hospitalized Recovery Likelihood',
                          units = 'probability',
                          init_value = 0.9, #lambda: self.HRecovP_func(0, -1),
                          obtype = 'variable',
                          func = lambda tstep, tind: self.HRecovP_func(tstep, tind),
                          maxval = lambda: 1,
                          minval = lambda: 0,
                          category = 'Health Parameters')
              
            self.bHRL = SD_object('Base Hospitalized Recovery Likelihood',
                          units = 'probability',
                          init_value = 0.9,
                          obtype = 'variable',
                          func = lambda tstep, tind: self.bHRL.value(ind=tind),
                          maxval = lambda: 1,
                          minval = lambda: 0,
                          category = 'Health Parameters')
              
            self.HML = SD_object('Hospitalized Mortality Likelihood',
                          units = 'probability',
                          init_value = 1-self.HRL.value(),
                          obtype = 'variable',
                          func = lambda tstep, tind: 1 - self.HRL.value(ind=tind),
                          maxval = lambda: 1,
                          minval = lambda: 0,
                          category = 'Health Parameters')
          
            self.RecL = SD_object('Recovery Likelihood',
                          units = 'probability',
                          init_value = (1-self.HosL.value())*self.UHRL.value() + 
                                        self.HosL.value() * self.HRL.value(),
                          obtype = 'variable',
                          func = lambda tstep, tind: (1-self.HosL.value(ind=tind))*self.UHRL.value(ind=tind) + 
                                        self.HosL.value(ind=tind) * self.HRL.value(ind=tind),
                          maxval = lambda: 1,
                          minval = lambda: 0,
                          category = 'Health Parameters')
              
            self.MorL = SD_object('Mortality Likelihood',
                          units = 'probability',
                          init_value = (1-self.HosL.value())*self.UHML.value() + 
                                        self.HosL.value() * self.HML.value(),
                          obtype = 'variable',
                          func = lambda tstep, tind: (1-self.HosL.value(ind=tind))*self.UHML.value(ind=tind) + 
                                        self.HosL.value(ind=tind) * self.HML.value(ind=tind),
                          maxval = lambda: 1,
                          minval = lambda: 0,
                          category = 'Health Parameters')
              
            self.AvHDur = SD_object('Average Hospitalization Duration',
                          units = 'Days',
                          init_value = 7,
                          obtype = 'variable',
                          func = lambda tstep, tind: self.AvHDur.value(ind=tind),
                          maxval = lambda: 300,
                          minval = lambda: 0,
                          category = 'Health Parameters')
            
          
            """ 3 - HEALTH POPULATIONS """
            self.SPop = SD_object('Susceptible Population',
                                  units = 'people',
                                  init_value = lambda: self.historical_data('Susceptible Population', location, filename),
                                  obtype = 'stock',
                                  func = lambda tstep, tind: self.SPop.value(ind=tind) - self.InfectR.value(ind=tind) * tstep,
                                  maxval = lambda: 1000000000,
                                  minval = lambda: 0,
                                  category = 'Health Populations')
            
            self.IPop = SD_object("'Estimated' Unhospitalized Infected Population",
                                units = 'people',
                                init_value = lambda: self.historical_data('True Unhospitalized Infected', location, filename),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.IPop.value(ind=tind) + (self.InfectR.value(ind=tind) - self.UHMR.value(ind=tind) - 
                                                                          self.HosR.value(ind=tind) - self.UHRR.value(ind=tind)) * tstep,
                                maxval = lambda: 100000000,
                                minval = lambda: 0,
                                category = 'Health Populations')
          
            self.Deaths = SD_object('Deaths',
                                units = 'people',
                                init_value = lambda: self.historical_data('Accumulative Deaths', location, filename),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.Deaths.value(ind=tind) + (self.UHMR.value(ind=tind) + self.HMR.value(ind=tind)) * tstep,
                                maxval = lambda: 100000000,
                                minval = lambda: 0,
                                category = 'Health Populations')
              
            self.HPop = SD_object('Hospitalized Population',
                                units = 'people',
                                init_value = lambda: self.historical_data('Hospitalized Population', location, filename),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.HPop.value(ind=tind) + (self.HosR.value(ind=tind) - self.HMR.value(ind=tind) - self.HRR.value(ind=tind)) * tstep,
                                maxval = lambda: 1000000,
                                minval = lambda: 0,
                                category = 'Health Populations')
              
            self.RPop = SD_object('Known Recovered Population',
                                units = 'people',
                                init_value = lambda: self.historical_data('Recovered Population', location, filename),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.RPop.value(ind=tind) + (self.UHRR.value(ind=tind) + self.HRR.value(ind=tind)) * tstep,
                                maxval = lambda: 100000000,
                                minval = lambda: 0,
                                category = 'Health Populations')
              
            self.mIPop = SD_object("Measured Unhospitalized Infected Population",
                                units = 'people',
                                init_value = lambda: self.historical_data('Measured Unhospitalized Infected', location, filename),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.true_to_measured(self.IPop, 14, 0.1),
                                maxval = lambda: 100000000,
                                minval = lambda: 0,
                                category = 'Health Populations')
              
            self.mTotIPop = SD_object('Measured Total Infected Population',
                                units = 'people',
                                init_value = self.historical_data('Measured Current Infected', location, filename),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.mIPop.value(ind=tind) + self.HPop.value(ind=tind),
                                maxval = lambda: 100000000,
                                minval = lambda: 0,
                                category = 'Health Populations')
              
            self.TotIPop = SD_object("'Estimated' Total Infected Population",
                                units = 'people',
                                init_value = self.IPop.value() + self.HPop.value(),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.IPop.value(ind=tind) + self.HPop.value(ind=tind),
                                maxval = lambda: 100000000,
                                minval = lambda: 0,
                                category = 'Health Populations')
            
            
          
            """ 4 - HEALTH FLOWS """
            self.InfectR = SD_object("'Estimated' Infection Rate",
                                      units = 'people/day',
                                      init_value = lambda: self.historical_data('True Infection Rate', location, filename),
                                      obtype = 'flow',
                                      func = lambda tstep, tind: (self.combos(self.SPop.value(ind=tind) + self.IPop.value(ind=tind)) - self.combos(self.SPop.value(ind=tind)) - self.combos(self.IPop.value(ind=tind))) / 
                                                          self.combos(self.SPop.value(ind=tind) + self.IPop.value(ind=tind)) * self.ContactR.value(ind=tind) * (self.SPop.value(ind=tind) + self.IPop.value(ind=tind)) * self.Infectivity.value(ind=tind),
                                      maxval = lambda: self.SPop.value(),
                                      minval = lambda: 0,
                                      category = 'Health Flows'
                                      )
                  
            self.mInfectR = SD_object("Measured Infection Rate",
                                      units = 'people/day',
                                      init_value = lambda: self.historical_data('Measured Infection Rate',  location, filename),
                                      obtype = 'flow',
                                      func = lambda tstep, tind: self.true_to_measured(self.InfectR, 14, 0.1),
                                      maxval = lambda: self.SPop.value(),
                                      minval = lambda: 0,
                                      category = 'Health Flows'
                                      )
            
            self.UHRR = SD_object('Unhospitalized Recovery Rate',
                                  units = 'people/day',
                                  init_value = (1 - self.HosL.value()) * self.UHRL.value() * self.IPop.value() / self.AvDur.value(),
                                  obtype = 'flow',
                                  func = lambda tstep, tind: (1 - self.HosL.value(ind=tind)) * self.UHRL.value(ind=tind) * self.IPop.value(ind=tind) / self.AvDur.value(ind=tind),
                                  maxval = lambda: self.IPop.value(),
                                  minval = lambda: 0,
                                  category = 'Health Flows'
                                  )
              
            self.UHMR = SD_object('Unhospitalized Mortality Rate',
                                  units = 'people/day',
                                  init_value = (1 - self.HosL.value()) * self.UHML.value() * self.IPop.value() / self.AvDur.value(),
                                  obtype = 'flow',
                                  func = lambda tstep, tind: (1 - self.HosL.value(ind=tind)) * self.UHML.value(ind=tind) * self.IPop.value(ind=tind) / self.AvDur.value(ind=tind),
                                  maxval = lambda: self.IPop.value(),
                                  minval = lambda: 0,
                                  category = 'Health Flows'
                                  )
              
            self.HRR = SD_object('Hospital Recovery Rate',
                                  units = 'people/day',
                                  init_value = self.HRL.value() * self.HPop.value() / self.AvHDur.value(),
                                  obtype = 'flow',
                                  func = lambda tstep, tind: self.HRL.value(ind=tind) * self.HPop.value(ind=tind) / self.AvHDur.value(ind=tind),
                                  maxval = lambda: self.HPop.value(),
                                  minval = lambda: 0,
                                  category = 'Health Flows'
                                  )
              
            self.HMR = SD_object('Hospital Mortaility Rate',
                                  units = 'people/day',
                                  init_value = int(round(self.HML.value() * self.HPop.value() / self.AvHDur.value())),
                                  obtype = 'flow',
                                  func = lambda tstep, tind: self.HML.value(ind=tind) * self.HPop.value(ind=tind) / self.AvHDur.value(ind=tind),
                                  maxval = lambda: self.HPop.value(),
                                  minval = lambda: 0,
                                  category = 'Health Flows'
                                  )
              
            self.HosR = SD_object('Hospitalization Rate',
                                  units = 'people/day',
                                  init_value = lambda: self.historical_data('Hospitalization Rate', location, filename),
                                  obtype = 'flow',
                                  func = lambda tstep, tind: self.HosL.value(ind=tind) * self.IPop.value(ind=tind) / self.AvDur.value(ind=tind),
                                  maxval = lambda: self.IPop.value(),
                                  minval = lambda: 0,
                                  category = 'Health Flows'
                                  )
            
            """ 5 - EQUIPMENT SUPPLIES """
            self.HBeds = SD_object('Hospital Bed Capacity',
                        units = 'person',
                        init_value = 2000,
                        obtype = 'variable',
                        func = lambda tstep, tind: self.HBeds.value(ind=tind),
                        maxval = lambda: 1000000,
                        minval = lambda: 0,
                        category = 'Equipment Supplies')
              
            
            """ 7 - ENVIRONMENT """
            self.Temperature = SD_object('Average Temperature',
                        units = 'Celsius',
                        init_value = lambda: self.historical_data('Temperature', location, filename),
                        obtype = 'variable',
                        func = lambda tstep, tind: self.Temperature.value(ind=tind),
                        maxval = lambda: 150,
                        minval = lambda: -20,
                        category = 'Environment')
              
            self.SO2 = SD_object('SO2',
                        units = 'µg / m3',
                        init_value = lambda: self.historical_data('SO2', location, filename),
                        obtype = 'variable',
                        func = lambda tstep, tind: self.SO2.value(ind=tind),
                        maxval = lambda: 1000,
                        minval = lambda: 0,
                        category = 'Environment')
              
            self.NO2 = SD_object('NO2',
                        units = 'µg / m3',
                        init_value = lambda: self.historical_data('NO2', location, filename),
                        obtype = 'variable',
                        func = lambda tstep, tind: self.NO2.value(ind=tind),
                        maxval = lambda: 1000,
                        minval = lambda: 0,
                        category = 'Environment')
              
            self.HCNM = SD_object('HCNM',
                        units = 'ppm',
                        init_value = lambda: self.historical_data('HCNM', location, filename),
                        obtype = 'variable',
                        func = lambda tstep, tind: self.HCNM.value(ind=tind),
                        maxval = lambda: 1000,
                        minval = lambda: 0,
                        category = 'Environment')
              
            self.HCT = SD_object('HCT',
                        units = 'ppm',
                        init_value = lambda: self.historical_data('HCT', location, filename),
                        obtype = 'variable',
                        func = lambda tstep, tind: self.HCT.value(ind=tind),
                        maxval = lambda: 1000,
                        minval = lambda: 0,
                        category = 'Environment')
              
            self.CH4 = SD_object('CH4',
                        units = 'ppm',
                        init_value = lambda: self.historical_data('CH4', location, filename),
                        obtype = 'variable',
                        func = lambda tstep, tind: self.CH4.value(ind=tind),
                        maxval = lambda: 1000,
                        minval = lambda: 0,
                        category = 'Environment')
              
            self.CO = SD_object('CO',
                        units = 'ppm',
                        init_value = lambda: self.historical_data('CO', location, filename),
                        obtype = 'variable',
                        func = lambda tstep, tind: self.CO.value(ind=tind),
                        maxval = lambda: 1000,
                        minval = lambda: 0,
                        category = 'Environment')
              
            self.NO = SD_object('NO',
                        units = 'µg / m3',
                        init_value = lambda: self.historical_data('NO', location, filename),
                        obtype = 'variable',
                        func = lambda tstep, tind: self.NO.value(ind=tind),
                        maxval = lambda: 1000,
                        minval = lambda: 0,
                        category = 'Environment')
              
            self.NOx = SD_object('NOx',
                        units = 'µg / m3',
                        init_value = lambda: self.historical_data('NOx', location, filename),
                        obtype = 'variable',
                        func = lambda tstep, tind: self.NOx.value(ind=tind),
                        maxval = lambda: 1000,
                        minval = lambda: 0,
                        category = 'Environment')
              
            self.O3 = SD_object('O3',
                        units = 'µg / m3',
                        init_value = lambda: self.historical_data('O3', location, filename),
                        obtype = 'variable',
                        func = lambda tstep, tind: self.O3.value(ind=tind),
                        maxval = lambda: 1000,
                        minval = lambda: 0,
                        category = 'Environment')
              
            self.PM10 = SD_object('PM10',
                        units = 'µg / m3',
                        init_value = lambda: self.historical_data('PM10', location, filename),
                        obtype = 'variable',
                        func = lambda tstep, tind: self.PM10.value(ind=tind),
                        maxval = lambda: 1000,
                        minval = lambda: 0,
                        category = 'Environment')
              
            self.PM2_5 = SD_object('PM2.5',
                        units = 'µg / m3',
                        init_value = lambda: self.historical_data('PM2.5',  location, filename),
                        obtype = 'variable',
                        func = lambda tstep, tind: self.PM2_5.value(ind=tind),
                        maxval = lambda: 1000,
                        minval = lambda: 0,
                        category = 'Environment')

            """ 8 - ECONOMIC """
            
            self.RioEmployment = SD_object('Rio de Janeiro Unemployment Rate',
                                units = 'percent',
                                init_value = lambda: self.historical_data('Rio de Janeiro Unemployment Rate', location, filename),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.RioEmployment.value(ind=tind) + self.RioEmploymentR.value(ind=tind) * tstep,
                                maxval = lambda: 1,
                                minval = lambda: 0,
                                category = 'Economy')
              
      
              
            self.RioEmploymentR = SD_object('Rio de Janeiro Unemployment Rate of Change',
                                  units = 'percent',
                                  init_value = 0,
                                  obtype = 'flow',
                                  func = lambda tstep, tind: self.RioEmploymentR_update(tstep, tind),
                                  maxval = lambda: 0.05,
                                  minval = lambda: -0.05,
                                  category = 'Economy'
                                  )
              
            self.BraEmployment = SD_object('Brazil Unemployment Rate',
                                units = 'percent',
                                init_value = lambda: self.historical_data('Brazil Unemployment Rate', location, filename),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.BraEmployment.value(ind=tind) + self.BraEmploymentR.value(ind=tind) * tstep,
                                maxval = lambda: 1,
                                minval = lambda: 0,
                                category = 'Economy',
                                visualization = [0.08, 0.15])
              
      
              
            self.BraEmploymentR = SD_object('Brazil Unemployment Rate of Change',
                                  units = 'percent',
                                  init_value = 0,
                                  obtype = 'flow',
                                  func = lambda tstep, tind: self.BraEmploymentR_update(tstep, tind),
                                  maxval = lambda: 0.05,
                                  minval = lambda: -0.05,
                                  category = 'Economy'
                                  )
            
            """ 9 - MOBILITY """
            
            
            self.loc_retail_recreation_mob = SD_object('Retail and Recreation Mobility',
                                units = 'Mobility Index',
                                init_value = lambda: self.historical_data('retail_and_recreation_mob', location, filename), #this historical data only goes through late July, so post-late July is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.loc_retail_recreation_mob.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 100,   
                                minval = lambda: -100, 
                                category = 'Mobility')
            
            self.loc_grocery__pharmacy_mob = SD_object('Grocery and Pharmacy Mobility',
                                units = 'Mobility Index',
                                init_value = lambda: self.historical_data('grocery_and_pharmacy_mob', location, filename), #this historical data only goes through late July, so post-late July is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.loc_grocery__pharmacy_mob.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 100,   
                                minval = lambda: -100, 
                                category = 'Mobility')
            
            self.loc_parks_mob = SD_object('Parks Mobility',
                                units = 'Mobility Index',
                                init_value = lambda: self.historical_data('parks_percent_mob', location, filename), #this historical data only goes through late July, so post-late July is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.loc_parks_mob.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 100,   
                                minval = lambda: -100, 
                                category = 'Mobility')
            
            self.loc_transit_mob = SD_object('Transit Mobility',
                                units = 'Mobility Index',
                                init_value = lambda: self.historical_data('transit_stations_mob', location, filename), #this historical data only goes through late July, so post-late July is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.loc_transit_mob.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 100,   
                                minval = lambda: -100, 
                                category = 'Mobility')
            
            self.loc_workplaces_mob = SD_object('Workplace Mobility',
                                units = 'Mobility Index',
                                init_value = lambda: self.historical_data('workplaces_mob', location, filename), #this historical data only goes through late July, so post-late July is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.loc_workplaces_mob.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 100,   
                                minval = lambda: -100, 
                                category = 'Mobility')
            
            self.loc_residential_mob = SD_object('Residential Mobility',
                                units = 'Mobility Index',
                                init_value = lambda: self.historical_data('residential_mob', location, filename), #this historical data only goes through late July, so post-late July is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.loc_residential_mob.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 100,   
                                minval = lambda: -100, 
                                category = 'Mobility')
                   
        
    # =============================================================================
    # %% 2 - Chile 
    # =============================================================================
        
        if location in ['Chile']:
          
            """ 1 - POLICIES & ACTIONS """
            self.ClosureP = SD_object('Closure Policy',
                                        units = 'unitless',
                                        init_value = lambda: self.historical_data('Closure Policy', location, filename),
                                        obtype = 'variable',
                                        func = lambda tstep, tind: self.ClosureP.value(),
                                        datatype = 'stringdict',
                                        category = 'Policies & Actions')
              
          
          
            self.SocialDisP = SD_object('Curfew Policy',
                                    units = 'unitless',
                                    init_value = 1,
                                    obtype = 'variable',
                                    func = lambda tstep, tind: self.SocialDisP.value(),
                                    datatype = 'stringdict',
                                    category = 'Policies & Actions')
          
          
            """ 2 - HEALTH PARAMETERS """
            self.BaseContactR = SD_object('Base Contact Rate',
                            units = 'people/(day*person)',
                            init_value = 5,
                            obtype = 'variable',
                            func = lambda tstep, tind: self.BaseContactR.value(),
                            category = 'Health Parameters'
                            )
            self.ContactR = SD_object('Contact Rate',
                                    units = 'people/(day*person)',
                                    init_value = self.ClosureP.value() * self.SocialDisP.value() * self.BaseContactR.value(),
                                    obtype = 'variable',
                                    func = lambda tstep, tind: self.ClosureP.value() * self.SocialDisP.value() * self.BaseContactR.value(),
                                    category = 'Health Parameters'
                                    )
            
            self.Infectivity = SD_object('Infectivity',
                                units = 'likelihood/contact',
                                init_value = 0.05,
                                obtype = 'variable',
                                func = lambda tstep, tind: self.Infectivity.value(ind=tind),
                                maxval = lambda: 1,
                                minval = lambda: 0,
                                category = 'Health Parameters')
            
            self.AvDur = SD_object('Average Illness Duration',
                                  units = 'Days',
                                  init_value = 14,
                                  obtype = 'variable',
                                  func = lambda tstep, tind: self.AvDur.value(ind=tind),
                                  maxval = lambda: 300,
                                  minval = lambda: 0,
                                  category = 'Health Parameters')  
            
            self.HosL = SD_object('Hospitalization Likelihood',
                          units = 'probability',
                          init_value = 0.39,
                          obtype = 'variable',
                          func = lambda tstep, tind: self.HosL.value(ind=tind),
                          maxval = lambda: 1,
                          minval = lambda: 0,
                          category = 'Health Parameters')
              
            self.UHML = SD_object('Unhospitalized Mortality Likelihood',
                          units = 'probability',
                          init_value = 0.3,
                          obtype = 'variable',
                          func = lambda tstep, tind: self.UHML.value(ind=tind),
                          maxval = lambda: 1,
                          minval = lambda: 0,
                          category = 'Health Parameters')
              
            self.UHRL = SD_object('Unhospitalized Recovery Likelihood',
                          units = 'probability',
                          init_value = 1-self.UHML.value(),
                          obtype = 'variable',
                          func = lambda tstep, tind: 1 - self.UHML.value(ind=tind),
                          maxval = lambda: 1,
                          minval = lambda: 0,
                          category = 'Health Parameters')
                
            self.HRL = SD_object('Hospitalized Recovery Likelihood',
                          units = 'probability',
                          init_value = 0.9, #lambda: self.HRecovP_func(0, -1),
                          obtype = 'variable',
                          func = lambda tstep, tind: self.HRecovP_func(tstep, tind),
                          maxval = lambda: 1,
                          minval = lambda: 0,
                          category = 'Health Parameters')
              
            self.bHRL = SD_object('Base Hospitalized Recovery Likelihood',
                          units = 'probability',
                          init_value = 0.9,
                          obtype = 'variable',
                          func = lambda tstep, tind: self.bHRL.value(ind=tind),
                          maxval = lambda: 1,
                          minval = lambda: 0,
                          category = 'Health Parameters')
              
            self.HML = SD_object('Hospitalized Mortality Likelihood',
                          units = 'probability',
                          init_value = 1-self.HRL.value(),
                          obtype = 'variable',
                          func = lambda tstep, tind: 1 - self.HRL.value(ind=tind),
                          maxval = lambda: 1,
                          minval = lambda: 0,
                          category = 'Health Parameters')
          
            self.RecL = SD_object('Recovery Likelihood',
                          units = 'probability',
                          init_value = (1-self.HosL.value())*self.UHRL.value() + 
                                        self.HosL.value() * self.HRL.value(),
                          obtype = 'variable',
                          func = lambda tstep, tind: (1-self.HosL.value(ind=tind))*self.UHRL.value(ind=tind) + 
                                        self.HosL.value(ind=tind) * self.HRL.value(ind=tind),
                          maxval = lambda: 1,
                          minval = lambda: 0,
                          category = 'Health Parameters')
              
            self.MorL = SD_object('Mortality Likelihood',
                          units = 'probability',
                          init_value = (1-self.HosL.value())*self.UHML.value() + 
                                        self.HosL.value() * self.HML.value(),
                          obtype = 'variable',
                          func = lambda tstep, tind: (1-self.HosL.value(ind=tind))*self.UHML.value(ind=tind) + 
                                        self.HosL.value(ind=tind) * self.HML.value(ind=tind),
                          maxval = lambda: 1,
                          minval = lambda: 0,
                          category = 'Health Parameters')
              
            self.AvHDur = SD_object('Average Hospitalization Duration',
                          units = 'Days',
                          init_value = 7,
                          obtype = 'variable',
                          func = lambda tstep, tind: self.AvHDur.value(ind=tind),
                          maxval = lambda: 300,
                          minval = lambda: 0,
                          category = 'Health Parameters')
            
          
            """ 3 - HEALTH POPULATIONS """
            self.SPop = SD_object('Susceptible Population',
                                  units = 'people',
                                  init_value = lambda: self.historical_data('Susceptible Population', location, filename),
                                  obtype = 'stock',
                                  func = lambda tstep, tind: self.SPop.value(ind=tind) - self.InfectR.value(ind=tind) * tstep,
                                  maxval = lambda: 1000000000,
                                  minval = lambda: 0,
                                  category = 'Health Populations')
            
            self.IPop = SD_object("'Estimated' Unhospitalized Infected Population",
                                units = 'people',
                                init_value = lambda: self.historical_data('True Unhospitalized Infected', location, filename),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.IPop.value(ind=tind) + (self.InfectR.value(ind=tind) - self.UHMR.value(ind=tind) - 
                                                                          self.HosR.value(ind=tind) - self.UHRR.value(ind=tind)) * tstep,
                                maxval = lambda: 100000000,
                                minval = lambda: 0,
                                category = 'Health Populations')
          
            self.Deaths = SD_object('Deaths',
                                units = 'people',
                                init_value = lambda: self.historical_data('Accumulative Deaths', location, filename),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.Deaths.value(ind=tind) + (self.UHMR.value(ind=tind) + self.HMR.value(ind=tind)) * tstep,
                                maxval = lambda: 100000000,
                                minval = lambda: 0,
                                category = 'Health Populations')
              
            self.HPop = SD_object('Hospitalized Population',
                                units = 'people',
                                init_value = lambda: self.historical_data('Hospitalized Population', location, filename),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.HPop.value(ind=tind) + (self.HosR.value(ind=tind) - self.HMR.value(ind=tind) - self.HRR.value(ind=tind)) * tstep,
                                maxval = lambda: 1000000,
                                minval = lambda: 0,
                                category = 'Health Populations')
              
            self.RPop = SD_object('Known Recovered Population',
                                units = 'people',
                                init_value = lambda: self.historical_data('Recovered Population', location, filename),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.RPop.value(ind=tind) + (self.UHRR.value(ind=tind) + self.HRR.value(ind=tind)) * tstep,
                                maxval = lambda: 100000000,
                                minval = lambda: 0,
                                category = 'Health Populations')
              
            self.mIPop = SD_object("Measured Unhospitalized Infected Population",
                                units = 'people',
                                init_value = lambda: self.historical_data('Measured Unhospitalized Infected', location, filename),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.true_to_measured(self.IPop, 14, 0.25),
                                maxval = lambda: 100000000,
                                minval = lambda: 0,
                                category = 'Health Populations')
              
            self.mTotIPop = SD_object('Measured Total Infected Population',
                                units = 'people',
                                init_value = self.historical_data('Measured Current Infected', location, filename),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.mIPop.value(ind=tind) + self.HPop.value(ind=tind),
                                maxval = lambda: 100000000,
                                minval = lambda: 0,
                                category = 'Health Populations')
              
            self.TotIPop = SD_object("'Estimated' Total Infected Population",
                                units = 'people',
                                init_value = self.IPop.value() + self.HPop.value(),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.IPop.value(ind=tind) + self.HPop.value(ind=tind),
                                maxval = lambda: 100000000,
                                minval = lambda: 0,
                                category = 'Health Populations')
            
          
            """ 4 - HEALTH FLOWS """
            self.InfectR = SD_object("'Estimated' Infection Rate",
                                      units = 'people/day',
                                      init_value = lambda: self.historical_data('True Infection Rate', location, filename),
                                      obtype = 'flow',
                                      func = lambda tstep, tind: (self.combos(self.SPop.value(ind=tind) + self.IPop.value(ind=tind)) - self.combos(self.SPop.value(ind=tind)) - self.combos(self.IPop.value(ind=tind))) / 
                                                          self.combos(self.SPop.value(ind=tind) + self.IPop.value(ind=tind)) * self.ContactR.value(ind=tind) * (self.SPop.value(ind=tind) + self.IPop.value(ind=tind)) * self.Infectivity.value(ind=tind),
                                      maxval = lambda: self.SPop.value(),
                                      minval = lambda: 0,
                                      category = 'Health Flows'
                                      )
                  
            self.mInfectR = SD_object("Measured Infection Rate",
                                      units = 'people/day',
                                      init_value = lambda: self.historical_data('Measured Infection Rate',  location, filename),
                                      obtype = 'flow',
                                      func = lambda tstep, tind: self.true_to_measured(self.InfectR, 14, 0.25),
                                      maxval = lambda: self.SPop.value(),
                                      minval = lambda: 0,
                                      category = 'Health Flows'
                                      )
            
            self.UHRR = SD_object('Unhospitalized Recovery Rate',
                                  units = 'people/day',
                                  init_value = (1 - self.HosL.value()) * self.UHRL.value() * self.IPop.value() / self.AvDur.value(),
                                  obtype = 'flow',
                                  func = lambda tstep, tind: (1 - self.HosL.value(ind=tind)) * self.UHRL.value(ind=tind) * self.IPop.value(ind=tind) / self.AvDur.value(ind=tind),
                                  maxval = lambda: self.IPop.value(),
                                  minval = lambda: 0,
                                  category = 'Health Flows'
                                  )
              
            self.UHMR = SD_object('Unhospitalized Mortality Rate',
                                  units = 'people/day',
                                  init_value = (1 - self.HosL.value()) * self.UHML.value() * self.IPop.value() / self.AvDur.value(),
                                  obtype = 'flow',
                                  func = lambda tstep, tind: (1 - self.HosL.value(ind=tind)) * self.UHML.value(ind=tind) * self.IPop.value(ind=tind) / self.AvDur.value(ind=tind),
                                  maxval = lambda: self.IPop.value(),
                                  minval = lambda: 0,
                                  category = 'Health Flows'
                                  )
              
            self.HRR = SD_object('Hospital Recovery Rate',
                                  units = 'people/day',
                                  init_value = self.HRL.value() * self.HPop.value() / self.AvHDur.value(),
                                  obtype = 'flow',
                                  func = lambda tstep, tind: self.HRL.value(ind=tind) * self.HPop.value(ind=tind) / self.AvHDur.value(ind=tind),
                                  maxval = lambda: self.HPop.value(),
                                  minval = lambda: 0,
                                  category = 'Health Flows'
                                  )
              
            self.HMR = SD_object('Hospital Mortaility Rate',
                                  units = 'people/day',
                                  init_value = int(round(self.HML.value() * self.HPop.value() / self.AvHDur.value())),
                                  obtype = 'flow',
                                  func = lambda tstep, tind: self.HML.value(ind=tind) * self.HPop.value(ind=tind) / self.AvHDur.value(ind=tind),
                                  maxval = lambda: self.HPop.value(),
                                  minval = lambda: 0,
                                  category = 'Health Flows'
                                  )
              
            self.HosR = SD_object('Hospitalization Rate',
                                  units = 'people/day',
                                  init_value = lambda: self.historical_data('Hospitalization Rate', location, filename),
                                  obtype = 'flow',
                                  func = lambda tstep, tind: self.HosL.value(ind=tind) * self.IPop.value(ind=tind) / self.AvDur.value(ind=tind),
                                  maxval = lambda: self.IPop.value(),
                                  minval = lambda: 0,
                                  category = 'Health Flows'
                                  )
            
              
            """ 5 - EQUIPMENT SUPPLIES """
            self.HBeds = SD_object('Hospital Bed Capacity',
                        units = 'person',
                        init_value = 2000,
                        obtype = 'variable',
                        func = lambda tstep, tind: self.HBeds.value(ind=tind),
                        maxval = lambda: 1000000,
                        minval = lambda: 0,
                        category = 'Equipment Supplies')
              
            
            self.PCR = SD_object('Daily PCR Tests',
                    units = 'tests',
                    init_value = lambda: self.historical_data('PCR Tests', location, filename),
                    obtype = 'stock',
                    func = lambda tstep, tind: self.PCR.value(ind=tind),
                    maxval = lambda: 1000000,
                    minval = lambda: 0,
                    category = 'Equipment Supplies')
            
        
            
            
            """ 7 - ENVIRONMENT """
            
            """ 8 - ECONOMIC """
            self.AirPass = SD_object('Daily Flight Passengers',
                                units = 'people',
                                init_value = lambda: self.historical_data('Air Passengers', location, filename),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.AirPass.value(ind=tind),
                                maxval = lambda: 10000000,
                                minval = lambda: 0,
                                category = 'Economy')
        
    # =============================================================================
    # %% 3 - Santiago  
    # =============================================================================
        
        if location in ['Santiago']:
          
            """ 1 - POLICIES & ACTIONS """
            self.ClosureP = SD_object('Closure Policy',
                                        units = 'unitless',
                                        init_value = lambda: self.historical_data('Closure Policy', location, filename),
                                        obtype = 'variable',
                                        func = lambda tstep, tind: self.ClosureP.value(),
                                        datatype = 'stringdict',
                                        category = 'Policies & Actions')
              
          
          
            self.SocialDisP = SD_object('Curfew Policy',
                                    units = 'unitless',
                                    init_value = 1,
                                    obtype = 'variable',
                                    func = lambda tstep, tind: self.SocialDisP.value(),
                                    datatype = 'stringdict',
                                    category = 'Policies & Actions')
          
          
            """ 2 - HEALTH PARAMETERS """
            self.BaseContactR = SD_object('Base Contact Rate',
                            units = 'people/(day*person)',
                            init_value = 5,
                            obtype = 'variable',
                            func = lambda tstep, tind: self.BaseContactR.value(),
                            category = 'Health Parameters'
                            )
            self.ContactR = SD_object('Contact Rate',
                                    units = 'people/(day*person)',
                                    init_value = self.ClosureP.value() * self.SocialDisP.value() * self.BaseContactR.value(),
                                    obtype = 'variable',
                                    func = lambda tstep, tind: self.ClosureP.value() * self.SocialDisP.value() * self.BaseContactR.value(),
                                    category = 'Health Parameters'
                                    )
            
            self.Infectivity = SD_object('Infectivity',
                                units = 'likelihood/contact',
                                init_value = 0.05,
                                obtype = 'variable',
                                func = lambda tstep, tind: self.Infectivity.value(ind=tind),
                                maxval = lambda: 1,
                                minval = lambda: 0,
                                category = 'Health Parameters')
            
            self.AvDur = SD_object('Average Illness Duration',
                                  units = 'Days',
                                  init_value = 14,
                                  obtype = 'variable',
                                  func = lambda tstep, tind: self.AvDur.value(ind=tind),
                                  maxval = lambda: 300,
                                  minval = lambda: 0,
                                  category = 'Health Parameters')
            
            self.RecL = SD_object('Recovery Likelihood',
                        units = 'probability',
                        init_value = 0.79,
                        obtype = 'variable',
                        func = lambda tstep, tind: self.RecL.value(ind=tind),
                        maxval = lambda: 1,
                        minval = lambda: 0,
                        category = 'Health Parameters')
              
            self.MorL = SD_object('Mortality Likelihood',
                        units = 'probability',
                        init_value = 1-self.RecL.value(),
                        obtype = 'variable',
                        func = lambda tstep, tind: 1-self.RecL.value(ind=tind),
                        maxval = lambda: 1,
                        minval = lambda: 0,
                        category = 'Health Parameters')
          
          
            """ 3 - HEALTH POPULATIONS """
            self.SPop = SD_object('Susceptible Population',
                                  units = 'people',
                                  init_value = lambda: self.historical_data('Susceptible Population', location, filename),
                                  obtype = 'stock',
                                  func = lambda tstep, tind: self.SPop.value(ind=tind) - self.InfectR.value(ind=tind) * tstep,
                                  maxval = lambda: 1000000000,
                                  minval = lambda: 0,
                                  category = 'Health Populations')
            
            self.IPop = SD_object("'Estimated' Infected Population",
                                units = 'people',
                                init_value = lambda: self.historical_data('True Current Infected', location, filename),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.IPop.value(ind=tind) + (self.InfectR.value(ind=tind)  - 
                                                                          self.RR.value(ind=tind) - self.MR.value(ind=tind)) * tstep,
                                maxval = lambda: 100000000,
                                minval = lambda: 0,
                                category = 'Health Populations')
          
            self.Deaths = SD_object('Deaths',
                                units = 'people',
                                init_value = lambda: self.historical_data('Accumulative Deaths', location, filename),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.Deaths.value(ind=tind) + self.MR.value(ind=tind) * tstep,
                                maxval = lambda: 100000000,
                                minval = lambda: 0,
                                category = 'Health Populations')
              
            self.RPop = SD_object('Known Recovered Population',
                                units = 'people',
                                init_value = lambda: self.historical_data('Recovered Population', location, filename),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.RPop.value(ind=tind) + self.RR.value(ind=tind) * tstep,
                                maxval = lambda: 100000000,
                                minval = lambda: 0,
                                category = 'Health Populations')
              
            self.mIPop = SD_object("Measured Infected Population",
                                units = 'people',
                                init_value = lambda: self.historical_data('Measured Current Infected', location, filename),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.true_to_measured(self.IPop, 14, 0.25),
                                maxval = lambda: 100000000,
                                minval = lambda: 0,
                                category = 'Health Populations')
          
          
            """ 4 - HEALTH FLOWS """
            self.InfectR = SD_object("'Estimated' Infection Rate",
                                      units = 'people/day',
                                      init_value = lambda: self.historical_data('True Infection Rate', location, filename),
                                      obtype = 'flow',
                                      func = lambda tstep, tind: (self.combos(self.SPop.value(ind=tind) + self.IPop.value(ind=tind)) - self.combos(self.SPop.value(ind=tind)) - self.combos(self.IPop.value(ind=tind))) / 
                                                          self.combos(self.SPop.value(ind=tind) + self.IPop.value(ind=tind)) * self.ContactR.value(ind=tind) * (self.SPop.value(ind=tind) + self.IPop.value(ind=tind)) * self.Infectivity.value(ind=tind),
                                      maxval = lambda: self.SPop.value(),
                                      minval = lambda: 0,
                                      category = 'Health Flows'
                                      )
                  
            self.mInfectR = SD_object("Measured Infection Rate",
                                      units = 'people/day',
                                      init_value = lambda: self.historical_data('Measured Infection Rate',  location, filename),
                                      obtype = 'flow',
                                      func = lambda tstep, tind: self.true_to_measured(self.InfectR, 14, 0.25),
                                      maxval = lambda: self.SPop.value(),
                                      minval = lambda: 0,
                                      category = 'Health Flows'
                                      )
            
            self.RR = SD_object('Recovery Rate',
                                  units = 'people/day',
                                  init_value = self.RecL.value() * self.IPop.value() / self.AvDur.value(),
                                  # init_value = 1,
                                  obtype = 'flow',
                                  func = lambda tstep, tind: self.RecL.value(ind=tind) * self.IPop.value(ind=tind) / self.AvDur.value(ind=tind),
                                  maxval = lambda: self.IPop.value(),
                                  minval = lambda: 0,
                                  category = 'Health Flows'
                                  )
              
            self.MR = SD_object('Mortality Rate',
                                  units = 'people/day',
                                  init_value = self.MorL.value() * self.IPop.value() / self.AvDur.value(),
                                  obtype = 'flow',
                                  func = lambda tstep, tind: self.MorL.value(ind=tind) * self.IPop.value(ind=tind) / self.AvDur.value(ind=tind),
                                  maxval = lambda: self.IPop.value(),
                                  minval = lambda: 0,
                                  category = 'Health Flows'
                                  )
            
            
            """ 5 - EQUIPMENT SUPPLIES """
            
            """ 6 - EQUIPMENT PARAMETERS """
            
            """ 7 - ENVIRONMENT """
            
            self.Mob = SD_object('Mobility',
                                units = 'Mobility Index',
                                init_value = lambda: self.historical_data('Mobility', location, filename), #this historical data only goes through late July, so post-late July is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.Mob.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 100,   
                                minval = lambda: -100, 
                                category = 'Mobility')
            
            """ 8 - ECONOMIC """
        
        
        
        
    # =============================================================================
    # %% 4 - Indonesia 
    # =============================================================================
        
        if location in ['Indonesia']:
          
            """ 1 - POLICIES & ACTIONS """
            self.ClosureP = SD_object('Closure Policy',
                                        units = 'unitless',
                                        init_value = lambda: self.historical_data('Closure Policy', location, filename),
                                        obtype = 'variable',
                                        func = lambda tstep, tind: self.ClosureP.value(),
                                        datatype = 'stringdict',
                                        category = 'Policies & Actions')
              

          
          
            self.SocialDisP = SD_object('Social Distancing Policy',
                                    units = 'unitless',
                                    init_value = lambda: self.historical_data('Social Distancing Policy', location, filename),
                                    #init_value = 1,
                                    obtype = 'variable',
                                    func = lambda tstep, tind: self.SocialDisP.value(),
                                    datatype = 'stringdict',
                                    category = 'Policies & Actions')
  
            self.SocialDisP_s = SD_object('Social Distancing Policy Sulawesi',
                                    units = 'unitless',
                                    init_value = lambda: self.historical_data('Social Distancing Policy_sulawesi', location, filename),
                                    #init_value = 1,
                                    obtype = 'variable',
                                    func = lambda tstep, tind: self.SocialDisP_s.value(),
                                    datatype = 'stringdict',
                                    category = 'Policies & Actions')
  
            self.SocialDisP_j = SD_object('Social Distancing Policy Java',
                                    units = 'unitless',
                                    init_value = lambda: self.historical_data('Social Distancing Policy_java', location, filename),
                                    #init_value = 1,
                                    obtype = 'variable',
                                    func = lambda tstep, tind: self.SocialDisP_j.value(),
                                    datatype = 'stringdict',
                                    category = 'Policies & Actions')
  
            self.ClosureP_s = SD_object('Closure Policy Sulawesi',
                                units = 'unitless',
                                init_value = lambda: self.historical_data('Closure Policy_sulawesi', location, filename),
                                obtype = 'variable',
                                func = lambda tstep, tind: self.ClosureP_s.value(),
                                datatype = 'stringdict',
                                category = 'Policies & Actions')
  
            self.ClosureP_j = SD_object('Closure Policy Java',
                                units = 'unitless',
                                init_value = lambda: self.historical_data('Closure Policy_java', location, filename),
                                obtype = 'variable',
                                func = lambda tstep, tind: self.ClosureP_j.value(),
                                datatype = 'stringdict',
                                category = 'Policies & Actions')            
  
          
            """ 2 - HEALTH PARAMETERS """
            self.BaseContactR = SD_object('Base Contact Rate',
                            units = 'people/(day*person)',
                            init_value = 5,
                            obtype = 'variable',
                            func = lambda tstep, tind: self.BaseContactR.value(),
                            category = 'Health Parameters'
                            )
            self.ContactR = SD_object('Contact Rate',
                                    units = 'people/(day*person)',
                                    init_value = self.ClosureP.value() * self.SocialDisP.value() * self.BaseContactR.value(),
                                    obtype = 'variable',
                                    func = lambda tstep, tind: self.ClosureP.value() * self.SocialDisP.value() * self.BaseContactR.value(),
                                    category = 'Health Parameters'
                                    )
            
            self.Infectivity = SD_object('Infectivity',
                                units = 'likelihood/contact',
                                init_value = 0.05,
                                obtype = 'variable',
                                func = lambda tstep, tind: self.Infectivity.value(ind=tind),
                                maxval = lambda: 1,
                                minval = lambda: 0,
                                category = 'Health Parameters')
            
            self.AvDur = SD_object('Average Illness Duration',
                                  units = 'Days',
                                  init_value = 14,
                                  obtype = 'variable',
                                  func = lambda tstep, tind: self.AvDur.value(ind=tind),
                                  maxval = lambda: 300,
                                  minval = lambda: 0,
                                  category = 'Health Parameters') 
            
            #nationwide  
            self.RecL = SD_object('Recovery Likelihood',
                        units = 'probability',
                        init_value = 0.79,
                        obtype = 'variable',
                        func = lambda tstep, tind: self.RecL.value(ind=tind),
                        maxval = lambda: 1,
                        minval = lambda: 0,
                        category = 'Health Parameters')
              
            self.MorL = SD_object('Mortality Likelihood',
                        units = 'probability',
                        init_value = 1-self.RecL.value(),
                        obtype = 'variable',
                        func = lambda tstep, tind: 1-self.RecL.value(ind=tind),
                        maxval = lambda: 1,
                        minval = lambda: 0,
                        category = 'Health Parameters')
  
            #island specific
            self.ContactR_j = SD_object('Contact Rate Java',
                                units = 'people/(day*person)',
                                init_value = self.ClosureP_j.value() * self.SocialDisP_j.value() * self.BaseContactR.value(),
                                obtype = 'variable',
                                func = lambda tstep, tind: self.ClosureP_j.value() * self.SocialDisP_j.value() * self.BaseContactR.value(),
                                category = 'Health Parameters'
                                )    
  
            self.ContactR_s = SD_object('Contact Rate Sulawesi',
                                units = 'people/(day*person)',
                                init_value = self.ClosureP_s.value() * self.SocialDisP_s.value() * self.BaseContactR.value(),
                                obtype = 'variable',
                                func = lambda tstep, tind: self.ClosureP_s.value() * self.SocialDisP_s.value() * self.BaseContactR.value(),
                                category = 'Health Parameters'
                                )    
          
          
            """ 3 - HEALTH POPULATIONS """
            self.SPop = SD_object('Susceptible Population',
                                  units = 'people',
                                  init_value = lambda: self.historical_data('Susceptible Population', location, filename),
                                  obtype = 'stock',
                                  func = lambda tstep, tind: self.SPop.value(ind=tind) - self.InfectR.value(ind=tind) * tstep,
                                  maxval = lambda: 1000000000,
                                  minval = lambda: 0,
                                  category = 'Health Populations')
            
            #nationwide
            self.IPop = SD_object("'Estimated' Infected Population",
                                units = 'people',
                                init_value = lambda: self.historical_data('True Current Infected', location, filename),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.IPop.value(ind=tind) + (self.InfectR.value(ind=tind)  - 
                                                                          self.RR.value(ind=tind) - self.MR.value(ind=tind)) * tstep,
                                maxval = lambda: 100000000,
                                minval = lambda: 0,
                                category = 'Health Populations')
          
            self.Deaths = SD_object('Deaths',
                                units = 'people',
                                init_value = lambda: self.historical_data('Accumulative Deaths', location, filename),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.Deaths.value(ind=tind) + self.MR.value(ind=tind) * tstep,
                                maxval = lambda: 100000000,
                                minval = lambda: 0,
                                category = 'Health Populations')
              
            self.RPop = SD_object('Known Recovered Population',
                                units = 'people',
                                init_value = lambda: self.historical_data('Recovered Population', location, filename),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.RPop.value(ind=tind) + self.RR.value(ind=tind) * tstep,
                                maxval = lambda: 100000000,
                                minval = lambda: 0,
                                category = 'Health Populations')
              
            self.mIPop = SD_object("Measured Infected Population",
                                units = 'people',
                                init_value = lambda: self.historical_data('Measured Current Infected', location, filename),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.true_to_measured(self.IPop, 14, 0.25),
                                maxval = lambda: 100000000,
                                minval = lambda: 0,
                                category = 'Health Populations')   
            
            #island specific
            self.IPop_j = SD_object("'Estimated' Infected Population Java",
                                units = 'people',
                                init_value = lambda: self.historical_data('True Current Infected_java', location, filename),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.IPop_j.value(ind=tind) + (self.InfectR_j.value(ind=tind)  - 
                                                                          self.RR_j.value(ind=tind) - self.MR_j.value(ind=tind)) * tstep,
                                maxval = lambda: 100000000,
                                minval = lambda: 0,
                                category = 'Health Populations')
  
            self.IPop_s = SD_object("'Estimated' Infected Population Sulawesi",
                                units = 'people',
                                init_value = lambda: self.historical_data('True Current Infected_SN', location, filename),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.IPop_s.value(ind=tind) + (self.InfectR_s.value(ind=tind)  - 
                                                                          self.RR_s.value(ind=tind) - self.MR_s.value(ind=tind)) * tstep,
                                maxval = lambda: 100000000,
                                minval = lambda: 0,
                                category = 'Health Populations')
          
            self.Deaths_j = SD_object('Deaths Java',
                                units = 'people',
                                init_value = lambda: self.historical_data('Accumulative Deaths_java', location, filename),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.Deaths_j.value(ind=tind) + self.MR_j.value(ind=tind) * tstep,
                                maxval = lambda: 100000000,
                                minval = lambda: 0,
                                category = 'Health Populations')
  
            self.Deaths_s = SD_object('Deaths Sulawesi',
                                units = 'people',
                                init_value = lambda: self.historical_data('Accumulative Deaths_SN', location, filename),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.Deaths_s.value(ind=tind) + self.MR_s.value(ind=tind) * tstep,
                                maxval = lambda: 100000000,
                                minval = lambda: 0,
                                category = 'Health Populations')
              
            self.RPop_j = SD_object('Known Recovered Population Java',
                                units = 'people',
                                init_value = lambda: self.historical_data('Recovered Population_java', location, filename),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.RPop_j.value(ind=tind) + self.RR_j.value(ind=tind) * tstep,
                                maxval = lambda: 100000000,
                                minval = lambda: 0,
                                category = 'Health Populations')
  
            self.RPop_s = SD_object('Known Recovered Population Sulawesi',
                                units = 'people',
                                init_value = lambda: self.historical_data('Recovered Population_SN', location, filename),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.RPop_s.value(ind=tind) + self.RR_s.value(ind=tind) * tstep,
                                maxval = lambda: 100000000,
                                minval = lambda: 0,
                                category = 'Health Populations')
              
            self.mIPop_j = SD_object("Measured Infected Population Java",
                                units = 'people',
                                init_value = lambda: self.historical_data('Measured Current Infected_java', location, filename),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.true_to_measured(self.IPop_j, 14, 0.25),
                                maxval = lambda: 100000000,
                                minval = lambda: 0,
                                category = 'Health Populations')  
  
            self.mIPop_s = SD_object("Measured Infected Population Sulawesi",
                                units = 'people',
                                init_value = lambda: self.historical_data('Measured Current Infected_SN', location, filename),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.true_to_measured(self.IPop_s, 14, 0.25),
                                maxval = lambda: 100000000,
                                minval = lambda: 0,
                                category = 'Health Populations') 
  
            self.SPop_j = SD_object('Susceptible Population Java',
                              units = 'people',
                              init_value = lambda: self.historical_data('Susceptible Population_java', location, filename),
                              obtype = 'stock',
                              func = lambda tstep, tind: self.SPop_j.value(ind=tind) - self.InfectR_j.value(ind=tind) * tstep,
                              maxval = lambda: 1000000000,
                              minval = lambda: 0,
                              category = 'Health Populations')  
  
            self.SPop_s = SD_object('Susceptible Population Sulawesi',
                              units = 'people',
                              init_value = lambda: self.historical_data('Susceptible Population_SN', location, filename),
                              obtype = 'stock',
                              func = lambda tstep, tind: self.SPop_s.value(ind=tind) - self.InfectR_s.value(ind=tind) * tstep,
                              maxval = lambda: 1000000000,
                              minval = lambda: 0,
                              category = 'Health Populations')
            
          
            """ 4 - HEALTH FLOWS """
            self.InfectR = SD_object("'Estimated' Infection Rate",
                                      units = 'people/day',
                                      init_value = lambda: self.historical_data('True Infection Rate', location, filename),
                                      obtype = 'flow',
                                      func = lambda tstep, tind: (self.combos(self.SPop.value(ind=tind) + self.IPop.value(ind=tind)) - self.combos(self.SPop.value(ind=tind)) - self.combos(self.IPop.value(ind=tind))) / 
                                                          self.combos(self.SPop.value(ind=tind) + self.IPop.value(ind=tind)) * self.ContactR.value(ind=tind) * (self.SPop.value(ind=tind) + self.IPop.value(ind=tind)) * self.Infectivity.value(ind=tind),
                                      maxval = lambda: self.SPop.value(),
                                      minval = lambda: 0,
                                      category = 'Health Flows'
                                      )
                  
            self.mInfectR = SD_object("Measured Infection Rate",
                                      units = 'people/day',
                                      init_value = lambda: self.historical_data('Measured Infection Rate',  location, filename),
                                      obtype = 'flow',
                                      func = lambda tstep, tind: self.true_to_measured(self.InfectR, 14, 0.25),
                                      maxval = lambda: self.SPop.value(),
                                      minval = lambda: 0,
                                      category = 'Health Flows'
                                      )
            
            #nationwide
            self.RR = SD_object('Recovery Rate',
                                  units = 'people/day',
                                  init_value = self.RecL.value() * self.IPop.value() / self.AvDur.value(),
                                  # init_value = 1,
                                  obtype = 'flow',
                                  func = lambda tstep, tind: self.RecL.value(ind=tind) * self.IPop.value(ind=tind) / self.AvDur.value(ind=tind),
                                  maxval = lambda: self.IPop.value(),
                                  minval = lambda: 0,
                                  category = 'Health Flows'
                                  )
              
            self.MR = SD_object('Mortality Rate',
                                  units = 'people/day',
                                  init_value = self.MorL.value() * self.IPop.value() / self.AvDur.value(),
                                  obtype = 'flow',
                                  func = lambda tstep, tind: self.MorL.value(ind=tind) * self.IPop.value(ind=tind) / self.AvDur.value(ind=tind),
                                  maxval = lambda: self.IPop.value(),
                                  minval = lambda: 0,
                                  category = 'Health Flows'
                                  )
            
            #Island specific
            self.RR_j = SD_object('Recovery Rate Java',
                                  units = 'people/day',
                                  init_value = self.RecL.value() * self.IPop_j.value() / self.AvDur.value(),
                                  # init_value = 1,
                                  obtype = 'flow',
                                  func = lambda tstep, tind: self.RecL.value(ind=tind) * self.IPop_j.value(ind=tind) / self.AvDur.value(ind=tind),
                                  maxval = lambda: self.IPop.value(),
                                  minval = lambda: 0,
                                  category = 'Health Flows'
                                  )
  
            self.RR_s = SD_object('Recovery Rate Sulawesi',
                                  units = 'people/day',
                                  init_value = self.RecL.value() * self.IPop_s.value() / self.AvDur.value(),
                                  # init_value = 1,
                                  obtype = 'flow',
                                  func = lambda tstep, tind: self.RecL.value(ind=tind) * self.IPop_s.value(ind=tind) / self.AvDur.value(ind=tind),
                                  maxval = lambda: self.IPop.value(),
                                  minval = lambda: 0,
                                  category = 'Health Flows'
                                  )                                
              
            self.MR_j = SD_object('Mortality Rate Java',
                                  units = 'people/day',
                                  init_value = self.MorL.value() * self.IPop_j.value() / self.AvDur.value(),
                                  obtype = 'flow',
                                  func = lambda tstep, tind: self.MorL.value(ind=tind) * self.IPop_j.value(ind=tind) / self.AvDur.value(ind=tind),
                                  maxval = lambda: self.IPop.value(),
                                  minval = lambda: 0,
                                  category = 'Health Flows'
                                  )
  
            self.MR_s = SD_object('Mortality Rate Sulawesi',
                                  units = 'people/day',
                                  init_value = self.MorL.value() * self.IPop_s.value() / self.AvDur.value(),
                                  obtype = 'flow',
                                  func = lambda tstep, tind: self.MorL.value(ind=tind) * self.IPop_s.value(ind=tind) / self.AvDur.value(ind=tind),
                                  maxval = lambda: self.IPop.value(),
                                  minval = lambda: 0,
                                  category = 'Health Flows'
                                  )
  
            self.InfectR_j = SD_object("'Estimated' Infection Rate Java",
                                          units = 'people/day',
                                          init_value = lambda: self.historical_data('True Infection Rate_java', location, filename),
                                          obtype = 'flow',
                                          func = lambda tstep, tind: (self.combos(self.SPop_j.value(ind=tind) + self.IPop_j.value(ind=tind)) - self.combos(self.SPop_j.value(ind=tind)) - self.combos(self.IPop_j.value(ind=tind))) / 
                                                              self.combos(self.SPop_j.value(ind=tind) + self.IPop_j.value(ind=tind)) * self.ContactR_j.value(ind=tind) * (self.SPop_j.value(ind=tind) + self.IPop_j.value(ind=tind)) * self.Infectivity.value(ind=tind),
                                          maxval = lambda: self.SPop_j.value(),
                                          minval = lambda: 0,
                                          category = 'Health Flows'
                                          )
  
            self.InfectR_s = SD_object("'Estimated' Infection Rate Sulawesi",
                                          units = 'people/day',
                                          init_value = lambda: self.historical_data('True Infection Rate_SN', location, filename),
                                          obtype = 'flow',
                                          func = lambda tstep, tind: (self.combos(self.SPop_s.value(ind=tind) + self.IPop_s.value(ind=tind)) - self.combos(self.SPop_s.value(ind=tind)) - self.combos(self.IPop_s.value(ind=tind))) / 
                                                              self.combos(self.SPop_s.value(ind=tind) + self.IPop_s.value(ind=tind)) * self.ContactR_s.value(ind=tind) * (self.SPop_s.value(ind=tind) + self.IPop_s.value(ind=tind)) * self.Infectivity.value(ind=tind),
                                          maxval = lambda: self.SPop_s.value(),
                                          minval = lambda: 0,
                                          category = 'Health Flows'
                                          )                                        
                      
            self.mInfectR_j = SD_object("Measured Infection Rate Java",
                                  units = 'people/day',
                                  init_value = lambda: self.historical_data('Measured Infection Rate_java',  location, filename),
                                  obtype = 'flow',
                                  func = lambda tstep, tind: self.true_to_measured(self.InfectR_j, 14, 0.25),
                                  maxval = lambda: self.SPop_j.value(),
                                  minval = lambda: 0,
                                  category = 'Health Flows'
                                  )   
  
            self.mInfectR_s = SD_object("Measured Infection Rate Sulawesi",
                                  units = 'people/day',
                                  init_value = lambda: self.historical_data('Measured Infection Rate_SN',  location, filename),
                                  obtype = 'flow',
                                  func = lambda tstep, tind: self.true_to_measured(self.InfectR_s, 14, 0.25),
                                  maxval = lambda: self.SPop.value(),
                                  minval = lambda: 0,
                                  category = 'Health Flows'
                                  ) 
            
            
            """ 5 - EQUIPMENT SUPPLIES """
            
            """ 6 - EQUIPMENT PARAMETERS """
            
            """ 7 - ENVIRONMENT """
            
            
            """ 8 - ECONOMIC """
            self.GDP_Ind = SD_object('Gross Domestic Product',
                                units = 'Rp Million',
                                init_value = lambda: self.historical_data('GDP', location, filename),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.GDP_Ind.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 10000000,
                                minval = lambda: 0,
                                category = 'Economy - Nationwide')    
  
            self.Arrivals_Ind = SD_object('Visitor Arrivals',
                                units = 'people',
                                init_value = lambda: self.historical_data('Arrivals', location, filename), #this historical data only goes through June, so post-June is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.Arrivals_Ind.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 10000000,
                                minval = lambda: 0,
                                category = 'Economy - Nationwide')
  
  
            self.oil_Ind = SD_object('Oil and Gas Imports',
                                units = 'Millions USD',
                                init_value = lambda: self.historical_data('oil_imports', location, filename), #this historical data only goes through Q2, so post-Q2 is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.oil_Ind.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 10000000,
                                minval = lambda: 0,
                                category = 'Economy - Nationwide') 
  
            self.household_ex_Ind = SD_object('Household Expenditures',
                                units = 'Rp Million',
                                init_value = lambda: self.historical_data('household_ex', location, filename), #this historical data only goes through Q2, so post-Q2 is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.household_ex_Ind.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 100000000000,
                                minval = lambda: 0,
                                category = 'Economy - Nationwide')  
  
            self.consumtion_ex_Ind = SD_object('Consumption Expenditure LNPRT',
                                units = 'Rp Million',
                                init_value = lambda: self.historical_data('Consumtion_ex', location, filename), #this historical data only goes through Q2, so post-Q2 is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.consumtion_ex_Ind.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 100000000000,
                                minval = lambda: 0,
                                category = 'Economy - Nationwide')
  
            self.gov_ex_Ind = SD_object('Government Consumption Expenditure',
                                units = 'Rp Million',
                                init_value = lambda: self.historical_data('gov_ex', location, filename), #this historical data only goes through Q2, so post-Q2 is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.gov_ex_Ind.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 100000000000,
                                minval = lambda: 0,
                                category = 'Economy - Nationwide')         
  
            self.net_ex_Ind = SD_object('Net Exports',
                                units = 'Rp Million',
                                init_value = lambda: self.historical_data('net_ex', location, filename), #this historical data only goes through Q2, so post-Q2 is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.net_ex_Ind.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 100000000000,
                                minval = lambda: 0,
                                category = 'Economy - Nationwide')      
  
            self.GDP_manu_Ind = SD_object('Manufacturing GDP',
                                units = 'Rp Million',
                                init_value = lambda: self.historical_data('GDP_manu', location, filename), #this historical data only goes through Q2, so post-Q2 is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.GDP_manu_Ind.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 10000000,
                                minval = lambda: 0,
                                category = 'Economy - Nationwide')    
  
            self.GDP_cons_Ind = SD_object('Construction GDP',
                                units = 'Rp Million',
                                init_value = lambda: self.historical_data('GDP_cons', location, filename), #this historical data only goes through Q2, so post-Q2 is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.GDP_cons_Ind.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 10000000,
                                minval = lambda: 0,
                                category = 'Economy - Nationwide')   
  
            self.GDP_retail_Ind = SD_object('Retail and Vehicle Repair GDP',
                                units = 'Rp Million',
                                init_value = lambda: self.historical_data('GDP_retail', location, filename), #this historical data only goes through Q2, so post-Q2 is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.GDP_retail_Ind.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 10000000,
                                minval = lambda: 0,
                                category = 'Economy - Nationwide')     
  
            self.GDP_IT_Ind = SD_object('Information and Communication GDP',
                                units = 'Rp Million',
                                init_value = lambda: self.historical_data('GDP_IT', location, filename), #this historical data only goes through Q2, so post-Q2 is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.GDP_IT_Ind.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 10000000,
                                minval = lambda: 0,
                                category = 'Economy - Nationwide')       
  
            self.GDP_social_Ind = SD_object('Health and Social Work GDP',
                                units = 'Rp Million',
                                init_value = lambda: self.historical_data('GDP_social', location, filename), #this historical data only goes through Q2, so post-Q2 is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.GDP_social_Ind.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 10000000,
                                minval = lambda: 0,
                                category = 'Economy - Nationwide')           
  
            self.GDP_food_Ind = SD_object('Accommodation and Food Service GDP',
                                units = 'Rp Million',
                                init_value = lambda: self.historical_data('GDP_food', location, filename), #this historical data only goes through Q2, so post-Q2 is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.GDP_food_Ind.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 10000000,
                                minval = lambda: 0,
                                category = 'Economy - Nationwide')

            self.stock_index_Ind = SD_object('Closing Compsite Stock Index (IDX)',
                                units = 'Stock Index',
                                init_value = lambda: self.historical_data('stock_index', location, filename), 
                                obtype = 'stock',
                                func = lambda tstep, tind: self.stock_index_Ind.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 10000000,
                                minval = lambda: 0,
                                category = 'Economy - Nationwide')                                

            self.FTT_Ind_JK = SD_object('Farmer Terms of Trade - Jakarta',
                                units = 'Terms Rate',
                                init_value = lambda: self.historical_data('FTT_JK', location, filename), 
                                obtype = 'stock',
                                func = lambda tstep, tind: self.FTT_Ind_JK.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 10000000,
                                minval = lambda: 0,
                                category = 'Economy - Regional')    

            self.FTT_Ind_JB = SD_object('Farmer Terms of Trade - West Java',
                                units = 'Terms Rate',
                                init_value = lambda: self.historical_data('FTT_JB', location, filename), 
                                obtype = 'stock',
                                func = lambda tstep, tind: self.FTT_Ind_JB.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 10000000,
                                minval = lambda: 0,
                                category = 'Economy - Regional')        

            self.FTT_Ind_JT = SD_object('Farmer Terms of Trade - Central Java',
                                units = 'Terms Rate',
                                init_value = lambda: self.historical_data('FTT_JT', location, filename), 
                                obtype = 'stock',
                                func = lambda tstep, tind: self.FTT_Ind_JT.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 10000000,
                                minval = lambda: 0,
                                category = 'Economy - Regional')        

            self.FTT_Ind_JI = SD_object('Farmer Terms of Trade - East Java',
                                units = 'Terms Rate',
                                init_value = lambda: self.historical_data('FTT_JI', location, filename), 
                                obtype = 'stock',
                                func = lambda tstep, tind: self.FTT_Ind_JI.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 10000000,
                                minval = lambda: 0,
                                category = 'Economy - Regional')        

            self.FTT_Ind_SN = SD_object('Farmer Terms of Trade - South Sulawesi',
                                units = 'Terms Rate',
                                init_value = lambda: self.historical_data('FTT_SN', location, filename), 
                                obtype = 'stock',
                                func = lambda tstep, tind: self.FTT_Ind_SN.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 10000000,
                                minval = lambda: 0,
                                category = 'Economy - Regional')                                                                                         

            self.IF_Ind_JK = SD_object('Inflation - Jakarta',
                                units = '%',
                                init_value = lambda: self.historical_data('IF_JK', location, filename), 
                                obtype = 'stock',
                                func = lambda tstep, tind: self.IF_Ind_JK.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 10000000,
                                minval = lambda: 0,
                                category = 'Economy - Regional')    

            self.IF_Ind_JB = SD_object('Inflation - West Java',
                                units = '%',
                                init_value = lambda: self.historical_data('IF_JB', location, filename), 
                                obtype = 'stock',
                                func = lambda tstep, tind: self.IF_Ind_JB.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 10000000,
                                minval = lambda: 0,
                                category = 'Economy - Regional')        

            self.IF_Ind_JT = SD_object('Inflation - Central Java',
                                units = '%',
                                init_value = lambda: self.historical_data('IF_JT', location, filename), 
                                obtype = 'stock',
                                func = lambda tstep, tind: self.IF_Ind_JT.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 10000000,
                                minval = lambda: 0,
                                category = 'Economy - Regional')        

            self.IF_Ind_JI = SD_object('Inflation - East Java',
                                units = '%',
                                init_value = lambda: self.historical_data('IF_JI', location, filename), 
                                obtype = 'stock',
                                func = lambda tstep, tind: self.IF_Ind_JI.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 10000000,
                                minval = lambda: 0,
                                category = 'Economy - Regional')        

            self.IF_Ind_SN = SD_object('Inflation - South Sulawesi',
                                units = '%',
                                init_value = lambda: self.historical_data('IF_SN', location, filename), 
                                obtype = 'stock',
                                func = lambda tstep, tind: self.IF_Ind_SN.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 10000000,
                                minval = lambda: 0,
                                category = 'Economy - Regional')   

            self.foreign_vis_Ind = SD_object('Foreign Visitors',
                                units = 'People',
                                init_value = lambda: self.historical_data('foreign', location, filename), 
                                obtype = 'stock',
                                func = lambda tstep, tind: self.foreign_vis_Ind.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 10000000,
                                minval = lambda: 0,
                                category = 'Economy - Nationwide')   


            self.HO_Ind_JK = SD_object('Hotel Occupancy - Jakarta',
                                units = '%',
                                init_value = lambda: self.historical_data('HO_JK', location, filename), 
                                obtype = 'stock',
                                func = lambda tstep, tind: self.HO_Ind_JK.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 10000000,
                                minval = lambda: 0,
                                category = 'Economy - Regional')    


            self.HO_Ind_JB = SD_object('Hotel Occupancy - West Java',
                                units = '%',
                                init_value = lambda: self.historical_data('HO_JB', location, filename), 
                                obtype = 'stock',
                                func = lambda tstep, tind: self.HO_Ind_JB.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 10000000,
                                minval = lambda: 0,
                                category = 'Economy - Regional')        


            self.HO_Ind_JT = SD_object('Hotel Occupancy - Central Java',
                                units = '%',
                                init_value = lambda: self.historical_data('HO_JT', location, filename), 
                                obtype = 'stock',
                                func = lambda tstep, tind: self.HO_Ind_JT.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 10000000,
                                minval = lambda: 0,
                                category = 'Economy - Regional')        


            self.HO_Ind_JI = SD_object('Hotel Occupancy - East Java',
                                units = '%',
                                init_value = lambda: self.historical_data('HO_JI', location, filename), 
                                obtype = 'stock',
                                func = lambda tstep, tind: self.HO_Ind_JI.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 10000000,
                                minval = lambda: 0,
                                category = 'Economy - Regional')        


            self.HO_Ind_SN = SD_object('Hotel Occupancy - South Sulawesi',
                                units = '%',
                                init_value = lambda: self.historical_data('HO_SN', location, filename), 
                                obtype = 'stock',
                                func = lambda tstep, tind: self.HO_Ind_SN.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 10000000,
                                minval = lambda: 0,
                                category = 'Economy - Regional')   

            """ 8 - MOBILITY """                                                              
            self.Retail_Mob = SD_object('Retail and Recreation Mobility',
                                units = 'Percent Change from Baseline',
                                init_value = lambda: self.historical_data('retail_and_recreation_percent_change_from_baseline', location, filename), #this historical data only goes through late July, so post-late July is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.Retail_Mob.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 100,   
                                minval = lambda: -100, 
                                category = 'Mobility')
  
            self.Grocery_Mob = SD_object('Grocery and Pharmacy Mobility',
                                units = 'Percent Change from Baseline',
                                init_value = lambda: self.historical_data('grocery_and_pharmacy_percent_change_from_baseline', location, filename), #this historical data only goes through late July, so post-late July is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.Grocery_Mob.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 100,
                                minval = lambda: -100,
                                category = 'Mobility')                                                       
  
            self.Parks_Mob = SD_object('Parks Mobility',
                                units = 'Percent Change from Baseline',
                                init_value = lambda: self.historical_data('parks_percent_change_from_baseline', location, filename), #this historical data only goes through late July, so post-late July is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.Parks_Mob.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 100,
                                minval = lambda: -100,
                                category = 'Mobility')    
  
            self.Transit_Mob = SD_object('Transit Mobility',
                                units = 'Percent Change from Baseline',
                                init_value = lambda: self.historical_data('transit_stations_percent_change_from_baseline', location, filename), #this historical data only goes through late July, so post-late July is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.Transit_Mob.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 100,
                                minval = lambda: -100,
                                category = 'Mobility')  
  
            self.Workplace_Mob = SD_object('Workplace Mobility',
                                units = 'Percent Change from Baseline',
                                init_value = lambda: self.historical_data('workplaces_percent_change_from_baseline', location, filename), #this historical data only goes through late July, so post-late July is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.Workplace_Mob.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 100,
                                minval = lambda: -100,
                                category = 'Mobility')   
  
            self.Residential_Mob = SD_object('Residential Mobility',
                                units = 'Percent Change from Baseline',
                                init_value = lambda: self.historical_data('residential_percent_change_from_baseline', location, filename), #this historical data only goes through late July, so post-late July is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.Residential_Mob.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 100,
                                minval = lambda: -100,
                                category = 'Mobility')
            
    # =============================================================================
    # %% 6 - Querétaro  
    # =============================================================================   
        
        if location in ['Querétaro']:
          
            """ 1 - POLICIES & ACTIONS """
            self.ClosureP = SD_object('Closure Policy',
                                        units = 'unitless',
                                        init_value = lambda: self.historical_data('Closure Policy', location, filename),
                                        obtype = 'variable',
                                        func = lambda tstep, tind: self.ClosureP.value(),
                                        datatype = 'stringdict',
                                        category = 'Policies & Actions')
          
          
            """ 2 - HEALTH PARAMETERS """
            self.BaseContactR = SD_object('Base Contact Rate',
                            units = 'people/(day*person)',
                            init_value = 5,
                            obtype = 'variable',
                            func = lambda tstep, tind: self.BaseContactR.value(),
                            category = 'Health Parameters'
                            )
            self.ContactR = SD_object('Contact Rate',
                                    units = 'people/(day*person)',
                                    init_value = self.ClosureP.value() * self.BaseContactR.value(),
                                    obtype = 'variable',
                                    func = lambda tstep, tind: self.ClosureP.value() * self.BaseContactR.value(),
                                    category = 'Health Parameters'
                                    )
            
            self.Infectivity = SD_object('Infectivity',
                                units = 'likelihood/contact',
                                init_value = 0.05,
                                obtype = 'variable',
                                func = lambda tstep, tind: self.Infectivity.value(ind=tind),
                                maxval = lambda: 1,
                                minval = lambda: 0,
                                category = 'Health Parameters')
            
            self.AvDur = SD_object('Average Illness Duration',
                                  units = 'Days',
                                  init_value = 14,
                                  obtype = 'variable',
                                  func = lambda tstep, tind: self.AvDur.value(ind=tind),
                                  maxval = lambda: 300,
                                  minval = lambda: 0,
                                  category = 'Health Parameters')  
            
            self.HosL = SD_object('Hospitalization Likelihood',
                          units = 'probability',
                          init_value = 0.39,
                          obtype = 'variable',
                          func = lambda tstep, tind: self.HosL.value(ind=tind),
                          maxval = lambda: 1,
                          minval = lambda: 0,
                          category = 'Health Parameters')
              
            self.UHML = SD_object('Unhospitalized Mortality Likelihood',
                          units = 'probability',
                          init_value = 0.3,
                          obtype = 'variable',
                          func = lambda tstep, tind: self.UHML.value(ind=tind),
                          maxval = lambda: 1,
                          minval = lambda: 0,
                          category = 'Health Parameters')
              
            self.UHRL = SD_object('Unhospitalized Recovery Likelihood',
                          units = 'probability',
                          init_value = 1-self.UHML.value(),
                          obtype = 'variable',
                          func = lambda tstep, tind: 1 - self.UHML.value(ind=tind),
                          maxval = lambda: 1,
                          minval = lambda: 0,
                          category = 'Health Parameters')
                
            self.HRL = SD_object('Hospitalized Recovery Likelihood',
                          units = 'probability',
                          init_value = 0.9, #lambda: self.HRecovP_func(0, -1),
                          obtype = 'variable',
                          func = lambda tstep, tind: self.HRecovP_func(tstep, tind),
                          maxval = lambda: 1,
                          minval = lambda: 0,
                          category = 'Health Parameters')
              
            self.bHRL = SD_object('Base Hospitalized Recovery Likelihood',
                          units = 'probability',
                          init_value = 0.9,
                          obtype = 'variable',
                          func = lambda tstep, tind: self.bHRL.value(ind=tind),
                          maxval = lambda: 1,
                          minval = lambda: 0,
                          category = 'Health Parameters')
              
            self.HML = SD_object('Hospitalized Mortality Likelihood',
                          units = 'probability',
                          init_value = 1-self.HRL.value(),
                          obtype = 'variable',
                          func = lambda tstep, tind: 1 - self.HRL.value(ind=tind),
                          maxval = lambda: 1,
                          minval = lambda: 0,
                          category = 'Health Parameters')
          
            self.RecL = SD_object('Recovery Likelihood',
                          units = 'probability',
                          init_value = (1-self.HosL.value())*self.UHRL.value() + 
                                        self.HosL.value() * self.HRL.value(),
                          obtype = 'variable',
                          func = lambda tstep, tind: (1-self.HosL.value(ind=tind))*self.UHRL.value(ind=tind) + 
                                        self.HosL.value(ind=tind) * self.HRL.value(ind=tind),
                          maxval = lambda: 1,
                          minval = lambda: 0,
                          category = 'Health Parameters')
              
            self.MorL = SD_object('Mortality Likelihood',
                          units = 'probability',
                          init_value = (1-self.HosL.value())*self.UHML.value() + 
                                        self.HosL.value() * self.HML.value(),
                          obtype = 'variable',
                          func = lambda tstep, tind: (1-self.HosL.value(ind=tind))*self.UHML.value(ind=tind) + 
                                        self.HosL.value(ind=tind) * self.HML.value(ind=tind),
                          maxval = lambda: 1,
                          minval = lambda: 0,
                          category = 'Health Parameters')
              
            self.AvHDur = SD_object('Average Hospitalization Duration',
                          units = 'Days',
                          init_value = 7,
                          obtype = 'variable',
                          func = lambda tstep, tind: self.AvHDur.value(ind=tind),
                          maxval = lambda: 300,
                          minval = lambda: 0,
                          category = 'Health Parameters')
            
          
            """ 3 - HEALTH POPULATIONS """
            self.SPop = SD_object('Susceptible Population',
                                  units = 'people',
                                  init_value = lambda: self.historical_data('Susceptible Population', location, filename),
                                  obtype = 'stock',
                                  func = lambda tstep, tind: self.SPop.value(ind=tind) - self.InfectR.value(ind=tind) * tstep,
                                  maxval = lambda: 1000000000,
                                  minval = lambda: 0,
                                  category = 'Health Populations')
            
            self.IPop = SD_object("'Estimated' Unhospitalized Infected Population",
                                units = 'people',
                                init_value = lambda: self.historical_data('True Unhospitalized Infected', location, filename),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.IPop.value(ind=tind) + (self.InfectR.value(ind=tind) - self.UHMR.value(ind=tind) - 
                                                                          self.HosR.value(ind=tind) - self.UHRR.value(ind=tind)) * tstep,
                                maxval = lambda: 100000000,
                                minval = lambda: 0,
                                category = 'Health Populations')
          
            self.Deaths = SD_object('Deaths',
                                units = 'people',
                                init_value = lambda: self.historical_data('Accumulative Deaths', location, filename),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.Deaths.value(ind=tind) + (self.UHMR.value(ind=tind) + self.HMR.value(ind=tind)) * tstep,
                                maxval = lambda: 100000000,
                                minval = lambda: 0,
                                category = 'Health Populations')
              
            self.HPop = SD_object('Hospitalized Population',
                                units = 'people',
                                init_value = lambda: self.historical_data('Hospitalized Population', location, filename),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.HPop.value(ind=tind) + (self.HosR.value(ind=tind) - self.HMR.value(ind=tind) - self.HRR.value(ind=tind)) * tstep,
                                maxval = lambda: 1000000,
                                minval = lambda: 0,
                                category = 'Health Populations')
              
            self.RPop = SD_object('Known Recovered Population',
                                units = 'people',
                                init_value = lambda: self.historical_data('Recovered Population', location, filename),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.RPop.value(ind=tind) + (self.UHRR.value(ind=tind) + self.HRR.value(ind=tind)) * tstep,
                                maxval = lambda: 100000000,
                                minval = lambda: 0,
                                category = 'Health Populations')
              
            self.mIPop = SD_object("Measured Unhospitalized Infected Population",
                                units = 'people',
                                init_value = lambda: self.historical_data('Measured Unhospitalized Infected', location, filename),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.true_to_measured(self.IPop, 14, 0.25),
                                maxval = lambda: 100000000,
                                minval = lambda: 0,
                                category = 'Health Populations')
              
            self.mTotIPop = SD_object('Measured Total Infected Population',
                                units = 'people',
                                init_value = self.historical_data('Measured Current Infected', location, filename),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.mIPop.value(ind=tind) + self.HPop.value(ind=tind),
                                maxval = lambda: 100000000,
                                minval = lambda: 0,
                                category = 'Health Populations')
              
            self.TotIPop = SD_object("'Estimated' Total Infected Population",
                                units = 'people',
                                init_value = self.IPop.value() + self.HPop.value(),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.IPop.value(ind=tind) + self.HPop.value(ind=tind),
                                maxval = lambda: 100000000,
                                minval = lambda: 0,
                                category = 'Health Populations')
            
            
          
            """ 4 - HEALTH FLOWS """
            self.InfectR = SD_object("'Estimated' Infection Rate",
                                      units = 'people/day',
                                      init_value = lambda: self.historical_data('True Infection Rate', location, filename),
                                      obtype = 'flow',
                                      func = lambda tstep, tind: (self.combos(self.SPop.value(ind=tind) + self.IPop.value(ind=tind)) - self.combos(self.SPop.value(ind=tind)) - self.combos(self.IPop.value(ind=tind))) / 
                                                          self.combos(self.SPop.value(ind=tind) + self.IPop.value(ind=tind)) * self.ContactR.value(ind=tind) * (self.SPop.value(ind=tind) + self.IPop.value(ind=tind)) * self.Infectivity.value(ind=tind),
                                      maxval = lambda: self.SPop.value(),
                                      minval = lambda: 0,
                                      category = 'Health Flows'
                                      )
                  
            self.mInfectR = SD_object("Measured Infection Rate",
                                      units = 'people/day',
                                      init_value = lambda: self.historical_data('Measured Infection Rate',  location, filename),
                                      obtype = 'flow',
                                      func = lambda tstep, tind: self.true_to_measured(self.InfectR, 14, 0.25),
                                      maxval = lambda: self.SPop.value(),
                                      minval = lambda: 0,
                                      category = 'Health Flows'
                                      )
            
            self.UHRR = SD_object('Unhospitalized Recovery Rate',
                                  units = 'people/day',
                                  init_value = (1 - self.HosL.value()) * self.UHRL.value() * self.IPop.value() / self.AvDur.value(),
                                  obtype = 'flow',
                                  func = lambda tstep, tind: (1 - self.HosL.value(ind=tind)) * self.UHRL.value(ind=tind) * self.IPop.value(ind=tind) / self.AvDur.value(ind=tind),
                                  maxval = lambda: self.IPop.value(),
                                  minval = lambda: 0,
                                  category = 'Health Flows'
                                  )
              
            self.UHMR = SD_object('Unhospitalized Mortality Rate',
                                  units = 'people/day',
                                  init_value = (1 - self.HosL.value()) * self.UHML.value() * self.IPop.value() / self.AvDur.value(),
                                  obtype = 'flow',
                                  func = lambda tstep, tind: (1 - self.HosL.value(ind=tind)) * self.UHML.value(ind=tind) * self.IPop.value(ind=tind) / self.AvDur.value(ind=tind),
                                  maxval = lambda: self.IPop.value(),
                                  minval = lambda: 0,
                                  category = 'Health Flows'
                                  )
              
            self.HRR = SD_object('Hospital Recovery Rate',
                                  units = 'people/day',
                                  init_value = self.HRL.value() * self.HPop.value() / self.AvHDur.value(),
                                  obtype = 'flow',
                                  func = lambda tstep, tind: self.HRL.value(ind=tind) * self.HPop.value(ind=tind) / self.AvHDur.value(ind=tind),
                                  maxval = lambda: self.HPop.value(),
                                  minval = lambda: 0,
                                  category = 'Health Flows'
                                  )
              
            self.HMR = SD_object('Hospital Mortaility Rate',
                                  units = 'people/day',
                                  init_value = int(round(self.HML.value() * self.HPop.value() / self.AvHDur.value())),
                                  obtype = 'flow',
                                  func = lambda tstep, tind: self.HML.value(ind=tind) * self.HPop.value(ind=tind) / self.AvHDur.value(ind=tind),
                                  maxval = lambda: self.HPop.value(),
                                  minval = lambda: 0,
                                  category = 'Health Flows'
                                  )
              
            self.HosR = SD_object('Hospitalization Rate',
                                  units = 'people/day',
                                  init_value = lambda: self.historical_data('Hospitalization Rate', location, filename),
                                  obtype = 'flow',
                                  func = lambda tstep, tind: self.HosL.value(ind=tind) * self.IPop.value(ind=tind) / self.AvDur.value(ind=tind),
                                  maxval = lambda: self.IPop.value(),
                                  minval = lambda: 0,
                                  category = 'Health Flows'
                                  )
            
            """ 5 - EQUIPMENT SUPPLIES """
            self.HBeds = SD_object('Hospital Bed Capacity',
                        units = 'people',
                        init_value = 2000,
                        obtype = 'variable',
                        func = lambda tstep, tind: self.HBeds.value(ind=tind),
                        maxval = lambda: 1000000,
                        minval = lambda: 0,
                        category = 'Equipment Supplies')
              
            """ 7 - MOBILITY """
            
            self.nat_retail_recreation_mob = SD_object('National Retail and Recreation Mobility',
                                units = 'Mobility Index',
                                init_value = lambda: self.historical_data('nat_retail_recreation_mob', location, filename), #this historical data only goes through late July, so post-late July is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.nat_retail_recreation_mob.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 100,   
                                minval = lambda: -100, 
                                category = 'Mobility')
            
            self.nat_grocery__pharmacy_mob = SD_object('National Grocery and Pharmacy Mobility',
                                units = 'Mobility Index',
                                init_value = lambda: self.historical_data('nat_grocery__pharmacy_mob', location, filename), #this historical data only goes through late July, so post-late July is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.nat_grocery__pharmacy_mob.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 100,   
                                minval = lambda: -100, 
                                category = 'Mobility')
            
            self.nat_parks_mob = SD_object('National Parks Mobility',
                                units = 'Mobility Index',
                                init_value = lambda: self.historical_data('nat_parks_mob', location, filename), #this historical data only goes through late July, so post-late July is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.nat_parks_mob.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 100,   
                                minval = lambda: -100, 
                                category = 'Mobility')
            
            self.nat_transit_mob = SD_object('National Transit Stations Mobility',
                                units = 'Mobility Index',
                                init_value = lambda: self.historical_data('nat_transit_mob', location, filename), #this historical data only goes through late July, so post-late July is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.nat_transit_mob.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 100,   
                                minval = lambda: -100, 
                                category = 'Mobility')
            
            self.nat_workplaces_mob = SD_object('National Workplaces Mobility',
                                units = 'Mobility Index',
                                init_value = lambda: self.historical_data('nat_workplaces_mob', location, filename), #this historical data only goes through late July, so post-late July is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.nat_workplaces_mob.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 100,   
                                minval = lambda: -100, 
                                category = 'Mobility')
            
            self.nat_residential_mob = SD_object('National Residential Mobility',
                                units = 'Mobility Index',
                                init_value = lambda: self.historical_data('nat_residential_mob', location, filename), #this historical data only goes through late July, so post-late July is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.nat_residential_mob.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 100,   
                                minval = lambda: -100, 
                                category = 'Mobility')
            
            self.loc_retail_recreation_mob = SD_object('Querétaro Retail and Recreation Mobility',
                                units = 'Mobility Index',
                                init_value = lambda: self.historical_data('loc_retail_recreation_mob', location, filename), #this historical data only goes through late July, so post-late July is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.loc_retail_recreation_mob.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 100,   
                                minval = lambda: -100, 
                                category = 'Mobility')
            
            self.loc_grocery__pharmacy_mob = SD_object('Querétaro Grocery and Pharmacy Mobility',
                                units = 'Mobility Index',
                                init_value = lambda: self.historical_data('loc_grocery__pharmacy_mob', location, filename), #this historical data only goes through late July, so post-late July is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.loc_grocery__pharmacy_mob.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 100,   
                                minval = lambda: -100, 
                                category = 'Mobility')
            
            self.loc_parks_mob = SD_object('Querétaro Parks Mobility',
                                units = 'Mobility Index',
                                init_value = lambda: self.historical_data('loc_parks_mob', location, filename), #this historical data only goes through late July, so post-late July is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.loc_parks_mob.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 100,   
                                minval = lambda: -100, 
                                category = 'Mobility')
            
            self.loc_transit_mob = SD_object('Querétaro Transit Stations Mobility',
                                units = 'Mobility Index',
                                init_value = lambda: self.historical_data('loc_transit_mob', location, filename), #this historical data only goes through late July, so post-late July is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.loc_transit_mob.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 100,   
                                minval = lambda: -100, 
                                category = 'Mobility')
            
            self.loc_workplaces_mob = SD_object('Querétaro Workplaces Mobility',
                                units = 'Mobility Index',
                                init_value = lambda: self.historical_data('loc_workplaces_mob', location, filename), #this historical data only goes through late July, so post-late July is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.loc_workplaces_mob.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 100,   
                                minval = lambda: -100, 
                                category = 'Mobility')
            
            self.loc_residential_mob = SD_object('Querétaro Residential Mobility',
                                units = 'Mobility Index',
                                init_value = lambda: self.historical_data('loc_residential_mob', location, filename), #this historical data only goes through late July, so post-late July is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.loc_residential_mob.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 100,   
                                minval = lambda: -100, 
                                category = 'Mobility')
           
            
    # =============================================================================
    # %% 7 - Luanda  
    # =============================================================================   
        
        if location in ['Luanda']:
          
            """ 1 - POLICIES & ACTIONS """
            self.ClosureP = SD_object('Closure Policy',
                                        units = 'unitless',
                                        init_value = lambda: self.historical_data('Closure Policy', location, filename),
                                        obtype = 'variable',
                                        func = lambda tstep, tind: self.ClosureP.value(),
                                        datatype = 'stringdict',
                                        category = 'Policies & Actions')
            
            
            
            """ 2 - HEALTH PARAMETERS """
            self.BaseContactR = SD_object('Base Contact Rate',
                            units = 'people/(day*person)',
                            init_value = 5,
                            obtype = 'variable',
                            func = lambda tstep, tind: self.BaseContactR.value(),
                            category = 'Health Parameters'
                            )
            self.ContactR = SD_object('Contact Rate',
                                    units = 'people/(day*person)',
                                    init_value = self.ClosureP.value() * self.BaseContactR.value(),
                                    obtype = 'variable',
                                    func = lambda tstep, tind: self.ClosureP.value() * self.BaseContactR.value(),
                                    category = 'Health Parameters'
                                    )
            
            self.Infectivity = SD_object('Infectivity',
                                units = 'likelihood/contact',
                                init_value = 0.01,
                                obtype = 'variable',
                                func = lambda tstep, tind: self.Infectivity.value(ind=tind),
                                maxval = lambda: 1,
                                minval = lambda: 0,
                                category = 'Health Parameters')
            
            self.AvDur = SD_object('Average Illness Duration',
                                  units = 'Days',
                                  init_value = 14,
                                  obtype = 'variable',
                                  func = lambda tstep, tind: self.AvDur.value(ind=tind),
                                  maxval = lambda: 300,
                                  minval = lambda: 0,
                                  category = 'Health Parameters')
            
            self.RecL = SD_object('Recovery Likelihood',
                        units = 'probability',
                        init_value = 0.79,
                        obtype = 'variable',
                        func = lambda tstep, tind: self.RecL.value(ind=tind),
                        maxval = lambda: 1,
                        minval = lambda: 0,
                        category = 'Health Parameters')
              
            self.MorL = SD_object('Mortality Likelihood',
                        units = 'probability',
                        init_value = 1-self.RecL.value(),
                        obtype = 'variable',
                        func = lambda tstep, tind: 1-self.RecL.value(ind=tind),
                        maxval = lambda: 1,
                        minval = lambda: 0,
                        category = 'Health Parameters')
          
          
            """ 3 - HEALTH POPULATIONS """
            self.SPop = SD_object('National Susceptible Population',
                                  units = 'people',
                                  init_value = lambda: self.historical_data('Susceptible Population', location, filename),
                                  obtype = 'stock',
                                  func = lambda tstep, tind: self.SPop.value(ind=tind) - self.InfectR.value(ind=tind) * tstep,
                                  maxval = lambda: 1000000000,
                                  minval = lambda: 0,
                                  category = 'Health Populations')
            
            self.IPop = SD_object("'Estimated' National Infected Population",
                                units = 'people',
                                init_value = lambda: self.historical_data('True Infected', location, filename),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.IPop.value(ind=tind) + (self.InfectR.value(ind=tind)  - 
                                                                          self.RR.value(ind=tind) - self.MR.value(ind=tind)) * tstep,
                                maxval = lambda: 100000000,
                                minval = lambda: 0,
                                category = 'Health Populations')
          
            self.Deaths = SD_object('National Deaths',
                                units = 'people',
                                init_value = lambda: self.historical_data('Deaths', location, filename),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.Deaths.value(ind=tind) + self.MR.value(ind=tind) * tstep,
                                maxval = lambda: 100000000,
                                minval = lambda: 0,
                                category = 'Health Populations')
              
            self.RPop = SD_object('National Known Recovered Population',
                                units = 'people',
                                init_value = lambda: self.historical_data('Recoveries', location, filename),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.RPop.value(ind=tind) + self.RR.value(ind=tind) * tstep,
                                maxval = lambda: 100000000,
                                minval = lambda: 0,
                                category = 'Health Populations')
              
            self.mIPop = SD_object("National Measured Infected Population",
                                units = 'people',
                                init_value = lambda: self.historical_data('Measured Current Infected', location, filename),
                                obtype = 'stock',
                                func = lambda tstep, tind: self.true_to_measured(self.IPop, 14, 0.25),
                                maxval = lambda: 100000000,
                                minval = lambda: 0,
                                category = 'Health Populations')
          
          
            """ 4 - HEALTH FLOWS """
            self.InfectR = SD_object("National 'Estimated' Infection Rate",
                                      units = 'people/day',
                                      init_value = lambda: self.historical_data('True Infection Rate', location, filename),
                                      obtype = 'flow',
                                      func = lambda tstep, tind: (self.combos(self.SPop.value(ind=tind) + self.IPop.value(ind=tind)) - self.combos(self.SPop.value(ind=tind)) - self.combos(self.IPop.value(ind=tind))) / 
                                                          self.combos(self.SPop.value(ind=tind) + self.IPop.value(ind=tind)) * self.ContactR.value(ind=tind) * (self.SPop.value(ind=tind) + self.IPop.value(ind=tind)) * self.Infectivity.value(ind=tind),
                                      maxval = lambda: self.SPop.value(),
                                      minval = lambda: 0,
                                      category = 'Health Flows'
                                      )
                  
            self.mInfectR = SD_object("National Measured Infection Rate",
                                      units = 'people/day',
                                      init_value = lambda: self.historical_data('Measured Infection Rate',  location, filename),
                                      obtype = 'flow',
                                      func = lambda tstep, tind: self.true_to_measured(self.InfectR, 14, 0.25),
                                      maxval = lambda: self.SPop.value(),
                                      minval = lambda: 0,
                                      category = 'Health Flows'
                                      )
            
            self.RR = SD_object('National Recovery Rate',
                                  units = 'people/day',
                                  init_value = self.RecL.value() * self.IPop.value() / self.AvDur.value(),
                                  # init_value = 1,
                                  obtype = 'flow',
                                  func = lambda tstep, tind: self.RecL.value(ind=tind) * self.IPop.value(ind=tind) / self.AvDur.value(ind=tind),
                                  maxval = lambda: self.IPop.value(),
                                  minval = lambda: 0,
                                  category = 'Health Flows'
                                  )
              
            self.MR = SD_object('National Mortality Rate',
                                  units = 'people/day',
                                  init_value = self.MorL.value() * self.IPop.value() / self.AvDur.value(),
                                  obtype = 'flow',
                                  func = lambda tstep, tind: self.MorL.value(ind=tind) * self.IPop.value(ind=tind) / self.AvDur.value(ind=tind),
                                  maxval = lambda: self.IPop.value(),
                                  minval = lambda: 0,
                                  category = 'Health Flows'
                                  )
            
            
            """ 5 - EQUIPMENT SUPPLIES """
            
            """ 6 - EQUIPMENT PARAMETERS """
            
            """ 7 - MOBILITY """
            
            self.nat_retail_recreation_mob = SD_object('National Retail and Recreation Mobility',
                                units = 'Mobility Index',
                                init_value = lambda: self.historical_data('nat_retail_recreation_mob', location, filename), #this historical data only goes through late July, so post-late July is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.nat_retail_recreation_mob.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 100,   
                                minval = lambda: -100, 
                                category = 'Mobility')
            
            self.nat_grocery__pharmacy_mob = SD_object('National Grocery and Pharmacy Mobility',
                                units = 'Mobility Index',
                                init_value = lambda: self.historical_data('nat_grocery__pharmacy_mob', location, filename), #this historical data only goes through late July, so post-late July is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.nat_grocery__pharmacy_mob.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 100,   
                                minval = lambda: -100, 
                                category = 'Mobility')
            
            self.nat_parks_mob = SD_object('National Parks Mobility',
                                units = 'Mobility Index',
                                init_value = lambda: self.historical_data('nat_parks_mob', location, filename), #this historical data only goes through late July, so post-late July is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.nat_parks_mob.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 100,   
                                minval = lambda: -100, 
                                category = 'Mobility')
            
            self.nat_transit_mob = SD_object('National Transit Stations Mobility',
                                units = 'Mobility Index',
                                init_value = lambda: self.historical_data('nat_transit_mob', location, filename), #this historical data only goes through late July, so post-late July is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.nat_transit_mob.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 100,   
                                minval = lambda: -100, 
                                category = 'Mobility')
            
            self.nat_workplaces_mob = SD_object('National Workplaces Mobility',
                                units = 'Mobility Index',
                                init_value = lambda: self.historical_data('nat_workplaces_mob', location, filename), #this historical data only goes through late July, so post-late July is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.nat_workplaces_mob.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 100,   
                                minval = lambda: -100, 
                                category = 'Mobility')
            
            self.nat_residential_mob = SD_object('National Residential Mobility',
                                units = 'Mobility Index',
                                init_value = lambda: self.historical_data('nat_residential_mob', location, filename), #this historical data only goes through late July, so post-late July is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.nat_residential_mob.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 100,   
                                minval = lambda: -100, 
                                category = 'Mobility')
            
            self.loc_retail_recreation_mob = SD_object('Luanda Retail and Recreation Mobility',
                                units = 'Mobility Index',
                                init_value = lambda: self.historical_data('loc_retail_recreation_mob', location, filename), #this historical data only goes through late July, so post-late July is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.loc_retail_recreation_mob.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 100,   
                                minval = lambda: -100, 
                                category = 'Mobility')
            
            self.loc_grocery__pharmacy_mob = SD_object('Luanda Grocery and Pharmacy Mobility',
                                units = 'Mobility Index',
                                init_value = lambda: self.historical_data('loc_grocery__pharmacy_mob', location, filename), #this historical data only goes through late July, so post-late July is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.loc_grocery__pharmacy_mob.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 100,   
                                minval = lambda: -100, 
                                category = 'Mobility')
            
            self.loc_parks_mob = SD_object('Luanda Parks Mobility',
                                units = 'Mobility Index',
                                init_value = lambda: self.historical_data('loc_parks_mob', location, filename), #this historical data only goes through late July, so post-late July is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.loc_parks_mob.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 100,   
                                minval = lambda: -100, 
                                category = 'Mobility')
            
            self.loc_transit_mob = SD_object('Luanda Transit Stations Mobility',
                                units = 'Mobility Index',
                                init_value = lambda: self.historical_data('loc_transit_mob', location, filename), #this historical data only goes through late July, so post-late July is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.loc_transit_mob.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 100,   
                                minval = lambda: -100, 
                                category = 'Mobility')
            
            self.loc_workplaces_mob = SD_object('Luanda Workplaces Mobility',
                                units = 'Mobility Index',
                                init_value = lambda: self.historical_data('loc_workplaces_mob', location, filename), #this historical data only goes through late July, so post-late July is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.loc_workplaces_mob.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 100,   
                                minval = lambda: -100, 
                                category = 'Mobility')
            
            self.loc_residential_mob = SD_object('Luanda Residential Mobility',
                                units = 'Mobility Index',
                                init_value = lambda: self.historical_data('loc_residential_mob', location, filename), #this historical data only goes through late July, so post-late July is a placeholder value
                                obtype = 'stock',
                                func = lambda tstep, tind: self.loc_residential_mob.value(ind=tind), #this function is a placeholder taken from Air passengers in Chile
                                maxval = lambda: 100,   
                                minval = lambda: -100, 
                                category = 'Mobility')
            
            
            
            """ 8 - ECONOMIC """
            
            self.ShipsLuanda = SD_object('Ships in Luanda Bay',
                                units = 'ships',
                                        init_value = lambda: self.historical_data('Ships in Luanda Bay', location, filename),
                                        obtype = 'stock',
                                        func = lambda tstep, tind: self.ShipsLuanda.value(),
                                        maxval = lambda: 1000,
                                        minval = lambda: 0,
                                        category = 'Economy')
            
            self.ShipsOffshore = SD_object('Ships in Offshore Area',
                                        units = 'ships',
                                        init_value = lambda: self.historical_data('Ships in Offshore Area', location, filename),
                                        obtype = 'stock',
                                        func = lambda tstep, tind: self.ShipsOffshore.value(),
                                        maxval = lambda: 1000,
                                        minval = lambda: 0,
                                        category = 'Economy')
                        
            self.ShipsLobito = SD_object('Ships in Lobito Bay',
                                        units = 'ships',
                                        init_value = lambda: self.historical_data('Ships in Lobito Bay', location, filename),
                                        obtype = 'stock',
                                        func = lambda tstep, tind: self.ShipsLobito.value(),
                                        maxval = lambda: 1000,
                                        minval = lambda: 0,
                                        category = 'Economy')
              
            
            
            """ 9 - ENVIRONMENT """
            
            self.LC_NightRad = SD_object('Nighttime Radiance in Luanda City',
                                        units = 'radiance',
                                        init_value = lambda: self.historical_data('Luanda City Nighttime Radiance', location, filename),
                                        obtype = 'stock',
                                        func = lambda tstep, tind: self.LC_NightRad.value(),
                                        maxval = lambda: 1000,
                                        minval = lambda: 0,
                                        category = 'Environment')
            
            self.ZEE_NightRad = SD_object('Nighttime Radiance in ZEE',
                                        units = 'radiance',
                                        init_value = lambda: self.historical_data('ZEE Nighttime Radiance', location, filename),
                                        obtype = 'stock',
                                        func = lambda tstep, tind: self.ZEE_NightRad.value(),
                                        maxval = lambda: 1000,
                                        minval = lambda: 0,
                                        category = 'Environment')
            
            self.SO2_PerChange_Huambo = SD_object('SO2 Percent Change in Huambo City',
                                        units = '% Change Relative to Previous Year',
                                        init_value = lambda: self.historical_data('SO2_PercentChange_HuamboCity', location, filename),
                                        obtype = 'stock',
                                        func = lambda tstep, tind: self.SO2_PerChange_Huambo.value(),
                                        maxval = lambda: 100,
                                        minval = lambda: -100,
                                        category = 'Environment')
            
            self.SO2_PerChange_Luanda = SD_object('SO2 Percent Change in Luanda City',
                                        units = '% Change Relative to Previous Year',
                                        init_value = lambda: self.historical_data('SO2_PercentChange_LuandaCity', location, filename),
                                        obtype = 'stock',
                                        func = lambda tstep, tind: self.SO2_PercentChange_LuandaCity.value(),
                                        maxval = lambda: 100,
                                        minval = lambda: -100,
                                        category = 'Environment')
            
            self.SO2_PerChange_ZEE = SD_object('SO2 Percent Change in ZEE',
                                        units = '% Change Relative to Previous Year',
                                        init_value = lambda: self.historical_data('SO2_PercentChange_ZEE', location, filename),
                                        obtype = 'stock',
                                        func = lambda tstep, tind: self.SO2_PerChange_ZEE.value(),
                                        maxval = lambda: 100,
                                        minval = lambda: -100,
                                        category = 'Environment')
            
            self.NO2_PerChange_Huambo = SD_object('NO2 Percent Change in Huambo City',
                                        units = '% Change Relative to Previous Year',
                                        init_value = lambda: self.historical_data('NO2_PercentChange_HuamboCity', location, filename),
                                        obtype = 'stock',
                                        func = lambda tstep, tind: self.NO2_PerChange_Huambo.value(),
                                        maxval = lambda: 100,
                                        minval = lambda: -100,
                                        category = 'Environment')
            
            self.NO2_PerChange_Luanda = SD_object('NO2 Percent Change in Luanda City',
                                        units = '% Change Relative to Previous Year',
                                        init_value = lambda: self.historical_data('NO2_PercentChange_LuandaCity', location, filename),
                                        obtype = 'stock',
                                        func = lambda tstep, tind: self.NO2_PercentChange_LuandaCity.value(),
                                        maxval = lambda: 100,
                                        minval = lambda: -100,
                                        category = 'Environment')
            
            self.NO2_PerChange_ZEE = SD_object('NO2 Percent Change in ZEE',
                                        units = '% Change Relative to Previous Year',
                                        init_value = lambda: self.historical_data('NO2_PercentChange_ZEE', location, filename),
                                        obtype = 'stock',
                                        func = lambda tstep, tind: self.NO2_PerChange_ZEE.value(),
                                        maxval = lambda: 100,
                                        minval = lambda: -100,
                                        category = 'Environment')
            
          

    # =============================================================================
    # %% 5 - Adjustments for Tuning  
    # =============================================================================   
        
        #Determine the longest list of historical data
        maxtimelist = []
        SD_dict = self.__dict__.copy()
        for SDattribute in SD_dict:
            maxtimelist.append(len(self.__dict__[SDattribute].values))
        maxtime = max(maxtimelist)
        timeSeries = list(range(0,maxtime))
        
        #Add values to beginning of each SD_Objects history so that all values are the same length
        #Specifically uses the current first value to backfill appropriately
        for SDattribute in SD_dict:
            vallen = len(self.__dict__[SDattribute].values)
            timelen = len(timeSeries)
            if vallen < timelen:
                timedif = timelen - vallen
                list_add = [self.__dict__[SDattribute].values[-1]] * timedif
                self.__dict__[SDattribute].values[0:0] = list_add
        
        #Set initial value to either being a single value or the full history, depending on tuning setting
        for SDattribute in SD_dict:
            if tuning_flag == 1:
                history = [] 
                history.extend(self.__dict__[SDattribute].values)
                self.__dict__[SDattribute].history = history
                self.__dict__[SDattribute].values = [history[0]]
            if tuning_flag == 0:
                history = []
                history.extend(self.__dict__[SDattribute].values)
                self.__dict__[SDattribute].history = history
                
    
    # =============================================================================
    # %% 6 - Multi-line Update Functions
    # =============================================================================  
        

    def true_to_measured(self, ob, delay, error_std):
        """GENERATING A MEASUREMENT VALUE BASED ON A TRUE VALUE
        
        Args:
            ob: object that is the true value
            delay: temporal delay between true value and measured value
            error_std: standard deviation of normally distributed measurement error
        
        Returns:
            N/A
        """
        if len(ob.values) > delay:
            trueValue = ob.values[-1*delay]
            measuredValue = float(np.random.normal(trueValue, abs(error_std*trueValue), 1))
        else:
            measuredValue = 0
        
        return measuredValue
    
    
    def HRecovP_func(self, tstep, tind):
        """HOSPITAL RECOVERY RATE UPDATE FUNCTION
        
        Args:
            tstep: the length of time to simulate into the future
            tind: the index of values with which to refer to other SD objects
        
        Returns:
            N/A
        """
        
        baseprob = self.bHRL.value(ind=tind)
        rprob = baseprob
        
        #Adjust recovery rate based on relative hospitalized population and available beds
        if self.HPop.value(ind=tind) > self.HBeds.value(ind=tind):
            rprob = baseprob * 0.4
        
        return rprob   
        
    
    def RioEmploymentR_update(self, tstep, tind):
        """EMPLOYMENT RATE RATE OF CHANGE UPDATE
        
        Args:
            tstep: the length of time to simulate into the future
            tind: the index of values with which to refer to other SD objects
        
        Returns:
            N/A
        """
        if self.RioEmployment.value(ind=tind) < self.RioEmployment.values[0]:
            base_EmpR = np.random.normal(-0.005, 0.0025, 1)
        else:
            base_EmpR = np.random.normal(0, 0.0025, 1)
        EmpR = base_EmpR
        ClosureVal = self.ClosureP.value(ind=tind)
        
        if 0.7 < ClosureVal < 1:
            EmpR = np.random.normal(0.0005, 0.0003, 1)
        elif 0.3 < ClosureVal <= 0.7:
            EmpR = np.random.normal(0.001, 0.005, 1)
        elif ClosureVal <= 0.3:
            EmpR = np.random.normal(0.0015, 0.0055, 1) 
            
        EmpR = EmpR + self.TotIPop.value(ind=tind)/50000000
        return float(EmpR)
    
    
    def BraEmploymentR_update(self, tstep, tind):
        """EMPLOYMENT RATE RATE OF CHANGE UPDATE
        
        Args:
            tstep: the length of time to simulate into the future
            tind: the index of values with which to refer to other SD objects
        
        Returns:
            N/A
        """
        if self.BraEmployment.value(ind=tind) < self.BraEmployment.values[0]:
            base_EmpR = np.random.normal(-0.005, 0.0025, 1)
        else:
            base_EmpR = np.random.normal(0, 0.0025, 1)
        EmpR = base_EmpR
        ClosureVal = self.ClosureP.value(ind=tind)
        
        if 0.7 < ClosureVal < 1:
            EmpR = np.random.normal(0.0005, 0.0003, 1)
        elif 0.3 < ClosureVal <= 0.7:
            EmpR = np.random.normal(0.001, 0.005, 1)
        elif ClosureVal <= 0.3:
            EmpR = np.random.normal(0.0015, 0.0055, 1) 
            
        EmpR = EmpR + self.TotIPop.value(ind=tind)/50000000
        return float(EmpR)
       
        
    # =============================================================================
    # %% 7 - Auxillary Functions 
    # =============================================================================  
        

    
    def PolicyDicts(self, location):
        """GENERATE DICTIONARY DEFINING THE ALL POLICY ACTIONS. EACH ENTRY
        CONTAINS ITS OWN DICTIONARY WITH POLICY OPTIONS
        
        Args:
            location: the application location of the SD_System
            
        Returns:
            PolicyDictsOut: Dictionary of Policy Actions, each containging a 
            directionary relating string titles of policy options to 
                numerical values generally according with effectiveness
        """
        
        PolicyDictsOut = dict()
        if location == 'Rio de Janeiro':
            # PolicyDictsOut['Closure Policy'] = {'No Closures' : 1,
            #                                     'Conservative' : 0.8,
            #                                     'Fase 6b' : 0.75,
            #                                     'Fase 6a' : 0.65,
            #                                     'Fase 5': 0.6,
            #                                     'Fase 4' : 0.5,
            #                                     'Fase 3b': 0.45,
            #                                     'Fase 3a': 0.4,
            #                                     'Fase 2': 0.3,
            #                                     'Fase 1': 0.2,
            #                                     'Initial Closures': 0.1}
            PolicyDictsOut['Closure Policy'] = {'No Closures' : 1,
                                                'Conservative' : 0.68,
                                                'Fase 6b' : 0.66,
                                                'Fase 6a' : 0.64,
                                                'Fase 5': 0.62,
                                                'Fase 4' : 0.6,
                                                'Fase 3b': 0.57,
                                                'Fase 3a': 0.55,
                                                'Fase 2': 0.3,
                                                'Fase 1': 0.1,
                                                'Initial Closures': 0.05}

            PolicyDictsOut['Social Distancing Policy'] = {'No Distancing' : 1,
                                                        'Voluntary Social Distancing' : 0.6,
                                                        'Mandatory Social Distancing' : 0.1}
            
        elif location in ['Chile', 'Santiago']:
            PolicyDictsOut['Closure Policy'] = {'No Closures' : 1,
                            'Stage 5': 0.8,
                            'Stage 4' : 0.7,
                            'Stage 3': 0.5,
                            'Stage 2': 0.4,
                            'Stage 1': 0.2,
                            'Initial Closures':0.1}
            PolicyDictsOut['Curfew Policy'] = {'No Curfew' : 1,
                                                'Unenforced Curfew' : 0.6,
                                                'Enforced Curfew' : 0.1}
            
             
        elif location == 'Indonesia':
            #nationwide
            PolicyDictsOut['Closure Policy'] = {'No Closures' : 1,
                                                'Relaxed Social Restrictions': 0.66,
                                                'High Social Restrictions' : 0.33}

            PolicyDictsOut['Social Distancing Policy'] = {'No Distancing' : 1,
                                                        'Voluntary Social Distancing' : 0.6,
                                                        'Mandatory Social Distancing' : 0.1}

            #island specific
            PolicyDictsOut['Closure Policy Sulawesi'] = {'No Closures' : 1,
                                                'Relaxed Social Restrictions - Zonal': 0.66,
                                                'Relaxed Social Restrictions - Provincial': 0.4,
                                                'High Social Restrictions - Zonal': 0.33,
                                                'High Social Restrictions - Provincial' : 0.25}

            PolicyDictsOut['Closure Policy Java'] = {'No Closures' : 1,
                                                'Relaxed Social Restrictions - Zonal': 0.66,
                                                'Relaxed Social Restrictions - Provincial': 0.4,
                                                'High Social Restrictions - Zonal': 0.33,
                                                'High Social Restrictions - Provincial' : 0.25}

            PolicyDictsOut['Social Distancing Policy Sulawesi'] = {'No Distancing' : 1,
                                                        'Voluntary Social Distancing - Zonal': 0.75,
                                                        'Voluntary Social Distancing - Provincial' : 0.5,
                                                        'Mandatory Social Distancing - Zonal': 0.25,
                                                        'Mandatory Social Distancing - Provincial' : 0.1}

            PolicyDictsOut['Social Distancing Policy Java'] = {'No Distancing' : 1,
                                                        'Voluntary Social Distancing - Zonal': 0.75,
                                                        'Voluntary Social Distancing - Provincial' : 0.5,
                                                        'Mandatory Social Distancing - Zonal': 0.25,
                                                        'Mandatory Social Distancing - Provincial' : 0.1}
            
        elif location == 'Querétaro':
            PolicyDictsOut['Closure Policy'] = {'No Closures' : 1,
                                                'Initial Moderate Closures' : 0.7,
                                                'Scenario A: Remission': 0.6,
                                                'Scenario B: Prevention': 0.5,
                                                'Scenario C: Containment': 0.4,
                                                'Starting to Re-Open': 0.3,
                                                'Extraordinary Measures': 0.2} 

        elif location == 'Luanda':
            PolicyDictsOut['Closure Policy'] = {'Pre-Emergency' : 1,
                                    'Emergency State' : 0.6,
                                    'Calamity State': 0.2}
                                                                     
        return PolicyDictsOut
    
    def PolicyDictsInv(self, location):
        """GENERATE INVERSE OF PolicyDicts DICTIONARIES
        
        Args:
            location: the application location of the SD_System
            
        Returns:
            ClosureDictInvOut: Directionary relating numerical values to string titles of closure policies
        """
        
        PolicyDictsInvOut = dict()
        PolicyDictstemp = self.PolicyDicts(location)
        for policy in PolicyDictstemp.keys():
            #dictionary relating numerical closure policy to string value
            # policy_dict = policy
            PolicyDictsInvOut[policy] = dict(map(reversed, PolicyDictstemp[policy].items()))
        
        return PolicyDictsInvOut
    
    
    def CatColor(self):
        """GENERATE RELATIONSHIPS BETWEEN CATEGORY NAME AND VISUALIZATION COLOR
        
        Args:
            N/A
        
        Returns:
            strdict: dictionary relating the names of each category with a numerical value to indicate color
            colormap: matplotlib colormap
            norm: normalization function for the categories
        """
        
        #Generate dictionary of all SD_System objects
        SD_dict = dict(self.__dict__)
        
        #Generate list of all category names
        categorylist = []
        for SDobject in SD_dict:
            categoryname = self.__dict__[SDobject].category
            categorylist.append(categoryname)
                                
        #Sort categories alphabetically and assign a number of each unique value
        categorylist.sort()
        sortedvalues = categorylist
        strdict = {ni: indi for indi, ni in enumerate(set(sortedvalues))}
        values = [strdict[ni] for ni in sortedvalues]
            
        #Calculate the range of numberical values
        minim = min(values)
        maxim = max(values)
        valuerange = maxim - minim
        
        #Generate a colormap and a normalization function for the values
        colormap = cm.get_cmap('tab10', 48)
        norm = colors.Normalize(minim, minim+valuerange)
        
        return strdict, colormap, norm
        
    
    def combos(self, num):
        """CALCULATE NUMBER OF PAIR COMBINATIONS IN A POPULATION
        
        Args:
            num: size of the population
        
        Returns:
            number of pairwise combinations in population of size num
        """
        return (num*(num-1))/2
    
    
    def update_all(self, tstep, tind):
        """UPDATE ALL OF THE OBJECTS IN SD_SYSTEM
        
        Args:
            tstep: the length of time to simulate into the future
            tind: the index of values with which to refer to other SD objects
        
        Returns:
            N/A
        """
        SD_dict = self.__dict__.copy()

        for SDattribute in SD_dict:
            self.__dict__[SDattribute].update(tstep, tind)
            
            
    def retrieve_ob(self, obname):
        """RETRIEVE A SPECIFIC SD_OBJECT IN SD_SYSTEM BASED ON ITS NAME
        
        Args:
            obname: string, the name of the SD object to be retrieved
        
        Returns:
            N/A
        """
        
        SD_dict = self.__dict__.copy()

        for SDattribute in SD_dict:
            if self.__dict__[SDattribute].name == obname:
                output_ob = self.__dict__[SDattribute]
                break
            
        return output_ob
            
    
    # =============================================================================
    # %% 8 - Import Historical Data  
    # ============================================================================= 
    def historical_data(self, fieldname, location, filename):
        """ADD HISTORICAL DATA TO AN SD_OBJECT
        
        Args:
            fieldname: Name of csv column to be retrieved
            location: String naming the application context
            filename: Filepath for the csv holding historical data
        
        Returns:
            N/A
        """
        
        import csv
        
        fieldvalues = []
        
        
        with open(filename) as csv_file:
            csvread = csv.DictReader(csv_file)
            index = 0
            for row in csvread:
                value = row[fieldname]
                if value == '':
                    value = []
                else:
                    if fieldname == 'Closure Policy':
                        value = self.PolicyDicts(location)['Closure Policy'][value]
                    elif fieldname == 'Social Distancing Policy':
                        value = self.PolicyDicts(location)['Social Distancing Policy'][value]
                    #for Indonesia case
                    elif fieldname == 'Social Distancing Policy_java':
                        value = self.PolicyDicts(location)['Social Distancing Policy Java'][value]
                    elif fieldname == 'Social Distancing Policy_sulawesi':
                        value = self.PolicyDicts(location)['Social Distancing Policy Sulawesi'][value]
                    elif fieldname == 'Closure Policy_java':
                        value = self.PolicyDicts(location)['Closure Policy Java'][value]
                    elif fieldname == 'Closure Policy_sulawesi':
                        value = self.PolicyDicts(location)['Closure Policy Sulawesi'][value]                        
                    else:
                        value = float(value)
                fieldvalues.append(value)
                index+=1
               
        return fieldvalues
    

        
# =============================================================================
# %% Main Script  
# =============================================================================         
        
            
if str.__eq__(__name__, '__main__'):
    
    
    SD_Map = SD_System(tuning_flag=0,
                   location='Rio de Janeiro',
                   data_filepath='./Data/Rio de Janeiro/temporal_data.csv')

                   
   
   
   




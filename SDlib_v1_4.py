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
        return self.values[ind]
    
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
    #   1 - Policies & Actions  
    # =============================================================================
    
        self.ClosureP = SD_object('Closure Policy',
                              units = 'unitless',
                              init_value = lambda: self.historical_data('Closure Policy', location, filename),
                              obtype = 'variable',
                              func = lambda tstep, tind: self.ClosureP.value(),
                              category = 'Policies & Actions')
        
        self.SocialDisP = SD_object('Social Distancing Policy',
                              units = 'unitless',
                              init_value = 1,
                              obtype = 'variable',
                              func = lambda tstep, tind: self.SocialDisP.value(),
                              category = 'Policies & Actions')
        
        self.NewOVents = SD_object('New Ventilator Orders',
                    units = 'ventilator',
                    init_value = 0,
                    obtype = 'variable',
                    func = lambda tstep, tind: 0,
                    maxval = lambda: 1000000,
                    minval = lambda: 0,
                    category = 'Policies & Actions')
        
    # =============================================================================
    #   2 - Health Parameters  
    # =============================================================================
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
        
        self.HosL = SD_object('Hospitalization Likelihood',
                          units = 'person/person',
                          init_value = 0.39,
                          obtype = 'variable',
                          func = lambda tstep, tind: self.HosL.value(ind=tind),
                          maxval = lambda: 1,
                          minval = lambda: 0,
                          category = 'Health Parameters')
        
        self.UHML = SD_object('Unhospitalized Mortality Likelihood',
                  units = 'person/person',
                  init_value = 0.3,
                  obtype = 'variable',
                  func = lambda tstep, tind: self.UHML.value(ind=tind),
                  maxval = lambda: 1,
                  minval = lambda: 0,
                  category = 'Health Parameters')
        
        self.UHRL = SD_object('Unhospitalized Recovery Likelihood',
                  units = 'person/person',
                  init_value = 1-self.UHML.value(),
                  obtype = 'variable',
                  func = lambda tstep, tind: 1 - self.UHML.value(ind=tind),
                  maxval = lambda: 1,
                  minval = lambda: 0,
                  category = 'Health Parameters')
        
        self.HRL = SD_object('Hospitalized Recovery Likelihood',
                  units = 'person/person',
                  init_value = 0.9, #lambda: self.HRecovP_func(0, -1),
                  obtype = 'variable',
                  func = lambda tstep, tind: self.HRecovP_func(tstep, tind),
                  maxval = lambda: 1,
                  minval = lambda: 0,
                  category = 'Health Parameters')
        
        self.bHRL = SD_object('Base Hospitalized Recovery Likelihood',
                  units = 'person/person',
                  init_value = 0.9,
                  obtype = 'variable',
                  func = lambda tstep, tind: self.bHRL.value(ind=tind),
                  maxval = lambda: 1,
                  minval = lambda: 0,
                  category = 'Health Parameters')
        
        self.HML = SD_object('Hospitalized Mortality Likelihood',
                  units = 'person/person',
                  init_value = 1-self.HRL.value(),
                  obtype = 'variable',
                  func = lambda tstep, tind: 1 - self.HRL.value(ind=tind),
                  maxval = lambda: 1,
                  minval = lambda: 0,
                  category = 'Health Parameters')
        
        self.RecL = SD_object('Recovery Likelihood',
                  units = 'person/person',
                  init_value = (1-self.HosL.value())*self.UHRL.value() + 
                                self.HosL.value() * self.HRL.value(),
                  obtype = 'variable',
                  func = lambda tstep, tind: (1-self.HosL.value(ind=tind))*self.UHRL.value(ind=tind) + 
                                self.HosL.value(ind=tind) * self.HRL.value(ind=tind),
                  maxval = lambda: 1,
                  minval = lambda: 0,
                  category = 'Health Parameters')
        
        self.MorL = SD_object('Mortality Likelihood',
                  units = 'person/person',
                  init_value = (1-self.HosL.value())*self.UHML.value() + 
                                self.HosL.value() * self.HML.value(),
                  obtype = 'variable',
                  func = lambda tstep, tind: (1-self.HosL.value(ind=tind))*self.UHML.value(ind=tind) + 
                                self.HosL.value(ind=tind) * self.HML.value(ind=tind),
                  maxval = lambda: 1,
                  minval = lambda: 0,
                  category = 'Health Parameters')
        
        self.AvDur = SD_object('Average Illness Duration',
                  units = 'person/person',
                  init_value = 14,
                  obtype = 'variable',
                  func = lambda tstep, tind: self.AvDur.value(ind=tind),
                  maxval = lambda: 300,
                  minval = lambda: 0,
                  category = 'Health Parameters')
        
        self.AvHDur = SD_object('Average Hospitalization Duration',
                  units = 'person/person',
                  init_value = 7,
                  obtype = 'variable',
                  func = lambda tstep, tind: self.AvHDur.value(ind=tind),
                  maxval = lambda: 300,
                  minval = lambda: 0,
                  category = 'Health Parameters')
        
    # =============================================================================
    #   3 - Health Populations  
    # =============================================================================
        self.SPop = SD_object('Susceptible Population',
                        units = 'people',
                        init_value = lambda: self.historical_data('Susceptible Population', location, filename),
                        obtype = 'stock',
                        func = lambda tstep, tind: self.SPop.value(ind=tind) - self.InfectR.value(ind=tind) * tstep,
                        maxval = lambda: 1000000000,
                        minval = lambda: 0,
                        category = 'Health Populations')
           
        self.IPop = SD_object("'True' Unhospitalized Infected Population",
                          units = 'people',
                          init_value = lambda: self.historical_data('True UnHos Infected', location, filename),
                          obtype = 'stock',
                          func = lambda tstep, tind: self.IPop.value(ind=tind) + (self.InfectR.value(ind=tind) - self.UHMR.value(ind=tind) - 
                                                                    self.HosR.value(ind=tind) - self.UHRR.value(ind=tind)) * tstep,
                          maxval = lambda: 100000000,
                          minval = lambda: 0,
                          category = 'Health Populations')
    
        self.Deaths = SD_object('Deaths',
                          units = 'people',
                          init_value = lambda: self.historical_data('total_obito', location, filename),
                          obtype = 'stock',
                          func = lambda tstep, tind: self.Deaths.value(ind=tind) + (self.UHMR.value(ind=tind) + self.HMR.value(ind=tind)) * tstep,
                          maxval = lambda: 100000000,
                          minval = lambda: 0,
                          category = 'Health Populations')
        
        self.HPop = SD_object('Hospitalized Population',
                          units = 'people',
                          init_value = lambda: self.historical_data('Hospitalizados', location, filename),
                          obtype = 'stock',
                          func = lambda tstep, tind: self.HPop.value(ind=tind) + (self.HosR.value(ind=tind) - self.HMR.value(ind=tind) - self.HRR.value(ind=tind)) * tstep,
                          maxval = lambda: 1000000,
                          minval = lambda: 0,
                          category = 'Health Populations')
        
        self.RPop = SD_object('Known Recovered Population',
                          units = 'people',
                          init_value = lambda: self.historical_data('total_recup', location, filename),
                          obtype = 'stock',
                          func = lambda tstep, tind: self.RPop.value(ind=tind) + (self.UHRR.value(ind=tind) + self.HRR.value(ind=tind)) * tstep,
                          maxval = lambda: 100000000,
                          minval = lambda: 0,
                          category = 'Health Populations')
        
        self.mIPop = SD_object("Measured Unhospitalized Infected Population",
                          units = 'people',
                          init_value = lambda: self.historical_data('Unhospitalized Infected', location, filename),
                          obtype = 'stock',
                          func = lambda tstep, tind: self.true_to_measured(self.IPop, 14, 0.25),
                          maxval = lambda: 100000000,
                          minval = lambda: 0,
                          category = 'Health Populations')
        
        self.mTotIPop = SD_object('Measured Total Infected Population',
                          units = 'people',
                          init_value = self.historical_data('Current Infected', location, filename),
                          obtype = 'stock',
                          func = lambda tstep, tind: self.mIPop.value(ind=tind) + self.HPop.value(ind=tind),
                          maxval = lambda: 100000000,
                          minval = lambda: 0,
                          category = 'Health Populations')
        
        self.TotIPop = SD_object("'True' Total Infected Population",
                          units = 'people',
                          init_value = self.IPop.value() + self.HPop.value(),
                          obtype = 'stock',
                          func = lambda tstep, tind: self.IPop.value(ind=tind) + self.HPop.value(ind=tind),
                          maxval = lambda: 100000000,
                          minval = lambda: 0,
                          category = 'Health Populations')
        
    # =============================================================================
    #   4 - Health Flows  
    # =============================================================================
    
        self.InfectR = SD_object("'True' Infection Rate",
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
#                            init_value = 1,
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
        
    
    # =============================================================================
    #   5 - Equipment Supplies  
    # =============================================================================
        self.HBeds = SD_object('Hospital Bed Capacity',
                  units = 'person',
                  init_value = 2000,
                  obtype = 'variable',
                  func = lambda tstep, tind: self.HBeds.value(ind=tind),
                  maxval = lambda: 1000000,
                  minval = lambda: 0,
                  category = 'Equipment Supplies')
        
        self.Vents = SD_object('Available Ventilators',
                          units = 'ventilator',
                          init_value = lambda: self.historical_data('Ventilators', location, filename),
                          obtype = 'stock',
                          func = lambda tstep, tind: self.Vents.value(ind=tind) + self.VentAqRate.value(ind=tind) * tstep,
                          maxval = lambda: 1000000,
                          minval = lambda: 0,
                          category = 'Equipment Supplies')
        
        self.OVents = SD_object('Ordered Ventilators',
                          units = 'ventilator',
                          init_value = 0,
                          obtype = 'stock',
                          func = lambda tstep, tind: self.OVents.value(ind=tind) + self.NewOVents.value(ind=tind) 
                                                      - (self.VentAqRate.value(ind=tind) * tstep),
                          maxval = lambda: 1000000,
                          minval = lambda: 0,
                          category = 'Equipment Supplies')
        
        if location == 'Chile':
            
            self.PCR = SD_object('Daily PCR Tests',
                  units = 'tests',
                  init_value = lambda: self.historical_data('PCR Tests', location, filename),
                  obtype = 'stock',
                  func = lambda tstep, tind: self.PCR.value(ind=tind),
                  maxval = lambda: 1000000,
                  minval = lambda: 0,
                  category = 'Equipment Supplies')
        
    # =============================================================================
    #   6 - Equipment Parameters 
    # =============================================================================
        self.VWTP = SD_object('Ventilator Willingness to Pay',
                  units = 'dollar/ventilator',
                  init_value = 25000,
                  obtype = 'variable',
                  func = lambda tstep, tind: self.VWTP.value(ind=tind),
                  maxval = lambda: 1000000,
                  minval = lambda: 0,
                  category = 'Equipment Parameters')
        
        self.VDur = SD_object('Default VentilatorDelivery Duration',
                  units = 'days',
                  init_value = 30,
                  obtype = 'variable',
                  func = lambda tstep, tind: self.VDur.value(ind=tind),
                  maxval = lambda: 365,
                  minval = lambda: 0,
                  category = 'Equipment Parameters')
        
        self.VentAqRate = SD_object('Ventilator Acquisition Rate',
                                units = 'ventilator/day',
                                init_value = 0,
                                obtype = 'flow',
                                func = lambda tstep, tind: self.OVents.value(ind=tind) / self.VDur.value(ind=tind) 
                                                            * (3 * (1 - math.exp(-math.log(3/2) / self.VWTP.values[0] * self.VWTP.value(ind=tind)))),
                                maxval = lambda: 1000000,
                                minval = lambda: 0,
                                category = 'Equipment Parameters')
        

            
        
    # =============================================================================
    #   7 - Environment 
    # =============================================================================
        
        if location == 'Rio de Janeiro':
        
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
        
        
    # =============================================================================
    #   8 - Economic 
    # =============================================================================
        

        if location == 'Rio de Janeiro':
            
            self.RioEmployment = SD_object('Rio de Janeiro Unemployment Rate',
                              units = 'percent',
                              init_value = lambda: self.historical_data('Rio Unemployment Rate', location, filename),
                              obtype = 'stock',
                              func = lambda tstep, tind: self.RioEmployment.value(ind=tind) + self.RioEmploymentR.value(ind=tind) * tstep,
                              maxval = lambda: 1,
                              minval = lambda: 0,
                              category = 'Economic')
            
    
            
            self.RioEmploymentR = SD_object('Rio de Janeiro Unemployment Rate of Change',
                                units = 'percent',
                                init_value = 0,
                                obtype = 'flow',
                                func = lambda tstep, tind: self.RioEmploymentR_update(tstep, tind),
                                maxval = lambda: 0.05,
                                minval = lambda: -0.05,
                                category = 'Economic'
                                )
            
            self.BraEmployment = SD_object('Brazil Unemployment Rate',
                              units = 'percent',
                              init_value = lambda: self.historical_data('Brazil Unemployment Rate', location, filename),
                              obtype = 'stock',
                              func = lambda tstep, tind: self.BraEmployment.value(ind=tind) + self.BraEmploymentR.value(ind=tind) * tstep,
                              maxval = lambda: 1,
                              minval = lambda: 0,
                              category = 'Economic')
            
    
            
            self.BraEmploymentR = SD_object('Brazil Unemployment Rate of Change',
                                units = 'percent',
                                init_value = 0,
                                obtype = 'flow',
                                func = lambda tstep, tind: self.BraEmploymentR_update(tstep, tind),
                                maxval = lambda: 0.05,
                                minval = lambda: -0.05,
                                category = 'Economic'
                                )
            
        elif location == 'Chile':
            
                        self.AirPass = SD_object('Daily Flight Passengers',
                              units = 'people',
                              init_value = lambda: self.historical_data('AirPassengers', location, filename),
                              obtype = 'stock',
                              func = lambda tstep, tind: self.AirPass.value(ind=tind),
                              maxval = lambda: 10000000,
                              minval = lambda: 0,
                              category = 'Economic')

        elif location == 'Indonesia':
            
                        self.AirPass = SD_object('Gross Domestic Product',
                              units = 'Rp Million',
                              init_value = lambda: self.historical_data('GDP', location, filename),
                              obtype = 'stock',
                              func = lambda tstep, tind: self.AirPass.value(ind=tind),
                              maxval = lambda: 10000000,
                              minval = lambda: 0,
                              category = 'Economic')                              
            
        
    # =============================================================================
    #   9 - Adjustments for Tuning  
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
    #   10 - Multi-line Update Functions
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
        
        #Adjust recovery rate based on relative hospitalized population and available ventilators
        if self.HPop.value(ind=tind) > 5 * self.Vents.value(ind=tind):
            rprob = baseprob * 0.7
        if self.HPop.value(ind=tind) > 5 * self.Vents.value(ind=tind) and self.HPop.value(ind=tind) > self.HBeds.value(ind=tind):
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
        return EmpR
    
    
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
        return EmpR
       
        
    # =============================================================================
    #   11 - Auxillary Functions 
    # =============================================================================  
        
    def ClosureDict(self, location):
        """GENERATE DICTIONARY DEFINING THE CLOSURE POLICY OPTIONS
        
        Args:
            location: the application location of the SD_System
            
        Returns:
            ClosureDictOut: Directionary relating string titles of closure policies to 
                numerical values generally according with effectiveness
        """
        #dictionary relating string closure policy to numerical value
        if location == 'Rio de Janeiro':
            ClosureDictOut = {'No Closures' : 1,
                            'Fase 6' : 0.9,
                            'Fase 5': 0.8,
                            'Fase 4' : 0.7,
                            'Fase 3B': 0.6,
                            'Fase 3A': 0.5,
                            'Fase 2': 0.4,
                            'Fase 1': 0.3,
                            'Lockdown': 0.2}
        elif location == 'Chile':
             ClosureDictOut = {'No Closures' : 1,
                            'Paso 5': 0.8,
                            'Paso 4' : 0.7,
                            'Paso 3': 0.5,
                            'Paso 2': 0.4,
                            'Paso 1': 0.3,
                            'Lockdown': 0.2}
        elif location == 'Indonesia':
            ClosureDictOut = {'No Closures' : 1,
                            'Placeholder 5': 0.8,
                            'Placeholder 4' : 0.7,
                            'Placeholder 3': 0.5,
                            'Placeholder 2': 0.4,
                            'Placeholder 1': 0.3,
                            'Lockdown': 0.2}
        
        
        return ClosureDictOut
    
    
    def ClosureDictInv(self, location):
        """GENERATE INVERSE OF ClosureDict DICTIONARY
        
        Args:
            location: the application location of the SD_System
            
        Returns:
            ClosureDictInvOut: Directionary relating numerical values to string titles of closure policies
        """
        #dictionary relating numerical closure policy to string value
        cldict = self.ClosureDict(location)
        ClosureDictInvOut = dict(map(reversed, cldict.items()))
        return ClosureDictInvOut

        
    def SocialDisDict(self):
        """GENERATE DICTIONARY DEFINING THE SOCIAL DISTANCING POLICY OPTIONS
        
        Args:
            N/A
            
        Returns:
            SocialDisDictOut: Directionary relating string titles of social distancing policies 
                to numerical values generally according with effectiveness
        """
        
        #dictionary relating string social distancing policy to numerical value
        SocialDisDictOut = {'No Distancing' : 1,
                        'Voluntary Social Distancing' : 0.6,
                        'Mandatory Social Distancing' : 0.1}
        return SocialDisDictOut
    
    
    def SocialDisDictInv(self):
        """GENERATE INVERSE OF SocialDisDict DICTIONARY
        
        Args:
            N/A
            
        Returns:
            SocialDisDictInvOut: Directionary relating numerical values to string titles of closure policies
        """
        
        #dictionary relating numerical social distancing policy to string value
        sddict = self.SocialDisDict()
        SocialDisDictInvOut = dict(map(reversed, sddict.items()))
        return SocialDisDictInvOut
    
    
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
    #   13 - Import Historical Data  
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
                        value = self.ClosureDict(location)[value]
                    else:
                        value = float(value)
                fieldvalues.append(value)
                index+=1
               
        return fieldvalues
    

        
# =============================================================================
#   Main Script  
# =============================================================================         
        
            
if str.__eq__(__name__, '__main__'):
    

#    SD_Map = SD_System(tuning_flag=0,
#                       location='Chile',
#                       data_filepath='./Data/Chile/Chile_Data.csv')
    
    SD_Map = SD_System(tuning_flag=0,
                       location='Rio de Janeiro',
                       data_filepath='./Data/Brazil/Brazil_Data.csv')
       
       




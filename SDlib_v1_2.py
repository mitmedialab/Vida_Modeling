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
            self.values.append(kwargs.pop('init_value'))
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
        
        # self.update = lambda: print(SusceptiblePop.value(), 'and', InfectR.value(), 'and', time())
        
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
         
        


class SD_System: 
    def __init__(self, **kwargs):
        
        """INITIATE SD_SYSTEM CLASS
        This class specifies a specific system dynamics causal map. It is constituted of numerous SD_object's of various categories
        
        Args:
            N/A
        
        Returns:
            N/A
        """
   
    # =============================================================================
    #   Policies & Actions  
    # =============================================================================
    
        self.ClosureP = SD_object('Closure Policy',
                              units = 'unitless',
                              init_value = 1,
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
    #   Health Parameters  
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
                          init_value = 0.1,
                          obtype = 'variable',
                          func = lambda tstep, tind: self.HosL.value(ind=tind),
                          maxval = lambda: 1,
                          minval = lambda: 0,
                          category = 'Health Parameters')
        
        self.UHML = SD_object('Unhospitalized Mortality Likelihood',
                  units = 'person/person',
                  init_value = 0.01,
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
                  init_value = 0.94, #lambda: self.HRecovP_func(0, -1),
                  obtype = 'variable',
                  func = lambda tstep, tind: self.HRecovP_func(tstep, tind),
                  maxval = lambda: 1,
                  minval = lambda: 0,
                  category = 'Health Parameters')
        
        self.bHRL = SD_object('Base Hospitalized Recovery Likelihood',
                  units = 'person/person',
                  init_value = 0.94,
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
    #   Health Populations  
    # =============================================================================
        self.SPop = SD_object('Susceptible Population',
                        units = 'people',
                        init_value = 999995,
                        obtype = 'stock',
                        func = lambda tstep, tind: self.SPop.value(ind=tind) - self.InfectR.value(ind=tind) * tstep,
                        maxval = lambda: 1000000,
                        minval = lambda: 0,
                        category = 'Health Populations')
           
        self.IPop = SD_object("'True' Unhospitalized Infected Population",
                          units = 'people',
                          init_value = 5,
                          obtype = 'stock',
                          func = lambda tstep, tind: self.IPop.value(ind=tind) + (self.InfectR.value(ind=tind) - self.UHMR.value(ind=tind) - 
                                                                    self.HosR.value(ind=tind) - self.UHRR.value(ind=tind)) * tstep,
                          maxval = lambda: 1000000,
                          minval = lambda: 0,
                          category = 'Health Populations')
    
        self.Deaths = SD_object('Deaths',
                          units = 'people',
                          init_value = 0,
                          obtype = 'stock',
                          func = lambda tstep, tind: self.Deaths.value(ind=tind) + (self.UHMR.value(ind=tind) + self.HMR.value(ind=tind)) * tstep,
                          maxval = lambda: 1000000,
                          minval = lambda: 0,
                          category = 'Health Populations')
        
        self.HPop = SD_object('Hospitalized Population',
                          units = 'people',
                          init_value = 0,
                          obtype = 'stock',
                          func = lambda tstep, tind: self.HPop.value(ind=tind) + (self.HosR.value(ind=tind) - self.HMR.value(ind=tind) - self.HRR.value(ind=tind)) * tstep,
                          maxval = lambda: 1000000,
                          minval = lambda: 0,
                          category = 'Health Populations')
        
        self.RPop = SD_object('Recovered Population',
                          units = 'people',
                          init_value = 0,
                          obtype = 'stock',
                          func = lambda tstep, tind: self.RPop.value(ind=tind) + (self.UHRR.value(ind=tind) + self.HRR.value(ind=tind)) * tstep,
                          maxval = lambda: 1000000,
                          minval = lambda: 0,
                          category = 'Health Populations')
        
        self.mIPop = SD_object("Measured Unhospitalized Infected Population",
                          units = 'people',
                          init_value = 0,
                          obtype = 'stock',
                          func = lambda tstep, tind: self.true_to_measured(self.IPop, 14, 0.25),
                          maxval = lambda: 1000000,
                          minval = lambda: 0,
                          category = 'Health Populations')
        
        self.mTotIPop = SD_object('Measured Total Infected Population',
                          units = 'people',
                          init_value = self.mIPop.value() + self.HPop.value(),
                          obtype = 'stock',
                          func = lambda tstep, tind: self.mIPop.value(ind=tind) + self.HPop.value(ind=tind),
                          maxval = lambda: 1000000,
                          minval = lambda: 0,
                          category = 'Health Populations')
        
        self.TotIPop = SD_object("'True' Total Infected Population",
                          units = 'people',
                          init_value = self.IPop.value() + self.HPop.value(),
                          obtype = 'stock',
                          func = lambda tstep, tind: self.IPop.value(ind=tind) + self.HPop.value(ind=tind),
                          maxval = lambda: 1000000,
                          minval = lambda: 0,
                          category = 'Health Populations')
        
    # =============================================================================
    #   Health Flows  
    # =============================================================================
    
        self.InfectR = SD_object("'True' Infection Rate",
                            units = 'people/day',
                            init_value = (self.combos(self.SPop.value() + self.IPop.value()) - self.combos(self.SPop.value()) - self.combos(self.IPop.value())) / 
                                            self.combos(self.SPop.value() + self.IPop.value()) * self.ContactR.value() * (self.SPop.value() + self.IPop.value()) * self.Infectivity.value(),
                            obtype = 'flow',
                            func = lambda tstep, tind: (self.combos(self.SPop.value(ind=tind) + self.IPop.value(ind=tind)) - self.combos(self.SPop.value(ind=tind)) - self.combos(self.IPop.value(ind=tind))) / 
                                                self.combos(self.SPop.value(ind=tind) + self.IPop.value(ind=tind)) * self.ContactR.value(ind=tind) * (self.SPop.value(ind=tind) + self.IPop.value(ind=tind)) * self.Infectivity.value(ind=tind),
                            maxval = lambda: self.SPop.value(),
                            minval = lambda: 0,
                            category = 'Health Flows'
                            )
        
        self.mInfectR = SD_object("Measured Infection Rate",
                            units = 'people/day',
                            init_value = 0,
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
                            init_value = self.HosL.value() * self.IPop.value() / self.AvDur.value(),
                            obtype = 'flow',
                            func = lambda tstep, tind: self.HosL.value(ind=tind) * self.IPop.value(ind=tind) / self.AvDur.value(ind=tind),
                            maxval = lambda: self.IPop.value(),
                            minval = lambda: 0,
                            category = 'Health Flows'
                            )
        
    
    # =============================================================================
    #   Equipment Supplies  
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
                          init_value = 20,
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
    # =============================================================================
    #   Equipment Parameters 
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
                                category = 'Equipment Parameters'
                                )
    # =============================================================================
    #   Environment 
    # =============================================================================
        
        self.EmissionsR = SD_object('Daily Emissions Rate',
                  units = 'Metric Tons of Greenhouse Gases ',
                  init_value = 20000,
                  obtype = 'variable',
                  func = lambda tstep, tind: self.EmissionsR_update(tstep, tind),
                  maxval = lambda: 100000,
                  minval = lambda: 0,
                  category = 'Environment')
        
    # =============================================================================
    #   Economic 
    # =============================================================================
        
        self.GDP = SD_object('GDP (Relative to 2019)',
                          units = 'Percent Change from 2019',
                          init_value = 3,
                          obtype = 'stock',
                          func = lambda tstep, tind: self.GDP.value(ind=tind) + self.GDPR.value(ind=tind) * tstep,
                          maxval = lambda: 200,
                          minval = lambda: -100,
                          category = 'Economic')
        
        self.Employment = SD_object('Employment Rate',
                          units = 'percent',
                          init_value = 0.93,
                          obtype = 'stock',
                          func = lambda tstep, tind: self.Employment.value(ind=tind) + self.EmploymentR.value(ind=tind) * tstep,
                          maxval = lambda: 1,
                          minval = lambda: 0,
                          category = 'Economic')
        
        self.GDPR = SD_object('GDP Rate of Change',
                            units = 'percent/day',
                            init_value = 0,
                            obtype = 'flow',
                            func = lambda tstep, tind: self.GDPR_update(tstep, tind),
                            maxval = lambda: 0.2,
                            minval = lambda: -0.2,
                            category = 'Economic'
                            )
        
        self.EmploymentR = SD_object('Employment Rate of Change',
                            units = 'ventilator',
                            init_value = 0,
                            obtype = 'flow',
                            func = lambda tstep, tind: self.EmploymentR_update(tstep, tind),
                            maxval = lambda: 0.05,
                            minval = lambda: -0.05,
                            category = 'Economic'
                            )
   
    
    
    # =============================================================================
    #   Multi-line Update Functions
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
            measuredValue = np.random.normal(trueValue, error_std*trueValue, 1)
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
    
    def EmissionsR_update(self, tstep, tind):
        """EMISSIONS RATE UPDATE FUNCTION
        
        Args:
            tstep: the length of time to simulate into the future
            tind: the index of values with which to refer to other SD objects
        
        Returns:
            N/A
        """
        base_emissions = self.EmissionsR.values[0]
        emissions = base_emissions
        ClosureVal = self.ClosureDictInv()[self.ClosureP.value(ind=tind)]
        
        if ClosureVal == 'Large Events & Confined Spaces Closed':
            emissions = base_emissions*0.95
        elif ClosureVal == 'All Non Essential Businesses Closed':
            emissions = base_emissions*0.7
        elif ClosureVal == 'All In-Person Businesses Closed':
            emissions = base_emissions*0.6  
            
        return emissions
    
    def GDPR_update(self, tstep, tind):
        """GDP RATE OF CHANGE UPDATE FUNCTION
        
        Args:
            tstep: the length of time to simulate into the future
            tind: the index of values with which to refer to other SD objects
        
        Returns:
            N/A
        """
        base_GDPR = np.random.normal(0, 0.001, 1)[0]
        GDPR = base_GDPR
        ClosureVal = self.ClosureDictInv()[self.ClosureP.value(ind=tind)]
    
        if ClosureVal == 'Large Events & Confined Spaces Closed':
            GDPR = np.random.normal(-0.001, 0.0015, 1)[0]
        elif ClosureVal == 'All Non Essential Businesses Closed':
            GDPR = np.random.normal(-0.008, 0.005, 1)[0]
        elif ClosureVal == 'All In-Person Businesses Closed':
            GDPR = np.random.normal(-0.009, 0.006, 1) [0]
            
        GDPR = GDPR - self.Deaths.value(ind=tind)/1000000

        return GDPR
    
    def EmploymentR_update(self, tstep, tind):
        """EMPLOYMENT RATE RATE OF CHANGE UPDATE
        
        Args:
            tstep: the length of time to simulate into the future
            tind: the index of values with which to refer to other SD objects
        
        Returns:
            N/A
        """
        if self.Employment.value(ind=tind) < self.Employment.values[0]:
            base_EmpR = np.random.normal(0.0005, 0.0025, 1)
        else:
            base_EmpR = np.random.normal(0, 0.0025, 1)
        EmpR = base_EmpR
        ClosureVal = self.ClosureDictInv()[self.ClosureP.value(ind=tind)]
        
        if ClosureVal == 'Large Events & Confined Spaces Closed':
            EmpR = np.random.normal(-0.0005, 0.0003, 1)
        elif ClosureVal == 'All Non Essential Businesses Closed':
            EmpR = np.random.normal(-0.001, 0.005, 1)
        elif ClosureVal == 'All In-Person Businesses Closed':
            EmpR = np.random.normal(-0.0015, 0.0055, 1) 
            
        EmpR = EmpR - self.TotIPop.value(ind=tind)/20000000
        return EmpR
       
        
    # =============================================================================
    #   Auxillary Functions 
    # =============================================================================  
        
    def ClosureDict(self):
        #dictionary relating string closure policy to numerical value
        ClosureDictf = {'No Closures' : 1,
                        'Large Events & Confined Spaces Closed' : 0.7,
                        'All Non Essential Businesses Closed': 0.6,
                        'All In-Person Businesses Closed' : 0.1}
        return ClosureDictf
    
    def ClosureDictInv(self):
        #dictionary relating numerical closure policy to string value
        cldict = self.ClosureDict()
        ClosureDictInvf = dict(map(reversed, cldict.items()))
        return ClosureDictInvf

        
    def SocialDisDict(self):
        #dictionary relating string social distancing policy to numerical value
        SocialDisDictf = {'No Distancing' : 1,
                        'Voluntary Social Distancing' : 0.6,
                        'Mandatory Social Distancing' : 0.1}
        return SocialDisDictf
    
    def SocialDisDictInv(self):
        #dictionary relating numerical social distancing policy to string value
        sddict = self.SocialDisDict()
        SocialDisDictInvf = dict(map(reversed, sddict.items()))
        return SocialDisDictInvf
    
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
        SD_dict = self.__dict__
        
        #Generate list of all category names
        categorylist = []
        for SDobject in SD_dict:
            categoryname = SD_dict[SDobject].category
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
        
        for SDattribute in self.__dict__:
            self.__dict__[SDattribute].update(tstep, tind)
            
    def retrieve_ob(self, obname):
        """RETRIEVE A SPECIFIC SD_OBJECT IN SD_SYSTEM BASED ON ITS NAME
        
        Args:
            obname: string, the name of the SD object to be retrieved
        
        Returns:
            N/A
        """
        
        for SDattribute in self.__dict__:
            if self.__dict__[SDattribute].name == obname:
                output_ob = self.__dict__[SDattribute]
                break
        return output_ob
            
   

        
        
            
if str.__eq__(__name__, '__main__'):
    

    SD_Map = SD_System()
       




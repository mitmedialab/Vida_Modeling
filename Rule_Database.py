#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import SDlib_v1_4 as SDlib 



class Conditional_Database:
    
    """
    Define the Catalog of Decision Rules     
    
    Each decision rules follows a pattern, as follows
            
            Args:
                rule_intput: class holding all of the relevant input values for the decision conditions
    
            Conditional: Condition identifying when the rule is triggered
            
            Policy Effect: Policy changes that occur when the conditional is met
        
            Returns:
                output: a flag indicating if the conditional has been met (0=no, 1=yes)
    """
    def __init__(self, UI):
         
        # Import Relevant Attributes #
        self.SD_Map = UI.SD_Map
        self.PolicyDicts = UI.PolicyDicts
        
    
    # =============================================================================
    # %% RIO DE JANEIRO RULES            
    # =============================================================================
    
    def Br_Rule1func(self, policy_input):
        output = 0
        if self.SD_Map.mTotIPop.value() >= 20 and policy_input['Closure Policy'] == 'No Closures' and policy_input['Social Distancing Policy'] == 'No Distancing':
            # print('Rule 1 Triggered')
            self.SD_Map.ClosureP.values[-1] = self.PolicyDicts['Closure Policy']['Fase 3A']
            self.SD_Map.SocialDisP.values[-1] = self.PolicyDicts['Social Distancing Policy']['Voluntary Social Distancing']
            output = 1
        return output
    def Br_Rule2func(self, policy_input):
        output = 0
        if self.SD_Map.mTotIPop.value() >= 100 and (policy_input['Closure Policy'] in ['No Closures', 'Conservative', 'Fase 6b', 'Fase 6a', 'Fase 5', 'Fase 4', 'Fase 3b', 'Fase 3a']):
            # print('Rule 2 Triggered')
            self.SD_Map.ClosureP.values[-1] = self.PolicyDicts['Closure Policy']['Fase 1'] 
            output = 1
        return output
    def Br_Rule3func(self, policy_input):
        output = 0
        if self.SD_Map.mInfectR.value() >= 100 and (policy_input['Closure Policy'] in ['No Closures', 'Conservative', 'Fase 6b', 'Fase 6a', 'Fase 5', 'Fase 4', 'Fase 3b', 'Fase 3a', 'Fase 2', 'Fase 1' ]):
            # print('Rule 3 Triggered')
            self.SD_Map.ClosureP.values[-1] = self.PolicyDicts['Closure Policy']['Initial Closures']
            self.SD_Map.SocialDisP.values[-1] = self.PolicyDicts['Social Distancing Policy']['Mandatory Social Distancing'] 
            output = 1
        return output
    def Br_Rule4func(self,policy_input):
        output = 0
        if self.SD_Map.mTotIPop.value() <= 500 and (policy_input['Closure Policy'] in ['Fase 2', 'Fase 1', 'Initial Closures' ]):
            # print('Rule 4 Triggered')
            self.SD_Map.ClosureP.values[-1] = self.PolicyDicts['Closure Policy']['Fase 3a']
            output = 1
        return output
    def Br_Rule5func(self, policy_input):
        output = 0
        if self.SD_Map.mTotIPop.value() <= 500 and policy_input['Social Distancing Policy'] == 'Mandatory Social Distancing':
            # print('Rule 5 Triggered')
            self.SD_Map.SocialDisP.values[-1] = self.PolicyDicts['Social Distancing Policy']['Voluntary Social Distancing']   
            output = 1
        return output
    # def Br_Rule6func(self, policy_input):
    #     output = 0
    #     if self.SD_Map.HPop.value() > 2.5 * self.SD_Map.Vents.value():
    #         # print('Rule 6 Triggered')
    #         self.SD_Map.NewOVents.values[-1] = 5
    #         output = 1
    #     return output
    # def Br_Rule7func(self, policy_input):
    #     output = 0
    #     if self.SD_Map.HPop.value() > 7 * self.SD_Map.Vents.value():
    #         # print('Rule 7 Triggered')
    #         self.SD_Map.VWTP.values[-1] = 50000
    #         output = 1
    #     return output
    

    
    # =============================================================================
    # %% INDONESIA RULES            
    # =============================================================================
    
    #Nationwide
    # transition from nothing to relaxed restrictions
    def In_Rule1func(self, policy_input):
        output = 0
        if self.SD_Map.mIPop.value() >= 20 and policy_input['Closure Policy'] == 'No Closures' and policy_input['Social Distancing Policy'] == 'No Distancing':
            # print('Rule 1 Triggered')
            self.SD_Map.ClosureP.values[-1] = self.PolicyDicts['Closure Policy']['Relaxed Social Restrictions']
            self.SD_Map.SocialDisP.values[-1] = self.PolicyDicts['Social Distancing Policy']['Voluntary Social Distancing']
            output = 1
        return output
    # transition from nothing or relaxed restrictions to high restrictions
    def In_Rule2func(self, policy_input):
        output = 0
        if self.SD_Map.mIPop.value() >= 5000 and (policy_input['Closure Policy'] in ['No Closures', 'Relaxed Social Restrictions']):
            # print('Rule 2 Triggered')
            self.SD_Map.ClosureP.values[-1] = self.PolicyDicts['Closure Policy']['High Social Restrictions'] 
            self.SD_Map.SocialDisP.values[-1] = self.PolicyDicts['Social Distancing Policy']['Mandatory Social Distancing']            
            output = 1
        return output
    # Relax social restrictions
    def In_Rule3func(self,policy_input):
        output = 0
        if self.SD_Map.mIPop.value() <= 2500 and (policy_input['Closure Policy'] in ['High Social Restrictions']):
            # print('Rule 4 Triggered')
            self.SD_Map.ClosureP.values[-1] = self.PolicyDicts['Closure Policy']['Relaxed Social Restrictions']
            output = 1
        return output
        #test
    # Relax social distancing    
    def In_Rule4func(self, policy_input):
        output = 0
        if self.SD_Map.mIPop.value() <= 2500 and policy_input['Social Distancing Policy'] == 'Mandatory Social Distancing':
            # print('Rule 5 Triggered')
            self.SD_Map.SocialDisP.values[-1] = self.PolicyDicts['Social Distancing Policy']['Voluntary Social Distancing']   
            output = 1
        return output 
    #Island specific
    # transition from nothing to relaxed restrictions
    def In_Rule1func_j(self, policy_input):
        output = 0
        if self.SD_Map.mIPop_j.value() >= 20 and policy_input['Closure Policy Java'] == 'No Closures' and policy_input['Social Distancing Policy Java'] == 'No Distancing':
            # print('Rule 1 Triggered')
            self.SD_Map.ClosureP_j.values[-1] = self.PolicyDicts['Closure Policy Java']['Relaxed Social Restrictions - Zonal']
            self.SD_Map.SocialDisP_j.values[-1] = self.PolicyDicts['Social Distancing Policy Java']['Voluntary Social Distancing - Zonal']
            output = 1
        return output
    
    def In_Rule1func_s(self, policy_input):
        output = 0
        if self.SD_Map.mIPop_s.value() >= 20 and policy_input['Closure Policy Sulawesi'] == 'No Closures' and policy_input['Social Distancing Policy Sulawesi'] == 'No Distancing':
            # print('Rule 1 Triggered')
            self.SD_Map.ClosureP_s.values[-1] = self.PolicyDicts['Closure Policy Sulawesi']['Relaxed Social Restrictions - Zonal']
            self.SD_Map.SocialDisP_s.values[-1] = self.PolicyDicts['Social Distancing Policy Sulawesi']['Voluntary Social Distancing - Zonal']
            output = 1
        return output
    
    # transition from nothing or relaxed restrictions to high restrictions
    def In_Rule2func_j(self, policy_input):
        output = 0
        if self.SD_Map.mIPop_j.value() >= 1000 and (policy_input['Closure Policy Java'] in ['No Closures', 'Relaxed Social Restrictions - Zonal', 'Relaxed Social Restrictions - Provincial']):
            # print('Rule 2 Triggered')
            self.SD_Map.ClosureP_j.values[-1] = self.PolicyDicts['Closure Policy Java']['High Social Restrictions - Zonal'] 
            self.SD_Map.SocialDisP_j.values[-1] = self.PolicyDicts['Social Distancing Policy Java']['Mandatory Social Distancing - Zonal']            
            output = 1
        return output
    
    def In_Rule2func_s(self, policy_input):
        output = 0
        if self.SD_Map.mIPop_s.value() >= 500 and (policy_input['Closure Policy Sulawesi'] in ['No Closures', 'Relaxed Social Restrictions - Zonal', 'Relaxed Social Restrictions - Provincial']):
            # print('Rule 2 Triggered')
            self.SD_Map.ClosureP_s.values[-1] = self.PolicyDicts['Closure Policy Sulawesi']['High Social Restrictions - Zonal'] 
            self.SD_Map.SocialDisP_s.values[-1] = self.PolicyDicts['Social Distancing Policy Sulawesi']['Mandatory Social Distancing - Zonal']            
            output = 1
        return output
    # Relax social restrictions
    def In_Rule3func_j(self,policy_input):
        output = 0
        if self.SD_Map.mIPop_j.value() <= 500 and (policy_input['Closure Policy Java'] in ['High Social Restrictions - Zonal', 'High Social Restrictions - Provincial']):
            # print('Rule 4 Triggered')
            self.SD_Map.ClosureP_j.values[-1] = self.PolicyDicts['Closure Policy Java']['Relaxed Social Restrictions - Zonal']
            output = 1
        return output
    
    def In_Rule3func_s(self,policy_input):
        output = 0
        if self.SD_Map.mIPop_s.value() <= 250 and (policy_input['Closure Policy Sulawesi'] in ['High Social Restrictions - Zonal', 'High Social Restrictions - Provincial']):
            # print('Rule 4 Triggered')
            self.SD_Map.ClosureP_s.values[-1] = self.PolicyDicts['Closure Policy Sulawesi']['Relaxed Social Restrictions - Zonal']
            output = 1
        return output   
    
    # Relax social distancing    
    def In_Rule4func_j(self, policy_input):
        output = 0
        if self.SD_Map.mIPop_j.value() <= 500 and (policy_input['Social Distancing Policy Java'] in ['Mandatory Social Distancing - Provincial', 'Mandatory Social Distancing - Zonal']):
            # print('Rule 5 Triggered')
            self.SD_Map.SocialDisP_j.values[-1] = self.PolicyDicts['Social Distancing Policy Java']['Voluntary Social Distancing - Zonal']   
            output = 1
        return output 
    
    def In_Rule4func_s(self, policy_input):
        output = 0
        if self.SD_Map.mIPop_s.value() <= 250 and (policy_input['Social Distancing Policy Sulawesi'] in ['Mandatory Social Distancing - Provincial', 'Mandatory Social Distancing - Zonal']):
            # print('Rule 5 Triggered')
            self.SD_Map.SocialDisP_s.values[-1] = self.PolicyDicts['Social Distancing Policy Sulawesi']['Voluntary Social Distancing - Zonal']   
            output = 1
        return output         
    
    # =============================================================================
    # %% CHILE RULES            
    # =============================================================================
    
    def Ch_Rule1func(self, policy_input):
        output = 0
        if self.SD_Map.mTotIPop.value() >= 20 and policy_input['Closure Policy'] == 'Paso 5' and policy_input['Curfew Policy'] == 'No Curfew':
            # print('Rule 1 Triggered')
            self.SD_Map.ClosureP.values[-1] = self.PolicyDicts['Closure Policy']['Paso 3']
            self.SD_Map.SocialDisP.values[-1] = self.PolicyDicts['Curfew Policy']['Unenforced Curfew']
            output = 1
        return output
    def Ch_Rule2func(self, policy_input):
        output = 0
        if self.SD_Map.mTotIPop.value() >= 100 and (policy_input['Closure Policy'] in ['Paso 5', 'Paso 4']):
            # print('Rule 2 Triggered')
            self.SD_Map.ClosureP.values[-1] = self.PolicyDicts['Closure Policy']['Paso 3'] 
            output = 1
        return output
    def Ch_Rule3func(self, policy_input):
        output = 0
        if self.SD_Map.mInfectR.value() >= 100 and (policy_input['Closure Policy'] in ['Paso 5', 'Paso 4', 'Paso 3', 'Paso 2']):
            # print('Rule 3 Triggered')
            self.SD_Map.ClosureP.values[-1] = self.PolicyDicts['Closure Policy']['Paso 1']
            self.SD_Map.SocialDisP.values[-1] = self.PolicyDicts['Curfew Policy']['Enforced Curfew'] 
            output = 1
        return output
    def Ch_Rule4func(self,policy_input):
        output = 0
        if self.SD_Map.mTotIPop.value() <= 500 and (policy_input['Closure Policy'] in ['Paso 2', 'Paso 1']):
            # print('Rule 4 Triggered')
            self.SD_Map.ClosureP.values[-1] = self.PolicyDicts['Closure Policy']['Paso 3']
            output = 1
        return output
    def Ch_Rule5func(self, policy_input):
        output = 0
        if self.SD_Map.mTotIPop.value() <= 500 and policy_input['Curfew Policy'] == 'Enforced Curfew':
            # print('Rule 5 Triggered')
            self.SD_Map.SocialDisP.values[-1] = self.PolicyDicts['Curfew Policy']['Unenforced Curfew']   
            output = 1
        return output
    
    def Ch_Rule6func(self, policy_input):
        output = 0
        if self.SD_Map.HPop.value() > 2.5 * self.SD_Map.Vents.value():
            # print('Rule 6 Triggered')
            self.SD_Map.NewOVents.values[-1] = 5
            output = 1
        return output
    def Ch_Rule7func(self, policy_input):
        output = 0
        if self.SD_Map.HPop.value() > 7 * self.SD_Map.Vents.value():
            # print('Rule 7 Triggered')
            self.SD_Map.VWTP.values[-1] = 50000
            output = 1
        return output
    
    # =============================================================================
    # %% SANTIAGO RULES            
    # =============================================================================
    
    def Sa_Rule1func(self, policy_input):
        output = 0
        if self.SD_Map.mIPop.value() >= 20 and policy_input['Closure Policy'] == 'Stage 5' and policy_input['Curfew Policy'] == 'No Curfew':
            # print('Rule 1 Triggered')
            self.SD_Map.ClosureP.values[-1] = self.PolicyDicts['Closure Policy']['Stage 3']
            self.SD_Map.SocialDisP.values[-1] = self.PolicyDicts['Curfew Policy']['Unenforced Curfew']
            output = 1
        return output
    def Sa_Rule2func(self, policy_input):
        output = 0
        if self.SD_Map.mIPop.value() >= 100 and (policy_input['Closure Policy'] in ['Stage 5', 'Stage 4']):
            # print('Rule 2 Triggered')
            self.SD_Map.ClosureP.values[-1] = self.PolicyDicts['Closure Policy']['Stage 3'] 
            output = 1
        return output
    def Sa_Rule3func(self, policy_input):
        output = 0
        if self.SD_Map.mInfectR.value() >= 100 and (policy_input['Closure Policy'] in ['Stage 5', 'Stage 4', 'Stage 3', 'Stage 2']):
            # print('Rule 3 Triggered')
            self.SD_Map.ClosureP.values[-1] = self.PolicyDicts['Closure Policy']['Stage 1']
            self.SD_Map.SocialDisP.values[-1] = self.PolicyDicts['Curfew Policy']['Enforced Curfew'] 
            output = 1
        return output
    def Sa_Rule4func(self,policy_input):
        output = 0
        if self.SD_Map.mIPop.value() <= 500 and (policy_input['Closure Policy'] in ['Stage 2', 'Stage 1']):
            # print('Rule 4 Triggered')
            self.SD_Map.ClosureP.values[-1] = self.PolicyDicts['Closure Policy']['Stage 3']
            output = 1
        return output
    def Sa_Rule5func(self, policy_input):
        output = 0
        if self.SD_Map.mIPop.value() <= 500 and policy_input['Curfew Policy'] == 'Enforced Curfew':
            # print('Rule 5 Triggered')
            self.SD_Map.SocialDisP.values[-1] = self.PolicyDicts['Curfew Policy']['Unenforced Curfew']   
            output = 1
        return output
    

       
    
    
# =============================================================================
# %% make_rules            
# =============================================================================

def make_rules(UI):
    """PUT EACH DECISION RULE INTO A RULE CLASS AND STORE THEM AS A LIST
    
    Args:
        UI: UI class so that relevant attributes can be pulled

    Returns:
        Rules: List of SDlib Rule objects for the given context
    """
    
    Conditionals = Conditional_Database(UI)
    location = UI.location
    
    
    Rules = []
    if location in ['Rio de Janeiro']:

        Rules.append(SDlib.Rule('Initial Closures', 1, 
                             func = lambda policy_input: Conditionals.Br_Rule1func(policy_input)))
        Rules.append(SDlib.Rule('Additional Closures', 2, 
                             func = lambda policy_input: Conditionals.Br_Rule2func(policy_input)))
        
        Rules.append(SDlib.Rule('Complete Lockdown', 3, 
                             func = lambda policy_input: Conditionals.Br_Rule3func(policy_input)))
        
        Rules.append(SDlib.Rule('Re-open Some Businesses', 4, 
                             func = lambda policy_input: Conditionals.Br_Rule4func(policy_input)))
        Rules.append(SDlib.Rule('Relax Mandatory Social Distancing', 5, 
                             func = lambda policy_input: Conditionals.Br_Rule5func(policy_input)))
        # Rules.append(SDlib.Rule('Order More Ventilators', 6, 
        #                      func = lambda policy_input: Conditionals.Br_Rule6func(policy_input)))
        # Rules.append(SDlib.Rule('Pay More for Ventilators to Accelerate Delivery', 7, 
        #                      func = lambda policy_input: Conditionals.Br_Rule7func(policy_input)))

    elif location in ['Indonesia']:
        #National
        Rules.append(SDlib.Rule('Implement Some Restrictions Nationwide', 1, 
                             func = lambda policy_input: Conditionals.In_Rule1func(policy_input)))
        Rules.append(SDlib.Rule('Implement High Restrictions Nationwide', 2, 
                             func = lambda policy_input: Conditionals.In_Rule2func(policy_input)))
        Rules.append(SDlib.Rule('Relax Some Restrictions Nationwide', 3, 
                             func = lambda policy_input: Conditionals.In_Rule3func(policy_input)))
        Rules.append(SDlib.Rule('Relax Mandatory Social Distancing Nationwide', 4, 
                             func = lambda policy_input: Conditionals.In_Rule4func(policy_input))) 
        #Java
        Rules.append(SDlib.Rule('Implement Some Restrictions Java - Zonal', 5, 
                             func = lambda policy_input: Conditionals.In_Rule1func_j(policy_input)))
        Rules.append(SDlib.Rule('Implement High Restrictions Java - Zonal', 6, 
                             func = lambda policy_input: Conditionals.In_Rule2func_j(policy_input)))
        Rules.append(SDlib.Rule('Relax Some Restrictions Java - Zonal', 7, 
                             func = lambda policy_input: Conditionals.In_Rule3func_j(policy_input)))
        Rules.append(SDlib.Rule('Relax Mandatory Social Distancing Java - Zonal', 8, 
                             func = lambda policy_input: Conditionals.In_Rule4func_j(policy_input))) 

        #Sulawesi
        Rules.append(SDlib.Rule('Implement Some Restrictions Sulawesi - Zonal', 9, 
                             func = lambda policy_input: Conditionals.In_Rule1func_s(policy_input)))
        Rules.append(SDlib.Rule('Implement High Restrictions Sulawesi - Zonal', 10, 
                             func = lambda policy_input: Conditionals.In_Rule2func_s(policy_input)))
        Rules.append(SDlib.Rule('Relax Some Restrictions Sulawesi - Zonal', 11, 
                             func = lambda policy_input: Conditionals.In_Rule3func_s(policy_input)))
        Rules.append(SDlib.Rule('Relax Mandatory Social Distancing Sulawesi - Zonal', 12, 
                             func = lambda policy_input: Conditionals.In_Rule4func_s(policy_input))) 

    elif location in ['Chile']:
        Rules.append(SDlib.Rule('Initial Closures', 1, 
                             func = lambda policy_input: Conditionals.Ch_Rule1func(policy_input)))
        Rules.append(SDlib.Rule('Additional Closures', 2, 
                             func = lambda policy_input: Conditionals.Ch_Rule2func(policy_input)))
        
        Rules.append(SDlib.Rule('Complete Lockdown', 3, 
                             func = lambda policy_input: Conditionals.Ch_Rule3func(policy_input)))
        
        Rules.append(SDlib.Rule('Re-open Some Businesses', 4, 
                             func = lambda policy_input: Conditionals.Ch_Rule4func(policy_input)))
        Rules.append(SDlib.Rule('Relax Mandatory Social Distancing', 5, 
                             func = lambda policy_input: Conditionals.Ch_Rule5func(policy_input)))
        Rules.append(SDlib.Rule('Order More Ventilators', 6, 
                             func = lambda policy_input: Conditionals.Ch_Rule6func(policy_input)))
        Rules.append(SDlib.Rule('Pay More for Ventilators to Accelerate Delivery', 7, 
                             func = lambda policy_input: Conditionals.Ch_Rule7func(policy_input)))
        
    elif location in ['Santiago']:
        Rules.append(SDlib.Rule('Initial Closures', 1, 
                             func = lambda policy_input: Conditionals.Sa_Rule1func(policy_input)))
        Rules.append(SDlib.Rule('Additional Closures', 2, 
                             func = lambda policy_input: Conditionals.Sa_Rule2func(policy_input)))
        
        Rules.append(SDlib.Rule('Complete Lockdown', 3, 
                             func = lambda policy_input: Conditionals.Sa_Rule3func(policy_input)))
        
        Rules.append(SDlib.Rule('Re-open Some Businesses', 4, 
                             func = lambda policy_input: Conditionals.Sa_Rule4func(policy_input)))
        Rules.append(SDlib.Rule('Relax Mandatory Social Distancing', 5, 
                             func = lambda policy_input: Conditionals.Sa_Rule5func(policy_input)))
        
    if location in ['Querétaro']:

        Rules.append(SDlib.Rule('Initial Closures', 1, 
                             func = lambda policy_input: Conditionals.Br_Rule1func(policy_input)))
        Rules.append(SDlib.Rule('Additional Closures', 2, 
                             func = lambda policy_input: Conditionals.Br_Rule2func(policy_input)))
        
        Rules.append(SDlib.Rule('Complete Lockdown', 3, 
                             func = lambda policy_input: Conditionals.Br_Rule3func(policy_input)))
        
        Rules.append(SDlib.Rule('Re-open Some Businesses', 4, 
                             func = lambda policy_input: Conditionals.Br_Rule4func(policy_input)))
        Rules.append(SDlib.Rule('Relax Mandatory Social Distancing', 5, 
                             func = lambda policy_input: Conditionals.Br_Rule5func(policy_input)))
        # Rules.append(SDlib.Rule('Order More Ventilators', 6, 
        #                      func = lambda policy_input: Conditionals.Br_Rule6func(policy_input)))
        # Rules.append(SDlib.Rule('Pay More for Ventilators to Accelerate Delivery', 7, 
        #                      func = lambda policy_input: Conditionals.Br_Rule7func(policy_input)))

    return Rules

# =============================================================================
# %% Policy_Inputs            
# =============================================================================

def Policy_Inputs(UI):
    """TAKES THE NUMERIC POLICY VALUES AND CONVERTS THEM INTO STRINGS FOR USE IN THE RULES
    
    Args:
        UI: UI class so that relevant attributes can be pulled

    Returns:
        policy_input: dictionary of Policy names to their current string values
    """
    
    PolicyDicts = UI.PolicyDicts
    PolicyDictsInv = UI.PolicyDictsInv
    Map = UI.SD_Map
    location = UI.location
    
    policy_input = dict()
                 
    
    for policy in PolicyDicts.keys():
        policy_input[policy] = PolicyDictsInv[policy][Map.retrieve_ob(policy).value()]
        
    return policy_input
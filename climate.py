#
# climate - Lib that has functions to study some extreme climate events like heatwaves, coldwaves, humidex etc
#
# Author: Lucas Hideki Ueda
# Coyright 2019
#

# Necessary libs
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
plt.style.use('default')
plt.rcParams.update({'font.size': 18})
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

# Function to get colors of extreme climatic events marks on plot
def get_hcolors(df, var_temp,mean,pct90):

    """
        Function that get the mean and percentile of a time series and return a list of rgb for "heat" colors
                
        Parameters
        ----------
        df : pandas.Dataframe
            a dataframe with the 'var_temp' variable
         
        var_temp : string
            a string with the name of the variable to analyze
       
        mean : float
            a float number that represents a mean to be considered
        
        pct90 : float
            a float number that represents a 90th percentile to be considered
    
        
        Return
        ----------
        list
            returns a list of rgb values
            
    """
    
    colors = []
    
    aux_df = df.copy()
    
    for tmp in aux_df[var_temp]:
        
        if(tmp < mean):
            color = (1,0.8,0)
        elif(tmp > pct90):
            color = (0,0,0)
        else:
            color = (1,0.1,0)
            
        colors.append(color)

    
    return colors, aux_df


# Function that plots heatwaves
def plot_heatwave(df, FLAG_HEATWAVE,var_temperature = 'MAX_N_AIRTMP_MED10', var_day = 'NEW_DAY', savefig = None):
    
    
    """
        Function to plot heatwaves, or any other evento that high values are critic. The plot is pre determined so if there are a way more data it's better to make a own plot
                
        Parameters
        ----------
        df : pandas.Dataframe
            a dataframe with the 'var_temp' variable
            
        FLAG_HEATWAVE : string
            a string with the name of the variable that flags the extreme event to analyze
         
        var_temperature : string
            a string with the name of the variable to analyze, since it was first developed to heatwaves it starts with our default temperature var name
       
        var_day : string
            a string with the name of the variable in the x axis, here the default value is the day variable name
       
        savefig : string
           a string with the name of the file that will be saved
           
        Return
        ----------
        plot
            returns a default plot by years and days along
            
    """
        
        
    # Draw horizontal lines
    fig, ax = plt.subplots(figsize=(16,10), dpi= 80)
    ax.hlines(y=np.arange(df.YEAR.nunique()), xmin=0, xmax=3000, color='gray', alpha=0.5, linewidth=.5, linestyles='dashdot')

    
    #getting pct of all temperature
    mean = df[df[FLAG_HEATWAVE] != 0][var_temperature].mean()
    pct90 = df[df[FLAG_HEATWAVE] != 0][var_temperature].quantile(.9)
    
     # Draw the Dots
    for i, make in enumerate(df.YEAR.unique()):
        df_make = df.loc[(df.YEAR==make) & (df[FLAG_HEATWAVE] != 0), :]

        colors, aux_df = get_hcolors(df_make, var_temperature, mean, pct90)

        ax.scatter(y=np.repeat(i, df_make.shape[0]), x=var_day, data=df_make, s=75, edgecolors=colors , c=colors , alpha=0.7)



    # Decorations

    # Vertical Lines to indicate Stations according to https://www.calendario-365.com.br/epocas-estacoes-do-ano.html
    ax.vlines(x= 360 , ymin=-1, ymax=21, color='black', alpha=1, linewidth=1, linestyles='dotted')
    ax.vlines(x= 90 , ymin=-1, ymax=21, color='black', alpha=1, linewidth=1, linestyles='dotted')
    ax.vlines(x= 180, ymin=-1, ymax=21, color='black', alpha=1, linewidth=1, linestyles='dotted')
    ax.vlines(x= 270 , ymin=-1, ymax=21, color='black', alpha=1, linewidth=1, linestyles='dotted')

    #Annotates
    ax.text(45, 22, " Winter ", fontdict={'size':20}, color='indigo')
    ax.text(125, 22, " Spring ", fontdict={'size':20}, color='indigo')
    ax.text(215, 22, " Summer ", fontdict={'size':20}, color='indigo')
    ax.text(300, 22, " Fall ", fontdict={'size':20}, color='indigo')


    #Corpse
    # ax.set_title('Monthly heatwaves distribution by years', fontdict={'size':22})
    ax.set_xlabel('Dias', alpha=0.7)
    ax.set_ylabel('Anos', alpha=0.7)
    ax.set_yticks(np.arange(df.YEAR.nunique()))
    ax.set_yticklabels(df.YEAR.unique(), fontdict={'horizontalalignment': 'right'}, alpha=0.7)
    ax.set_xlim(0, 370)
    plt.xticks(alpha=0.7)
    plt.gca().spines["top"].set_visible(False)    
    plt.gca().spines["bottom"].set_visible(False)    
    plt.gca().spines["right"].set_visible(False)    
    plt.gca().spines["left"].set_visible(False)   
    plt.grid(axis='both', alpha=.4, linewidth=.1)
    if(savefig != None):
        plt.savefig(savefig)
    plt.show()
    
    
    
# Plot  coldwaves
def get_ccolors(df, var_temp,mean,pct10):

    """
        Function that get the mean and percentile of a time series and return a list of rgb for "cold" colors
                
        Parameters
        ----------
        df : pandas.Dataframe
            a dataframe with the 'var_temp' variable
         
        var_temp : string
            a string with the name of the variable to analyze
       
        mean : float
            a float number that represents a mean to be considered
        
        pct10 : float
            a float number that represents a 10th percentile to be considered
    
        
        Return
        ----------
        list
            returns a list of rgb values
            
    """
    
    colors = []
    
    aux_df = df.copy()
    
    for tmp in aux_df[var_temp]:
        
        if(tmp > mean):
            color = (0,0.8,1)
        elif(tmp < pct10):
            color = (0,0,0)
        else:
            color = (0,0.1,1)
            
        colors.append(color)

    
    return colors, aux_df

def plot_coldwave(df, FLAG_COLDWAVE,var_temperature = 'MIN_N_AIRTMP_MED10', var_day = 'NEW_DAY', savefig = None):
    
    """
        Function to plot coldwave, or any other evento that low values are critic. The plot is pre determined so if there are a way more data it's better to make a own plot
                
        Parameters
        ----------
        df : pandas.Dataframe
            a dataframe with the 'var_temp' variable
            
        FLAG_COLDWAVE : string
            a string with the name of the variable that flags the extreme event to analyze
         
        var_temperature : string
            a string with the name of the variable to analyze, since it was first developed to coldwaves it starts with our default temperature var name
       
        var_day : string
            a string with the name of the variable in the x axis, here the default value is the day variable name
       
        savefig : string
           a string with the name of the file that will be saved
           
        Return
        ----------
        plot
            returns a default plot by years and days along
            
    """
    
    # Draw horizontal lines
    fig, ax = plt.subplots(figsize=(16,10), dpi= 80)
    ax.hlines(y=np.arange(df.YEAR.nunique()), xmin=0, xmax=3000, color='gray', alpha=0.5, linewidth=.5, linestyles='dashdot')

    
    #getting pct of all temperature
    mean = df[df[FLAG_COLDWAVE] != 0][var_temperature].mean()
    pct10 = df[df[FLAG_COLDWAVE] != 0][var_temperature].quantile(.1)
    
     # Draw the Dots
    for i, make in enumerate(df.YEAR.unique()):
        df_make = df.loc[(df.YEAR==make) & (df[FLAG_COLDWAVE] != 0), :]

        colors, aux_df = get_ccolors(df_make, var_temperature, mean, pct10)

        ax.scatter(y=np.repeat(i, df_make.shape[0]), x=var_day, data=df_make, s=75, edgecolors=colors , c=colors , alpha=0.7)



    # Decorations

    # Vertical Lines to indicate Stations according to https://www.calendario-365.com.br/epocas-estacoes-do-ano.html
    ax.vlines(x= 360 , ymin=-1, ymax=21, color='black', alpha=1, linewidth=1, linestyles='dotted')
    ax.vlines(x= 90 , ymin=-1, ymax=21, color='black', alpha=1, linewidth=1, linestyles='dotted')
    ax.vlines(x= 180, ymin=-1, ymax=21, color='black', alpha=1, linewidth=1, linestyles='dotted')
    ax.vlines(x= 270 , ymin=-1, ymax=21, color='black', alpha=1, linewidth=1, linestyles='dotted')

    #Annotates
    ax.text(45, 22, " Winter ", fontdict={'size':20}, color='indigo')
    ax.text(125, 22, " Spring ", fontdict={'size':20}, color='indigo')
    ax.text(215, 22, " Summer ", fontdict={'size':20}, color='indigo')
    ax.text(300, 22, " Fall ", fontdict={'size':20}, color='indigo')


    #Corpse
    # ax.set_title('Monthly heatwaves distribution by years', fontdict={'size':22})
    ax.set_xlabel('Dias', alpha=0.7)
    ax.set_ylabel('Anos', alpha=0.7)
    ax.set_yticks(np.arange(df.YEAR.nunique()))
    ax.set_yticklabels(df.YEAR.unique(), fontdict={'horizontalalignment': 'right'}, alpha=0.7)
    ax.set_xlim(0, 370)
    plt.xticks(alpha=0.7)
    plt.gca().spines["top"].set_visible(False)    
    plt.gca().spines["bottom"].set_visible(False)    
    plt.gca().spines["right"].set_visible(False)    
    plt.gca().spines["left"].set_visible(False)   
    plt.grid(axis='both', alpha=.4, linewidth=.1)
    if(savefig != None):
        plt.savefig(savefig)
    plt.show()
    
    
# function to check the shape of a dataframe, if shape[0] == 0 then there is no information in this df
def check_shape(data, day, day_name = 'DAY365'):

    """
        Auxiliar function that check the shape of a dataset in a specific day
                
        Parameters
        ----------
        data : pandas.Dataframe
            a dataframe with the 'day_name' variable
            
        day : int
            an integer number that specify a day
         
        day_name : string
            a string with the name of the day variable
           
        Return
        ----------
        bool
            returns True if the shape is above 0 else return False
            
    """
    
    # Here we explicit variable "DAY365" because of our specific application in this project
    if(data[data[day_name] == day].shape[0] == 0):
        return False
    else:
        return True


# auxiliary function to check if theres is at least 2 consecutive days with air temperature above the p90th in the past
def check_2days(data, day,day_name = 'DAY365'):
    
    """
        Auxiliar function that check the shape of a dataset in a specific day and the previous 2 days
                
        Parameters
        ----------
        data : pandas.Dataframe
            a dataframe with the 'day_name' variable
            
        day : int
            an integer number that specify a day
         
        day_name : string
            a string with the name of the day variable
           
        Return
        ----------
        bool
            returns True if the shape is above 0 else return False
            
    """
    
    # If there is information in df in the day in question and the previous 2, then return True, else there is no way exist a heatwave
    if((check_shape(data,day,day_name)) & (check_shape(data,day-1,day_name)) & (check_shape(data,day-2,day_name)) ):
        return True
    else:
        return False
    
# Function that if "check_2days" is True we check if in these 2 days the definition of heatwave is satisfied
def init_hw(data,day, day_name = 'DAY365', max_tmp_name = 'MAX_N_AIRTMP_MED10', max_p90 = 35):
    
    """
        Function that check if in a specific day starts a heatwave with an specific given percentile which will be the window based percentiles
                
        Parameters
        ----------
        data : pandas.Dataframe
            a dataframe with the 'max_tmp_name' variable
            
        day : int
            an integer number that specify a day
         
        day_name : string
            a string with the name of the day variable
        
        max_tmp_name : string
            a string with the name of maximum air temperature
            
        max_p90 : float
            a float with the percentile 90 for this specific day
           
        Return
        ----------
        bool
            returns True its a init of heatwave else returns False
            
    """
    
    # Variables that is in our interest
    var_names = [max_tmp_name,day_name]
    
    actual_df = data[data[day_name] == day][var_names]
    
    if(check_2days(data,day)):
        
        #Creating auxiliar df's for 1 day and 2 day back 
        df1_back = data[data[day_name] == day - 1][var_names]
        df2_back = data[data[day_name] == day - 2][var_names]

        df1_forward = data[data[day_name] == day + 1][var_names]
        df2_forward = data[data[day_name] == day + 2][var_names]

        c1_b = df1_back[max_tmp_name].values >= max_p90
        c2_b = df2_back[max_tmp_name].values >= max_p90
        c1_f = df1_forward[max_tmp_name].values >= max_p90
        c2_f = df2_forward[max_tmp_name].values >= max_p90
        c3 = actual_df[max_tmp_name].values >= max_p90

        #Condition if there is 2 days before now that the temperature exceeds the pth
        c_b = c1_b & c2_b
        
        #Condition if there is 2 days AFTER now that the temperature exceeds the pth
        c_f = c1_f & c2_f
        
        if(c3&(c_b | c_f)):
            return True
        else:
            return False
    else:
        return False
    
# Function to actually get heatwaves
def get_heatwave(data, flag, hw_name='none',percentile = 0.9, day_name = 'DAY365', year_name = 'YEAR', max_tmp_name = 'MAX_N_AIRTMP_MED10'):
   
    """
        Get heatwave returns a df with the target days under heatwave effect
                
        Parameters
        ----------
        data : pandas.Dataframe
            a dataframe with the 'max_tmp_name', 'day_name' and 'year_name' variables
         
        flag : string
            a string name that represents a flag if there is or not a heatwave
         
        hw_name : string
            a string name that represents which heatwave is there
            
        day_name : string
            a string with the name of day variable
         
        year_name : string
           a string with the name of the year variable
        
        max_tmp_name : string
            a string with the name of maximum air temperature
            
        percentile : float
            a float with the percentile 90 for this specific day
           
        Return
        ----------
        DataFrame
            returns a dataframe with the flags of heatwave and unique heatwave
            
    """
    
    # Define a df that is out mutable dataframe
    df = data.copy()
    
    # here we define the flag variable names
    flag_heat = flag
    flag_unique_heat = hw_name

    # Defining variable that flags heat waves with zeros
    df[flag_heat] = 0
    df[flag_unique_heat] = 0

    # Variable that describe unique heataves, each one of hetawaves will have an unique integer number
    which_heat_wave = 1
    new_hw = False
    
    for y in df[year_name].unique():
        df_year = df[df[year_name] == y]



        itera = iter(df_year[day_name].unique())

        for d in itera:
            # For each day we will have a different pct
            df_pct = df[(df[day_name] >= d-15) & (df[day_name] <= d + 15)]

            pth_max = df_pct[max_tmp_name].quantile(percentile)

            if(init_hw(df_year,d,day_name,max_p90=pth_max,max_tmp_name = max_tmp_name)):
                new_hw = True
                df.loc[(df[year_name] == y) & (df[day_name] == d) , flag_heat] = 1
                df.loc[(data[year_name] == y) & (data[day_name] == d) , flag_unique_heat] = which_heat_wave
            else:
                if(new_hw == True):
                    which_heat_wave = which_heat_wave + 1
                    new_hw = False
                pass
    return df



# Function that if "check_2days" is True we check if in these 2 days the definition of coldwave is satisfied
def init_cw(data,day,day_name = 'DAY365',min_tmp_name = 'MIN_N_AIRTMP_MED10',  min_p10 = 25):

    """
        Function that check if in a specific day starts a coldwave with an specific given percentile which will be the window based percentiles
                
        Parameters
        ----------
        data : pandas.Dataframe
            a dataframe with the 'min_tmp_name' variable
            
        day : int
            an integer number that specify a day
         
        day_name : string
            a string with the name of the day variable
        
        min_tmp_name : string
            a string with the name of minimum air temperature
            
        min_p10 : float
            a float with the percentile 10 for this specific day
           
        Return
        ----------
        bool
            returns True its a init of coldwave else returns False
            
    """
    
    # Variables that is in our interest
    var_names = [min_tmp_name,'DAY365']
    
    actual_df = data[data['DAY365'] == day][var_names]
    
    if(check_2days(data,day)):
        
        #Creating auxiliar df's for 1 day and 2 day back 
        df1_back = data[data['DAY365'] == day - 1][var_names]
        df2_back = data[data['DAY365'] == day - 2][var_names]

        df1_forward = data[data['DAY365'] == day + 1][var_names]
        df2_forward = data[data['DAY365'] == day + 2][var_names]

        c1_b = df1_back[min_tmp_name].values <= min_p10
        c2_b = df2_back[min_tmp_name].values <= min_p10
        c1_f = df1_forward[min_tmp_name].values <= min_p10
        c2_f = df2_forward[min_tmp_name].values <= min_p10
        c3 = actual_df[min_tmp_name].values <= min_p10


        #Condition if there is 2 days before now that the temperature exceeds the pth
        c_b = c1_b & c2_b
        
        #Condition if there is 2 days AFTER now that the temperature exceeds the pth
        c_f = c1_f & c2_f
        
        if(c3&(c_b | c_f)):
            return True
        else:
            return False
    else:
        return False

# Function to actually get coldwaves
def get_coldwave(data, flag, cw_name='none',percentile = 0.1, day_name = 'DAY365', year_name = 'YEAR',min_tmp_name = 'MIN_N_AIRTMP_MED10'):

    """
        Get coldwave returns a df with the target days under coldwave effect
                
        Parameters
        ----------
        data : pandas.Dataframe
            a dataframe with the 'max_tmp_name', 'day_name' and 'year_name' variables
         
        flag : string
            a string name that represents a flag if there is or not a coldwave
         
        hw_name : string
            a string name that represents which coldwave is there
            
        day_name : string
            a string with the name of day variable
        
        year_name : string
           a string with the name of the year variable
        
        min_tmp_name : string
            a string with the name of minimum air temperature
            
        percentile : float
            a float with the percentile 10 for this specific day
           
        Return
        ----------
        DataFrame
            returns a dataframe with the flags of coldwave and unique coldwave
            
    """
    
    # Define a df that is out mutable dataframe
    df = data.copy()
    
    # here we define the flag variable names
    flag_cold = flag
    flag_unique_cold = cw_name

    # Defining variable that flags coldwave with zeros
    df[flag_cold] = 0
    df[flag_unique_cold] = 0

    # Variable that describe unique coldwave, each one of coldwave will have an unique integer number
    which_cold_wave = 1
    new_cw = False
    
    for y in df[year_name].unique():
        df_year = df[df[year_name] == y]



        itera = iter(df_year[day_name].unique())

        for d in itera:
            # For each day we will have a different pct
            df_pct = df[(df[day_name] >= d-15) & (df[day_name] <= d+15 )]

            pth_min = df_pct[min_tmp_name].quantile(percentile)
            if(init_cw(df_year,d,day_name,min_p90=pth_min, min_tmp_name = min_tmp_name)):
                new_cw = True
                df.loc[(df[year_name] == y) & (df[day_name] == d) , flag_cold] = 1
                df.loc[(data[year_name] == y) & (data[day_name] == d) , flag_unique_cold] = which_cold_wave
            else:
                if(new_cw == True):
                    which_cold_wave = which_cold_wave + 1
                    new_cw = False
                pass
    return df


# Function get thermal amplitude waves
def get_thermamp(data, flag, ta_name='none',percentile = 0.9, day_name = 'DAY365', year_name = 'YEAR', therm_amp_name = 'MAX_N_AIRTMP_MED10'):

    """
        Get thermal amplitude wave returns a df with the target days under termal amplitude wave effect
                
        Parameters
        ----------
        data : pandas.Dataframe
            a dataframe with the 'max_tmp_name', 'day_name' and 'year_name' variables
         
        flag : string
            a string name that represents a flag if there is or not a termal amplitude wave
         
        ta_name : string
            a string name that represents which termal amplitude wave is there
            
        day_name : string
            a string with the name of day variable
        
        year_name : string
           a string with the name of the year variable
        
        therm_amp_name : string
            a string with the name of thermal amplitude of air temperature
            
        percentile : float
            a float with the percentile 90 for this specific day
           
        Return
        ----------
        DataFrame
            returns a dataframe with the flags of termal amplitude wave and unique termal amplitude wave
            
    """
    
    # Define a df that is out mutable dataframe
    df = data.copy()
    
    # here we define the flag variable names
    flag_ta = flag
    flag_unique_ta = ta_name

    # Defining variable that flags termal amplitude wave with zeros
    df[flag_cold] = 0
    df[flag_unique_cold] = 0

    # Variable that describe unique termal amplitude wave, each one of termal amplitude wave will have an unique integer number
    which_ta_wave = 1
    new_ta = False
    
   

    pth_max = 15
    
    for y in df[year_name].unique():
        df_year = df[df[year_name] == y]



        itera = iter(df_year[day_name].unique())

        for d in itera:

            if(init_cw(df_year,d,day_name,max_p90=pth_max)):
                new_cw = True
                df.loc[(df[year_name] == y) & (df[day_name] == d) , flag_ta] = 1
                df.loc[(df[year_name] == y) & (df[day_name] == d) , flag_unique_ta] = which_ta_wave
            else:
                if(new_ta == True):
                    which_ta_wave = which_ta_wave + 1
                    new_ta = False
                pass
    return df


# Functions to get e and H given T in celsius and dewpoint also in celsius to get humidex index

def get_e(td):
    e = 6.11*np.exp(5417.7530*((1/273.16) - 1/(td+273.16)))
    return e

def get_humidex(T,td):
    H = T + (0.5555*(get_e(td) - 10))
    return H

def get_td(t,hr):
    td = t - (100-hr)/5
    return td
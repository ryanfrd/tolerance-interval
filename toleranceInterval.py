import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as st
import os

def readFile(filename,sheetname=None):
    if '.csv' in filename:
         df = pd.read_csv(filename)
    else:
        xl = pd.ExcelFile(filename)
        if sheetname:
            df = pd.read_excel(xl,sheetname)
        else:
            df = pd.read_excel(xl)
    return df,filename

def two_sided_toleranceInterval(
        data: pd.DataFrame = None,
        x: float = None,
        sd: float = None,
        n: int = None,
        xlab: str = None,
        plot_title: str = None,
        p: float = 0.95,
        alpha: float = 0.05,
        upper_lim: float =None,
        lower_lim: float =None
        )->tuple[plt.Figure,pd.DataFrame]:

    if data is not None:
        x = np.mean(data)
        sd = np.std(data,ddof=1).iloc[0]
        n = len(data)


    Limits = False
    if upper_lim is not None or lower_lim is not None:
        Limits = True
    h = (1+p)/2
    Z = st.norm.ppf(h)
    dof = n-1
    chi = st.chi2.ppf(alpha,dof)

    k = Z*np.sqrt((dof*(1+(1/n)))/chi)
    k_res = "N/A"

    UL = x+sd*k
    LL = x-sd*k

    x_axis = np.arange(LL-(abs(LL)*0.5),UL+(abs(UL)*0.5),abs((UL+abs(UL)*0.5)/1000))

    font = {'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        'size': 8,
        }
    newline = '\n'

    fig,ax = plt.subplots(1,1)

    if data is not None:
        plt.hist(data,density=True) # overlay the actual histogram
    else:
        x_axis = np.linspace(x - 4*sd, x + 4*sd, 1000)
        plt.plot(x_axis, st.norm.pdf(x_axis, x, sd))

    plt.plot(x_axis, st.norm.pdf(x_axis,x,sd))
    plt.axvline(LL,color='g',linestyle ='--')
    plt.axvline(UL,color='g',linestyle='--',label='Tolerance')
    xlimits = [LL,UL]
    if Limits:
        plt.axvline(upper_lim,color='r',linestyle='--')
        plt.axvline(lower_lim,color='r',linestyle='--',label='Spec Limits')
        xlimits.append(lower_lim)
        xlimits.append(upper_lim)

        k_res = (upper_lim - lower_lim)/sd
    min_xlim = min(xlimits)
    max_xlim = max(xlimits)
    range_xlim = max_xlim-min_xlim
    plt.xlim([min_xlim - (0.25*range_xlim), max_xlim + (0.25*range_xlim)])
    plt.title(f"{plot_title}")
    plt.xlabel(xlab)
    plt.ylabel("Probability density")
    t = f"With {str((1-alpha)*100)}% confidence, {p*100}% of the population will fall within [{round(LL,2)} , {round(UL,2)}]"
    plt.legend(loc = 'upper right')

    header = ['mean','sd','sample size','alpha','p','Z','Chi^2','kcrit','k_res','UL','LL',]
    out_df = pd.DataFrame([[x,sd,n,alpha,p,Z,chi,k,k_res,UL,LL]],columns=header)

    return (fig,out_df,t)

def one_sided_toleranceInterval(
        data: pd.DataFrame,
        x: float = None,
        sd: float = None,
        n: int = None,
        xlab: str = None,
        plot_title: str = None,
        p: float = 0.95,
        alpha: float = 0.05,
        up_low: str = "Upper",
        limit: float = None
        )->tuple[plt.Figure,pd.DataFrame]: 
    
    if data is not None:
        x = np.mean(data)
        sd = np.std(data,ddof=1)
        n = len(data)

    Limits = False
    if limit is not None:
        Limits = True
    h = p
    Z = st.norm.ppf(h)
    za = st.norm.ppf(alpha)

    a = 1-((za**2)/(2*(n-1)))
    b = (Z**2) - ((za**2)/n)
    k = (Z + np.sqrt((Z**2)-a*b))/a
    k_res = "N/A"

    UL = x+sd*k
    LL = x-sd*k

    if "Upper" in up_low:
        tol = UL
    elif "Lower" in up_low:
        tol = LL
    else:
        raise ValueError("up_low must be either 'Upper' or 'Lower'")

    x_axis = np.arange(LL-(abs(LL)*0.2),UL+(abs(UL)*0.2),abs((UL+abs(UL)*0.2)/1000))

    font = {'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        'size': 8,
        }
    newline = '\n'

    fig,ax = plt.subplots(1,1)

    if data is not None:
        plt.hist(data,density=True) # overlay the actual histogram
    else:
        x_axis = np.linspace(x - 4*sd, x + 4*sd, 1000)
        plt.plot(x_axis, st.norm.pdf(x_axis, x, sd))

    plt.plot(x_axis, st.norm.pdf(x_axis,x,sd))
    plt.axvline(tol,color='g',linestyle='--',label='Tolerance')
    xlimits = [LL,UL]
    if Limits:
        plt.axvline(limit,color='r',linestyle='--',label='Spec Limits')
        xlimits.append(tol)

        if "Upper" in up_low:
            k_res = (limit - x)/sd
        elif "Lower" in up_low:
            k_res = (x-limit)/sd
    min_xlim = min(xlimits)
    max_xlim = max(xlimits)
    range_xlim = max_xlim-min_xlim
    plt.xlim([min_xlim - (0.25*range_xlim), max_xlim + (0.25*range_xlim)])
    plt.title(f"{plot_title}")
    plt.xlabel(xlab)
    plt.ylabel("Probability density")
    plt.legend(loc = 'upper right')
    
    if "Upper" in up_low:
        t = f"With {str((1-alpha)*100)}% confidence, {p*100}% of the population will not exceed {round(tol,2)}"
        header = ['mean','sd','sample size','alpha','p','Z','k-crit','k_res','UL']
        out_df = pd.DataFrame([[x,sd,n,alpha,p,Z,k,k_res,UL]],columns=header)
    else:
        t = f"With {str((1-alpha)*100)}% confidence, {p*100}% of the population will not fall below {round(tol,2)}"
        header = ['mean','sd','sample size','alpha','p','Z','k-crit','k_res','LL']
        out_df = pd.DataFrame([[x,sd,n,alpha,p,Z,k,k_res,LL]],columns=header)

    return (fig,out_df,t)

if __name__ == "__main__":

    filename = "file\\path"
    result_folder = "result\\folder"
    os.makedirs(result_folder,exist_ok=True)
    data,filename = readFile(filename)


import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

mpl.rcParams["figure.figsize"] = (10, 6)
plt.style.use("ggplot")

def count_total(data, state=None):
    """
    Count total deaths.

    Args:
        data (DataFrame): DataFrame containing the shootings data.
        state (str, optional): State to select when counting.

    Returns:
        None.
    """
    df = data.copy()
    if state:
        pv = df[df["State"] == state].pivot_table(
            values="State",
            index="City", 
            columns="Manner of Death", 
            aggfunc="count", 
            fill_value=0
        )
        title = f"Deaths by City in the State of {state}"
    else: # all US
        pv = df.pivot_table(
            values="City",
            index="State",
            columns="Manner of Death",
            aggfunc="count",
            fill_value=0
        )
        title = f"Deaths by State in the US"
    pv.sort_values(by="Shot", ascending=False, inplace=True)
    ax = pv.head(10)[::-1].plot.barh(stacked=True)
    ax.set(title=title, xlabel="Total Deaths")

def show_trend(data, attr=None, time_interval=None, state=None, city=None):
    """
    Show death trend (total deaths by month).

    Args:
        data (DataFrame): DataFrame containing the shootings data.
        attr (str): Wether to separate deaths by attr.
        time_interval (tuple of int, optional): Time interval to show, in years.
        state (str, optional): State to show.
        city (str, optional): City to show. "state" should be None if this parameter is used.

    Returns:
        None.
    """
    df = data.copy()
    start, stop = np.min(df.index.year), np.max(df.index.year)
    title = "Death trend"
    if state:
        df = df[df["State"] == state]
        title += f" in the state of {state}"
    elif city:
        df = df[df["City"] == city]
        title += f" in the city of {city}"
    else:
        title += f" in the US"
    if time_interval:
        start, stop = (str(year) for year in time_interval)
        df = df[start:stop]
    if attr:
        ax = df.pivot_table(
            values="State",
            index=[df.index.year, df.index.month],
            columns=attr,
            aggfunc="count"
        ).plot.area()
        ax.set(xlabel="Date")
    else:
        ax = df.resample("M")["State"].count().plot()
    title += f" in the years {start}-{stop}"
    ax.set(title=title, ylabel="Monthly Deaths")

def age_dist(data, rows=None, cols=None, state=None, city=None):
    """
    Show age distplot.

    Args:
        data (DataFrame): DataFrame containing the shootings data.
        rows (str or list of str): Attribute to show in the FacetGrid rows.
        cols (str or list of str): Attribute to show in the FacetGrid columns.
        state (str, optional): State to show.
        city (str, optional): City to show. "state" should be None if this parameter is used.

    Returns:
        None.
    """
    df = data.copy()
    title = "Age distribution of victims"
    if state:
        df = df[df["State"] == state]
        title += f" in the state of {state}"
    elif city:
        df = df[df["City"] == city]
        title += f" in the city of {city}"
    else:
        title += f" in the US"
    if rows or cols: # use FacetGrid
        g = sns.FacetGrid(df, row=rows, col=cols, height=6, aspect=10/6, sharex=False)
        g = g.map(sns.distplot, "Age")
        g.fig.subplots_adjust(top=0.9)
        g.fig.suptitle(title, fontsize=18)
    else: # consider all age data and add boxplot
        _, axs = plt.subplots(2, 1, sharex=True)
        sns.distplot(df["Age"], ax=axs[0])
        axs[0].set(title=title, xlabel="")
        sns.boxplot(df["Age"], ax=axs[1])
        locator = plt.FixedLocator(list(range(0, 101, 5)))
        axs[1].xaxis.set_major_locator(locator)
    
def race_pie(data, attr=None, time_interval=None, state=None, city=None):
    """
    Show race pie chart.
    
    Args:
        data (DataFrame): DataFrame containing the shootings data.
        time_interval (tuple of int, optional): Time interval to show, in years.
        state (str, optional): State to show.
        city (str, optional): City to show. "state" should be None if this parameter is used.

    Returns:
        None.
    """
    df = data.copy()
    start, stop = np.min(df.index.year), np.max(df.index.year)
    title = "Race proportion"
    if time_interval:
        start, stop = (str(year) for year in time_interval)
        df = df[start:stop]
    if state:
        df = df[df["State"] == state]
        title += f" in the state of {state}"
    elif city:
        df = df[df["City"] == city]
        title += f" in the city of {city}"
    else:
        title += f" in the US"
    if attr:
        df = df.pivot_table(
            values="State",
            index="Race",
            columns=attr,
            aggfunc="count"
        )
        ax = df
    else:
        ax = df["Race"].value_counts().plot.pie()
    title += f" in the years {start}-{stop}"
    ax.set(title=title)
    

def body_camera_use(data, state=None, city=None):
    pass
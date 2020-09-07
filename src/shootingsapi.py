import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

mpl.rcParams["figure.figsize"] = (10, 5)
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
    Plot death trend (total deaths by month).

    Args:
        data (DataFrame): DataFrame containing the shootings data.
        attr (str, optional): Group deaths by this attribute.
        time_interval (tuple of int, optional): Time interval to consider, in years.
        state (str, optional): State to plot.
        city (str, optional): City to plot. "state" should be None if this parameter is used.

    Returns:
        None.
    """
    df = data.copy()
    start, stop = np.min(df.index.year), np.max(df.index.year)
    title = "Death Trend"
    if state:
        df = df[df["State"] == state]
        title += f" in the State of {state}"
    elif city:
        df = df[df["City"] == city]
        title += f" in the City of {city}"
    else:
        title += f" in the US"
    if time_interval:
        start, stop = (str(year) for year in time_interval)
        df = df[start:stop]
    title += f" in the Years {start}-{stop}"
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
    ax.set(title=title, ylabel="Monthly Deaths")

def age_dist(data, rows=None, cols=None, state=None, city=None):
    """
    Plot age distplot.

    Args:
        data (DataFrame): DataFrame containing the shootings data.
        rows (str or list of str): Attributes to show in the FacetGrid rows.
        cols (str or list of str): Attributes to show in the FacetGrid columns.
        state (str, optional): State to plot.
        city (str, optional): City to plot. "state" should be None if this parameter is used.

    Returns:
        None.
    """
    df = data.copy()
    title = "Age Distribution of Victims"
    if state:
        df = df[df["State"] == state]
        title += f" in the State of {state}"
    elif city:
        df = df[df["City"] == city]
        title += f" in the City of {city}"
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
    Plot race pie chart.
    
    Args:
        data (DataFrame): DataFrame containing the shootings data.
        attr (str, optional): Group deaths by this attribute.
        time_interval (tuple of int, optional): Time interval to consider, in years.
        state (str, optional): State to plot.
        city (str, optional): City to plot. "state" should be None if this parameter is used.

    Returns:
        None.
    """
    df = data.copy()
    start, stop = np.min(df.index.year), np.max(df.index.year)
    title = "Race Proportion"
    if time_interval:
        start, stop = (str(year) for year in time_interval)
        df = df[start:stop]
    if state:
        df = df[df["State"] == state]
        title += f" in the State of {state}"
    elif city:
        df = df[df["City"] == city]
        title += f" in the City of {city}"
    else:
        title += f" in the US"
    title += f" in the Years {start}-{stop}"
    if attr:
        df = df.pivot_table(
            values="State",
            index="Race",
            columns=attr,
            aggfunc="count"
        )
        axs = df.plot.pie(
            subplots=True, 
            labeldistance=None, 
            title=title, 
            figsize=(15, 7)
        )
        # plot a unique centered legend
        _, legend = axs[0].get_legend_handles_labels()
        plt.gcf().legend(legend, loc="lower center")
        for ax in axs:
            ax.get_legend().remove()
    else:
        df["Race"].value_counts().plot.pie(title=title)
    

def top_arms(data, attr=None, top=5, percentage=False, time_interval=None, state=None, city=None):
    """
    Plot a summary of top "armed" category values.

    Args:
        data (DataFrame): DataFrame containing the shootings data.
        attr (str, optional): Group deaths by this attribute.
        top (int, default 5): Select this ammount of top arms.
        percentage (bool, default False): Wether to plot in percentage.
        time_interval (tuple of int, optional): Time interval to show, in years.
        state (str, optional): State to plot.
        city (str, optional): City to plot. "state" should be None if this parameter is used.

    Returns:
        None.
    """
    df = data.copy()
    start, stop = np.min(df.index.year), np.max(df.index.year)
    title = f"Top {top} Arm Usage"
    if time_interval:
        start, stop = (str(year) for year in time_interval)
        df = df[start:stop]
    if state:
        df = df[df["State"] == state]
        title += f" in the State of {state}"
    elif city:
        df = df[df["City"] == city]
        title += f" in the City of {city}"
    else:
        title += f" in the US"
    title += f" in the Years {start}-{stop}"
    if attr:
        df = df.pivot_table(
            values="State",
            index=attr,
            columns="Armed",
            aggfunc="count"
        ).fillna(0).sort_values("Gun", ascending=False)
        df.sort_values(by=df.index[0], axis="columns", ascending=False, inplace=True)
        df = df.iloc[:, :top]
    else:
        df = df["Armed"].value_counts().sort_values(ascending=False)[:top]
    if percentage:
        df = df.transform(lambda row: row/sum(row)*100, axis="columns")
        ylabel = "Deaths Percentage"
    else:
        ylabel = "Deaths"
    df.plot.bar(title=title, ylabel=ylabel)
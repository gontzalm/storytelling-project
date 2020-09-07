import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

mpl.rcParams["figure.figsize"] = (10, 6)
plt.style.use("ggplot")

def count_total(data, state=None):
    """Count total deaths"""
    df = data.copy()
    if state:
        pv = df[df["State"] == state].pivot_table(
            values="State",
            index="City", 
            columns="Manner of Death", 
            aggfunc="count", 
            fill_value=0
        )
        title=f""
    else: # all US
        pv = df.pivot_table(
            values="City",
            index="State",
            columns="Manner of Death",
            aggfunc="count",
            fill_value=0
        )
    pv.sort_values(by="Shot", ascending=False, inplace=True)
    ax = pv.head(10)[::-1].plot.barh(stacked=True)
    ax.set(xlabel="Total Deaths")

def show_trend(data, time_interval=None, state=None, city=None):
    pass

def age_dist(data, age_interval=None, gender=False, state=None, city=None):
    pass

def race_pie(data, time_interval=None, state=None, city=None):
    pass

def body_camera_use(data, state=None, city=None):
    pass


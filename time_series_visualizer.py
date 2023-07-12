import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv')
df['date'] = pd.to_datetime(df['date'])
df = df.set_index('date')

# Clean data
# Filter out days when page views in bottom/top 2.5%
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    fig,ax = plt.subplots()
    ax.plot(df['value'], color='red',linewidth=1)

    # Labels
    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    plt.xlabel("Date")
    plt.ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
  
    df_bar['year'] = pd.DatetimeIndex(df_bar.index).year
    df_bar['month'] = pd.DatetimeIndex(df_bar.index).month

    df_bar = df_bar.groupby(['year','month'])['value'].mean()
    df_bar = df_bar.unstack()

    # Draw bar plot
    fig = df_bar.plot(kind='bar').figure

    # Legend
    plt.legend(title='Months',labels=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October','November','December'])

    # Labels
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')


    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)

    fig,(box1,box2) = plt.subplots(1,2)

    # First Axis
    box1 = sns.boxplot(x=df_box['year'], y=df_box['value'], data=df_box, ax=box1)

    box1.set_title('Year-wise Box Plot (Trend)')
    box1.set_xlabel('Year')
    box1.set_ylabel('Page Views')

    # Fix Month Order
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
  
    # Second Axis
    box2 = sns.boxplot(x=df_box['month'], order = month_order, y=df_box['value'], data=df_box,ax=box2)
  
    box2.set_title("Month-wise Box Plot (Seasonality)")
    box2.set_xlabel('Month')
    box2.set_ylabel('Page Views')

    
    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig

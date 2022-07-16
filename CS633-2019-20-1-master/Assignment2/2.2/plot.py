import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import sys


filename="datafile" + str(sys.argv[1]) + ".csv"

sns.set(style="ticks")

df =  pd.read_csv(filename)
g = sns.catplot(x="Datasizes", y="Bandwidth", hue="Algo", col="ppn", data=df, kind="box", height=5, aspect=.8);


img="plot-" + str(sys.argv[1]) + ".jpg"
plt.savefig(img, dpi=400)


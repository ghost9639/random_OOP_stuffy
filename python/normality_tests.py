"""
Two Neighbourhood areas in Ames, North Ames and College Centre, stored as dummies in 'Neighborhood' variable
testing whether the variable 1st floor sf from NAmes and CollgCR are normal
Run prob plots on both to taste test
finally running Kolmogorov–Smirnov test on both to test for normality formally
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns


df = pd.read_csv("Use_data/AmesHousing.csv")

def shrink_ints(df): #substitutes smaller datatypes where possible to save memory
    mapping = {}
    for col in df.dtypes[df.dtypes=='int64[pyarrow]'].index:
        max_ = df[col].max()
        min_ = df[col].min()
        if min_ < 0:
            continue
        if max_ < 255:
            mapping[col] = 'uint8[pyarrow]'
        elif max_ < 65_535:
            mapping[col] = 'uint16[pyarrow]'
        elif max_ <  4294967295:
            mapping[col] = 'uint32[pyarrow]'
    return df.astype(mapping)


def clean_housing(df): #standardises np.NaN and removes data past 2023
    return (df
     .assign(**df.select_dtypes('object').replace('', 'Missing').astype('category'),
             **{'Garage Yr Blt': df['Garage Yr Blt'].clip(upper=df['Year Built'].max())})
     .pipe(shrink_ints)
    )    

housing = clean_housing(df)

print(housing
	.groupby('Neighborhood')
	.describe()
	.loc[['CollgCr','NAmes'], ['SalePrice']]
	.T    #no particular reason for transpose it's just easier to read these summary statistics like that
	)

N_ames = (housing     #sale prices for both areas stored in here
	.query('Neighborhood == "NAmes"')
	.SalePrice)
college_cr = (housing
	.query('Neighborhood == "CollgCr"')
	.SalePrice)
	


def overlaid_hist_sns(df, nominal, RefCol1, RefCol2): #makes overlaid histograms of sales prices for any 2 dummies in a nominal variable
	plt.figure(figsize=(10,6))
	
	sns.histplot(data=df[df[nominal]==RefCol1], #generalises across nominal variables because I prefer abstract design when speed isn't king
	x='SalePrice',
	color = 'skyblue',
	label = f"{RefCol1}",
	kde = False,
	alpha = 0.5)
	
	sns.histplot(data=df[df[nominal]==RefCol2],
	x='SalePrice',
	color = 'salmon',
	label = f"{RefCol2}",
	kde = False,
	alpha = 0.5)
	
	plt.title(f"Overlaid Histogram of Sale Prices in {RefCol1} and {RefCol2}")
	plt.xlabel('Sale Price')
	plt.ylabel('Count')
	plt.legend()
	plt.tight_layout()
	plt.show()
	
overlaid_hist_sns(housing, 'Neighborhood', 'NAmes', 'CollgCr') 
#clearly different distributions, both look to have too much excess kurtosis (tailedness) to be credibly normal


	
def plot_cdf(series1, series2, label1 = None, label2 = None):  #constructs experimental CDFs to compare distributions
    plt.figure(figsize=(8,6))
    
    sns.ecdfplot(data = series1, label = label1)
    sns.ecdfplot(data = series2, label = label2)
    
    plt.xlabel("ECDFs")
    plt.ylabel(f"CDF of {series1.name} and {series2.name}")
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.show()
    
    
plot_cdf(N_ames, college_cr, label1 = 'North Ames', label2 = 'College Creation')



def run_ks(Series1, Series2): #hypothesis tests for normality in both series, this is generalised to any two data series entered
	ks, p_value = stats.ks_2samp(Series1, Series2)
	if (p_value < 0.01):
		print("Evidence at 99% CI to reject same distribution")
	elif (p_value < 0.05):
		print("Evidence at 95% CI to reject same distribution")
	else:
		print("No statistically significant evidence to reject different sampling distributions")

run_ks(N_ames, college_cr)






























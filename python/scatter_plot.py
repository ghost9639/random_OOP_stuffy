"""
General Scatterplot function and data cleaning
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("Use_data/AmesHousing.csv")


def shrink_ints(df):     #saves memory by converting unnecessarily large / signed numbers to more efficient options
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


def clean_housing(df):     #replaces missing values with 'Missing' explicitly, and clips garage year built because there is one value above 2023 when the dataset was made
    return (df
     .assign(**df.select_dtypes('object').replace('', 'Missing').astype('category'),
             **{'Garage Yr Blt': df['Garage Yr Blt'].clip(upper=df['Year Built'].max())})
     .pipe(shrink_ints)
    )  

housing = clean_housing(df)



def scatterplot(df, RefCol1, RefCol2):
	plt.figure(figsize=(8,6))
	sns.scatterplot(data=df,x=RefCol1,y=RefCol2)   #seaborn for ease
	plt.title('Title')
	plt.tight_layout()
	plt.show()
	
	
scatterplot(housing, '1st Flr SF', 'SalePrice')

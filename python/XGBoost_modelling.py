"""
XGBoost provides gradient boosting regression functionality. Decision trees are used for optimisation. This comes with risk of black boxing,
even if it is relatively interpretable with the 'weight' and 'gain' readers, so it must be used extremely carefully in analysis. As such, 
I also used adjusted r^2 specifically, to potentially mediate some overfitting from brute forcing RSS reduction.
"""

import xgboost as xgb
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

df = pd.read_csv("/Use_data/AmesHousing.csv")

def shrink_ints(df): #turns overly large storage type to smaller one to save memory
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


def clean_housing(df): #streamlines np.NaN handling and and removes an entry in the year 2200 
    return (df
     .assign(**df.select_dtypes('object').replace('', 'Missing').astype('category'),
             **{'Garage Yr Blt': df['Garage Yr Blt'].clip(upper=df['Year Built'].max())})
     .pipe(shrink_ints)
    )    

housing = clean_housing(df)

X = housing.select_dtypes('number').drop(['SalePrice', 'Order','PID'], axis=1)  #estimating sales price of houses in Ames, avoiding use of researcher imposed variables
y = df['SalePrice']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)  #this splits the data into randomly assorted training and testing sets
model = xgb.XGBRegressor(
	objective='reg:squarederror', #fitting to minimise residuals
	n_estimators=100,
	learning_rate=0.1,
	max_depth=6,
	random_state=42 #random state given for reproducibility
	)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)

print(f"Mean Squared Error: {mse:.2f}")  #f-string to print MSE in readable way

y_pred = model.predict(X_test)

r2 = r2_score(y_test, y_pred)

n = X_test.shape[0]  # number of samples
p = X_test.shape[1]  # number of feature

adjusted_r2 = 1 - (1 - r2) * ((n - 1) / (n - p - 1)) #adj-r^2 penalises overfitting by including regressors (features)

print(f"R²: {r2:.4f}")
print(f"Adjusted R²: {adjusted_r2:.4f}")

booster = model.get_booster()    #booster indicates how much value the model gets when any specific feature is added

importance_types = ['weight', 'gain']  #weight indicates how much the model factors in a feature, and gain is the direction of impact, enumeration for later use
importance_dfs = []

for imp_type in importance_types:
	scores = booster.get_score(importance_type = imp_type)
	df = pd.DataFrame.from_dict(scores, orient='index', columns = [imp_type])   #get a dataframe of parameter estimates in training
	importance_dfs.append(df)
	
feature_importance = pd.concat(importance_dfs, axis=1).fillna(0)   #fills unused data with 0 and sorts the dataframe
feature_importance = feature_importance.sort_values(by='gain',ascending=False)
feature_importance.index.name = 'feature'
feature_importance = feature_importance.reset_index()

plt.figure(figsize=(6,8))
top_n = 6        #number of features used in proper ML model to avoid overfitting, 6 is arbitrarily selected       


def plot_weight(): #constructs a bar chart of XGBoost weights using seaborn for ease
	sns.barplot(
	data=feature_importance.nlargest(top_n, 'weight'),
	y='feature', x='weight',palette = 'viridis'
	)
	plt.title(f"Top {top_n} Features by Weight")
	plt.xlabel("Weight (Frequency in Trees)")
	plt.ylabel("Feature")
	plt.tight_layout()
	plt.show()

plot_weight()

def plot_gain(): #same for gain
	sns.barplot(
	data=feature_importance.nlargest(top_n, 'gain'),
	y='feature', x='gain',palette = 'viridis'
	)
	plt.title(f"Top {top_n} Features by Gain")
	plt.xlabel("Gain (Frequency in Trees)")
	plt.ylabel("Feature")
	plt.tight_layout()
	plt.show()



plot_gain()























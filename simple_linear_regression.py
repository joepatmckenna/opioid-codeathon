## simple linear regression

import pandas as pd
#import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')
from sklearn.linear_model import LinearRegression as LinReg

filename = 'linear_regression_data_test.csv'
df = pd.read_csv(filename)
#print(df.head)
#print(df.shape)

# Create variable x and respose y
x = df['Variable1']
x = x.reshape(-1,1)

print(x)
y = df['Response1']
print(y)

# Linear Regression
reg = LinReg()
reg.fit(x,y)
print('Accuracy:' + str(reg.score(x,y)))

# coefficients
m = reg.coef_[0]
print(reg.coef_[0])
# intercept
b = reg.intercept_
print(reg.intercept_)

#plot
y_preds = reg.predict(x)
plt.figure(figsize=(15,5))
plt.title('Simple Linear Regression')
plt.scatter(x, y, color = 'b')
plt.plot(x, y_preds, color='r')
plt.xlabel('Variable 1')
plt.ylabel('Response 1')
plt.savefig('simple regression.png')
plt.show()


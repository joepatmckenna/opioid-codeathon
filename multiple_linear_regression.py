## multiple linear regression

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')
from sklearn.linear_model import LinearRegression as LinReg

filename = 'linear_regression_data_test.csv'
df = pd.read_csv(filename)

x = df[["Variable1", "Variable2", "Variable3", "Variable4"]]
print(x)

y = df['Response1']
print(y)

# Linear Regression
reg = LinReg()
reg.fit(x,y)
print('Accuracy:' + str(reg.score(x,y)))

# coefficients
#m = reg.coef_[:]
print(reg.coef_[:])
# intercept
b = reg.intercept_
print(reg.intercept_)

#plot
t = np.arange(y.min(),y.max(), 0.2)
y_preds = reg.predict(x)
plt.figure(figsize=(15,10))
plt.xlim(y.min()+1,y.max()+1)
plt.ylim(y_preds.min()+1,y_preds.max()+1)
plt.title('Multiple Linear Regression')
plt.scatter(y, y_preds , color = 'b')
plt.plot(t,t, color='r')
plt.xlabel('Actual')
plt.ylabel('Predict')
plt.savefig('Multiple regression.png')
plt.show()


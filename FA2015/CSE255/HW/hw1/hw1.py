
# coding: utf-8

# In[1]:

import numpy as np


# In[2]:

import urllib


# In[3]:

import scipy.optimize


# In[4]:

import random
from sklearn import datasets, linear_model


# In[5]:

def parseData(fname):
  for l in urllib.urlopen(fname):
    yield eval(l)


# In[6]:

print "Reading data..."
data = list(parseData("file:///Users/YW/Dropbox/UCSD/FA2015/CSE255/HW/hw1/beer_50000.json"))
print "done"


# In[7]:

def feature(datum):
  feat = [1]
  feat.append(datum['beer/ABV'])
  return feat


# In[8]:

X = [feature(d) for d in data]


# In[9]:

y = [d['review/taste'] for d in data]


# In[10]:

theta, residuals, rank, s = np.linalg.lstsq(X, y)


# In[11]:

print 'Theta0:%s, Theta1:%s'%(theta[0], theta[1])


# In[90]:

X1 = np.matrix(X)
y1 = np.matrix(y)
print np.linalg.inv(X1.T * X1) * X1.T * y1.T


# In[91]:

def feature5(datum):
    feat = [1]
    feat.append(datum['beer/ABV'])
    feat.append(datum['beer/ABV']**2)
    feat.append(datum['beer/ABV']**3)
    feat.append(datum['beer/ABV']**3)
    feat.append(datum['beer/ABV']**4)
    feat.append(datum['beer/ABV']**5)
    return feat


# In[92]:

X5 = [feature5(d) for d in data]


# In[93]:

y5 = [d['review/taste'] for d in data]


# In[94]:

theta, residuals, rank, s = np.linalg.lstsq(X5, y5)


# In[95]:

print theta, residuals, rank, s


# In[96]:

regr = linear_model.LinearRegression(fit_intercept=False)


# In[97]:

regr.fit(X5, y5)


# In[98]:

print 'Coefficients:%s\n'%regr.coef_ 


# In[101]:

print 'Residual sum of squares: %.2f' % np.mean((regr.predict(X5) - y5) ** 2)


# In[102]:

train = data[:25000]
test = data[0:25000]


# In[133]:

def features(datum, degree):
    feat = [1]
    for i in xrange(1, degree+1):
        feat.append(datum['beer/ABV']**i)
    return feat


# In[134]:

lastTestingError = 0


# In[135]:

deg = 1


# In[136]:

while True:
    regr = linear_model.LinearRegression(fit_intercept=False)
    X = [features(d, deg) for d in train]
    y = [d['review/taste'] for d in train]
    X_test = [features(d, deg) for d in test]
    y_test = [d['review/taste'] for d in test]
    regr.fit(X, y)
    thisTestingError = np.mean((regr.predict(X_test) - y_test) ** 2)
    if np.fabs(thisTestingError-lastTestingError) < 0.0000001:
        break
    deg = deg + 1
    lastTestingError = thisTestingError


# In[137]:

print regr.coef_


# In[138]:

print lastTestingError
print thisTestingError


# In[ ]:




# In[ ]:




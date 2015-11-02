import random
import math
import pylab
import matplotlib.ticker as ticker

#Calculate the posterior probability according to function f
def posterior(Z, B, alpha):
	fB = 0
	for i in xrange(10):
		fB = fB + (2**i)*B[i]
	#print fB
	return (1.0-alpha)*(alpha**math.fabs(Z-fB))/(1.0+alpha)

#A random sample
def sample(N):
	numerator = 0
	denominator = 0
	for i in xrange(N):
		B = []
		for j in xrange(10):
			B.append(random.randint(0, 1))

		postProb = posterior(64, B, 0.35)
		#print postProb
		if B[6]==1:
			numerator = numerator + postProb
		denominator = denominator + postProb
	return numerator/denominator

index = []
samples = []
#Generate more samples
for i in xrange(1000, 1000000, 1000):
	print i
	index.append(i)
	samples.append(sample(i))

#print last 10 probabilities, convergence on a value
print samples[-10:]

#Plot the probabilities as the function of N
pylab.figure()
ax = pylab.gca()
ax.yaxis.set_major_locator(ticker.MultipleLocator(0.05))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.01))
ax.yaxis.grid(True, which='minor')
ax.yaxis.set_ticks_position('both')
plt = pylab.plot(index, samples)
pylab.ylabel('Probabilities')
pylab.xlabel('The sample size')
pylab.show()

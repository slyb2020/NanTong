import numpy
a = numpy.array([7,6,5,4,3])
ap = [1,3,5,7,9]
b=a.argsort()
print("a,b=",a,b)
b = numpy.argsort(a)
print('a,b=',a,b)


a = numpy.array([5,4,3,2,1,0])
b = numpy.array([1,2,3,4,5,6])
c = list(b[a])
print("c=",c)
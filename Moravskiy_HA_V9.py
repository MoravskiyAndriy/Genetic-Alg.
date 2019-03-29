import numpy as np
from scipy.linalg import norm
import math
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.tri as mtri


k=3 # з формули- визначає кількість виділених бітів
iterations=150 # кількість ітерацій

#ab=[[-2,2],[-7,-2],[5,10]] #задані відрізки на яких мінімізуємо функцію

ab=[[-1,3],[0,5]]

mi=[]

def getLenght(N): #знаходимо кількість бітів, які треба виділити
    counter=1
    c=2
    while (c<N):
        c=c*2
        counter=counter+1
    return counter

for i in ab:
    mi.append(getLenght((i[1]-i[0])*(10**k)))
    
m=0 # загальна довжина індивіда
for i in mi:
    m=m+i

    
def getX(biteval): # розділити двійковий індивід на окремі значення Х
    x=[]
    startpose=0
    endpose=mi[0]
    for i in range(len(mi)):
        temp=[]
        for j in range(startpose,endpose):
            temp.append(biteval[0][j])
        x.append(toDecimal(temp,mi[i]))
        if(i==len(mi)-1):
            break
        startpose=startpose+mi[i]
        endpose=endpose+mi[i+1]
    return x

def f1(x):
    return x[0]**2-2*x[1]**2-x[0]*x[1]+2*x[0]-x[1]+1

def f2(x):
    return 2*x[0]**2-x[1]**2+x[0]*x[1]+3*x[1]-5

def function(x): # задана функція (рез. мінімізації (1,1))
    return (abs(f1(x))+abs(f2(x)))


def toDecimal(n,lenght): #перевести двійковий індивід в десяткове число
    nb=list(n)
    nb.reverse()
    numb=0
    for i in range(0,lenght):
        numb=numb+2**i*int(nb[i])
    return numb

def getIndividuals(n,lenght): #згенерувати випадкових індивідів
    lenght=lenght*len(ab)
    population=[]
    for i in range(n):
        temp=np.random.choice([0,1],lenght)
        population.append([temp,5])
    return population

def toAB(numbers): # перевести результат на відрізок
    x=[]
    for i in range(len(mi)):
        a=ab[i][0]
        b=ab[i][1]
        k=mi[i]
        x.append(a+numbers[i]*((b-a)/(2**mi[i]-1)))
    #return (abs(a-b)/((2**k)-1))*number-1
    return x

def Main(indiv=100,p=0):
    mas=getIndividuals(indiv,m)
    minimum=1000000000000000

    counter=0
    prevmin=10000000
    #p=0.3 #2...7
    for generation in range(iterations):
        newlenght=int((len(mas)*(1+p)))
        mas1=[]
        for i in mas:
            if (i[1]>0):
                mas1.append(i)
        if(len(mas1)<5):
            #print('Less then 5!')
            break
        pi=[] # масив ймовірностей (чим краще наближення, тим більше число, тим більший шанс потрапляння
        #випадкового значення в його інтервал
        newmas1=[]
        #print('generation', generation+1)
        #print(len(mas))
        #print(len(mas1))
        #print(mas1[0])

        #знаходимо max значення f по всіх індивідах, рахуємо eval() і розраховуємо ймовірності
        maxF=function(toAB(getX(mas1[0])))
        for i in range(int(len(mas1))):
            if (function(toAB(getX(mas1[i])))>maxF):
                maxF=function(toAB(getX(mas1[i])))
                
        minF=function(toAB(getX(mas1[0])))
        for i in range(int(len(mas1))):
            if (function(toAB(getX(mas1[i])))<minF):
                minF=function(toAB(getX(mas1[i])))
        avgF=0
        for i in range(int(len(mas1))):
            avgF=avgF+function(toAB(getX(mas1[i])))
        avgF=avgF/len(mas1)
        MinLT=2
        MaxLT=7
        eta=0.5*(MaxLT-MinLT)
        prevLT=1000
                
        Ft=0
        for k in range(int(len(mas1))):
            Ft=Ft-function(toAB(getX(mas1[k])))+maxF

        for s in range(int(len(mas1))):
            pi.append((-function(toAB(getX(mas1[s])))+maxF)/Ft)

        newlenght=newlenght-(len(mas)-len(mas1))
        #print('newlenght: ',newlenght)

        for i in mas1:
            i[1]=i[1]-1
        
        # вибір батьків
        #print('len(pi): ',len(pi))
        #print('sum: ',sum(pi))
        for v in range(newlenght):
            rv1=np.random.uniform(0.0+0.01, 1.0)
            rv2=np.random.uniform(0.0+0.01, 1.0)
            it1=-1
            iterator1=0
            #print('rv1: ',rv1)
            while(iterator1<=rv1):
                iterator1=iterator1+pi[it1]
                it1=it1+1
            it2=-1
            iterator2=0
            while(iterator2<=rv2-(1-sum(pi))):
                iterator2=iterator2+pi[it2]
                it2=it2+1

            #print('i1: ',it1)
            goodparent1=mas1[it1][0]
            gp1LT=mas1[it1][1]
            goodparent2=mas1[it2][0]
            gp2LT=mas1[it2][1]

            child1=[]

            # схрещення і мутація
            temp=[]
            if(np.random.randint(0,99)>10):
                pos=int(np.random.randint(0,int(len(goodparent1))))
            
                for el in range(0,pos):
                    temp.append(goodparent1[el])
                for e2 in range(pos,int(len(goodparent1))):
                    temp.append(goodparent2[e2])
            else:
                if(np.random.randint(0,1)==0):
                    for el in range(0,int(len(goodparent1))):
                        temp.append(goodparent1[el])
                        prevLT=gp1LT
                if(np.random.randint(0,1)==1):
                    for el in range(0,int(len(goodparent2))):
                        temp.append(goodparent2[el])
                        prevLT=gp2LT
                        
            
            
            if(np.random.randint(0,99)>50):
                position=np.random.randint(0,len(temp))
                if(temp[position]==0):
                    temp[position]=1
                else:
                    temp[position]=0
            temp=np.array(temp)
            child1.append(temp)

            if(avgF>=(function(toAB(getX(child1)))+maxF)):
                lt=MinLT+eta*((function(toAB(getX(child1)))-abs(minF))/(abs(maxF)-abs(minF)))
            else:
                lt=0.5*(MinLT+MaxLT)+eta*((function(toAB(getX(child1)))-abs(minF))/(abs(maxF)-abs(minF)))

            lt=int(lt)
            if(prevLT!=1000):
                lt=prevLT
            child1.append(lt)
            
            newmas1.append(child1)

        mas=newmas1
        # моніторинг кращого у вибірці значення
        localmin=1000000000
        for i in newmas1:
            if(function(toAB(getX(i)))<minimum):
                minimum=function(toAB(getX(i)))
                element=i
                gener=generation
            if(function(toAB(getX(i)))<localmin):
                localmin=function(toAB(getX(i)))
        #print('prevmin',prevmin)
        #print('localmin',localmin)
        #print('len: ',len(mas))
        if (prevmin>localmin):
            #print('better')
            prevmin=localmin
            counter=0
            minimum_val=1000000000
            for j in newmas1:
                if(function(toAB(getX(j)))<minimum_val):
                    minimum_val=function(toAB(getX(j)))
                    minelem=j
                    min_iter=generation
        else:
            counter=counter+1
        #print(localmin)
        #print()
        if (counter>49):
            break

                    


    #print()

    # результати найкращої і останньої ітерацій

    lastmin=function(toAB(getX(mas[0])))
    lastelem=mas[0]
    for i in mas:
        #print(function(toAB(toDecimal(i,len(i)),N)))
        if(function(toAB(getX(i)))<lastmin):
            lastmin=function(toAB(getX(i)))
            lastelem=i

    '''
    print("для найкращої ітераціЇ: номер, абсолютна похибка мінімізації, двійковий індивід, значення невідомих:" )
    print(gener)
    print(minimum)
    print(element)
    print(toAB(getX(element)))
    print()
    print("для останньої ітераціЇ: номер, абсолютна похибка мінімізації, двійковий індивід, значення невідомих:" )
    print(lastmin)
    print(lastelem)
    print(toAB(getX(lastelem)))
    '''
    #print("для найкращої ітераціЇ: номер, абсолютна похибка мінімізації, двійковий індивід, значення невідомих:" )
    #print(min_iter+1)
    #print(minimum_val)
    #print(minelem)
    #print(toAB(getX(minelem)))
    return [min_iter+1,p]



dots=[]
for i in range(15):
    a,b=Main(150,0.1+(0.5/20)*i)
    print(a,b)
    dots.append([b,a])
    #plt.plot(b,a,'o',color='red')

for i in range(1,len(dots)):
    plt.plot(dots[i-1][0],dots[i-1][1],'o',color='red')
    plt.plot([dots[i-1][0],dots[i][0]],[dots[i-1][1],dots[i][1]],linestyle='solid',color='red')
plt.plot(dots[-1][0],dots[-1][1],'o',color='red')

plt.show()




#plt.plot([0,1],[0,1],linestyle='solid',color='red')
#plt.show()




























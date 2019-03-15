import numpy as np
import math


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
            temp.append(biteval[j])
        x.append(toDecimal(temp,mi[i]))
        if(i==len(mi)-1):
            break
        startpose=startpose+mi[i]
        endpose=endpose+mi[i+1]
    return x    

# приклад для лінійної задачі
'''
def f1(x):
    return x[0]+x[1]+x[2]

def f2(x):
    return 8*x[0]+4*x[1]+6*x[2]-8

def f3(x):
    return 15*x[0]+3*x[1]+5*x[2]

def function(x): # задана функція (рез. мінімізації (-1,-5,6))
    return (abs(f1(x))+abs(f2(x))+abs(f3(x)))
'''

# приклад для нелінійної задачі
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
        population.append(temp)
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

def bubble(bad_list,mas): # сортування (для попередньої програми)
    length = len(bad_list) - 1
    sorted = False

    while not sorted:
        sorted = True
        for i in range(length):
            if (bad_list[i] > bad_list[i+1]):
                sorted = False
                bad_list[i], bad_list[i+1] = bad_list[i+1], bad_list[i]
                mas[i],mas[i+1]=mas[i+1],mas[i]
    return [bad_list,mas]


mas=getIndividuals(400,m) # початкова генерація індивідів

newmas1=[]


minimum=1000000000000000

# До попередньої програми (варіант, де обираються не за ймовірностями, а 20-50% найкращих)
'''
for generation in range(iterations):
    pi=[]
    newmas1=[]
    print('generation', generation+1) 
    for i in range(int(len(mas))):
        feature1=np.random.randint(0,len(mas))
        feature2=np.random.randint(0,len(mas))
        feature3=np.random.randint(0,len(mas))
        feature4=np.random.randint(0,len(mas))
        parent1=mas[feature1]
        parent2=mas[feature2]
        parent3=mas[feature3]
        parent4=mas[feature4]

        
        if(function(toAB(getX(mas[feature1])))>=function(toAB(getX(mas[feature2])))):
            goodparent1=parent1
        else:
            goodparent1=parent2
        if(function(toAB(getX(mas[feature3])))>=function(toAB(getX(mas[feature4])))):
            goodparent2=parent3
        else:
            goodparent2=parent4
        
        child1=[]
        #child1=[]
        #child2=[]
        #for el in range(int(len(goodparent1)/2)):
        #    child1.append(goodparent1[el])
        #    child2.append(goodparent2[el])
        #for e2 in range(int(len(goodparent1)/2),int(len(goodparent1))):
        #    child1.append(goodparent2[e2])
        #    child2.append(goodparent1[e2])

        if(np.random.randint(0,99)>15):
            pos=int(np.random.randint(0,int(len(goodparent1))))
        
            for el in range(0,pos):
                child1.append(goodparent1[el])
            for e2 in range(pos,int(len(goodparent1))):
                child1.append(goodparent2[e2])
        else:
            for el in range(0,int(len(goodparent1))):
                child1.append(goodparent1[el])
        
        
        if(np.random.randint(0,99)>5):
            position=np.random.randint(0,len(child1))
            if(child1[position]==0):
                child1[position]=1
            else:
                child1[position]=0
        newmas1.append(child1)
        #newmas1.append(child2)
    #print(newmas1)
    masval=[]
    mas=[]
    for i in newmas1:
        mas.append(i)
        masval.append(function(toAB(getX(i))))
    #localminimum=1
    BestMasses=bubble(masval,mas)
    
    bm1=BestMasses[0]
    indivmass=BestMasses[1]
    
    mas=[]
    
    for i in range(int(len(indivmass)/5)):
        mas.append(indivmass[i])
        mas.append(indivmass[i])
        mas.append(indivmass[i])
        mas.append(indivmass[i])
        mas.append(indivmass[i])

        
    #for i in mas:
    #    masval.append(function(toAB(toDecimal(i,len(i)),N)))
    localmin=1000000000
    for i in mas:
        if(function(toAB(getX(i)))<minimum):
            minimum=function(toAB(getX(i)))
            element=i
            gener=generation
        if(function(toAB(getX(i)))<localmin):
            localmin=function(toAB(getX(i)))
    #print(localmin)
    print(function(toAB(getX(i))))
    print()

'''

for generation in range(iterations):
    pi=[] # масив ймовірностей (чим краще наближення, тим більше число, тим більший шанс потрапляння
    #випадкового значення в його інтервал
    newmas1=[]
    print('generation', generation+1)

    #знаходимо max значення f по всіх індивідах, рахуємо eval() і розраховуємо ймовірності

    maxF=function(toAB(getX(mas[0])))
    for i in range(int(len(mas))):
        if (function(toAB(getX(mas[i])))>maxF):
            maxF=function(toAB(getX(mas[i])))
    Ft=0
    for k in range(int(len(mas))):
        Ft=Ft-function(toAB(getX(mas[k])))+maxF

    for s in range(int(len(mas))):
        pi.append((-function(toAB(getX(mas[s])))+maxF)/Ft)

    # вибір батьків

    for v in range(int(len(mas))):
        rv1=np.random.uniform(0.0, 1.0)
        rv2=np.random.uniform(0.0, 1.0)
        i1=0
        iterator1=0
        while(iterator1<=rv1):
            iterator1=iterator1+pi[i]
            i1=i1+1
        i2=0
        iterator2=0
        while(iterator2<=rv2):
            iterator2=iterator2+pi[i]
            i2=i2+1
        goodparent1=mas[i1]
        goodparent2=mas[i2]

        child1=[]

        # схрещення і мутація

        if(np.random.randint(0,99)>50):
            pos=int(np.random.randint(0,int(len(goodparent1))))
        
            for el in range(0,pos):
                child1.append(goodparent1[el])
            for e2 in range(pos,int(len(goodparent1))):
                child1.append(goodparent2[e2])
        else:
            if(np.random.randint(0,1)==0):
                for el in range(0,int(len(goodparent1))):
                    child1.append(goodparent1[el])
            if(np.random.randint(0,1)==1):
                for el in range(0,int(len(goodparent2))):
                    child1.append(goodparent2[el])
        
        
        if(np.random.randint(0,99)>50):
            position=np.random.randint(0,len(child1))
            if(child1[position]==0):
                child1[position]=1
            else:
                child1[position]=0
        newmas1.append(child1)

    # моніторинг кращого у вибірці значення
    localmin=1000000000
    for i in newmas1:
        if(function(toAB(getX(i)))<minimum):
            minimum=function(toAB(getX(i)))
            element=i
            gener=generation
        if(function(toAB(getX(i)))<localmin):
            localmin=function(toAB(getX(i)))
    print(localmin)
    print()

                


print()

# результати найкращої і останньої ітерацій

lastmin=function(toAB(getX(mas[0])))
lastelem=mas[0]
for i in mas:
    #print(function(toAB(toDecimal(i,len(i)),N)))
    if(function(toAB(getX(i)))<lastmin):
        lastmin=function(toAB(getX(i)))
        lastelem=i

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

# Іноді точність дуже хороша, іноді трошки погана... Якщо збільшити ймовірність мутації, то,
# загалом, при достатній кількості ітерацій, вивистрибує, переважно, з тих локальних мінімумів.
# Можливо, справді, раціональніше представляти невідомі як окремі індивіди і окремо їх схрещувати,
# при поточній схемі (глобальне схрещування) добре помітна певна хаотичність результатів: покращуючи
# одне значення, алгоритм схрещування іноді погіршує інше, тому помітна деяка девіація
# проміжних результатів і нестабільна збіжність. (Подібне не спостерігаєть, наприклад, у мого
# колеги Юри Вусача, котрий сепарує невідомі значення і вони схрещуються лише в межах "свого типу",
# його алгоритм, хоч і відмінний від рекомендованого, демонструє куди кращу збіжність і стабільність
# результатів на таких же прикладах).

# Зауваження: іноді, при запуску вибиває помилку "list index out of range" у
# goodparent2=mas[i2]. Не знаю, з чим це пов'язано... Вирішується кількакратним
# перезапуском (стартує на другий-третій раз).


















































# In[ ]:




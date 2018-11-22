
import pandas
from nltk import ngrams
from nltk.stem import PorterStemmer
import re
from nltk.corpus import stopwords
from sklearn import naive_bayes
from sklearn.model_selection import train_test_split,cross_val_score
from sklearn.metrics import confusion_matrix,precision_score, recall_score, f1_score

colnames = ['url','name','review','state','dishnames']
data = pandas.read_csv('Path to Restaurant Reviews Data Labelled.csv', names=colnames)

url = data.url.tolist()
name = data.name.tolist()
review = data.review.tolist()
state = data.state.tolist()
dishnames = data.dishnames.tolist()
review_unstemmed=review[:]

#Data Stemming
porter = PorterStemmer()

#Removing stop words
for h in range(len(review)):
    f=review[h]
    f=re.sub(r'[?|$|.|!|,|\'|"|+|-|_|\(|\)|*|\^|#|@|~|`|/|;|:|<|>|-]',r'', f )
    f=f.lower()
    review[h]=' '.join([porter.stem(word) for word in f.split() if word not in (stopwords.words('english'))])

#print review

for h in range(len(review_unstemmed)):
    f=review_unstemmed[h]
    f=re.sub(r'[?|$|.|!|,|\'|"|+|-|_|\(|\)|*|\^|#|@|~|`|/|;|:|<|>|-]',r'', f )
    f=f.lower()
    review_unstemmed[h]=' '.join([word for word in f.split() if word not in (stopwords.words('english'))])

#Creating "dish names" list
dishnames_list=[]
for i in range(len(dishnames)):
        dishnames[i]=dishnames[i].lower()
        a=dishnames[i].split(",")
        for j in range(len(a)):
            dishnames_list.append(a[j].strip())

dishnames_list = list(set(dishnames_list))
dishnames_list.remove('none')

review_poniter=[]
i=0
review_poniter.append(i)
while i < len(name)-2:
    while name[i] == name[i+1]:
        if i+1<len(name)-1:
            i=i+1
        if i+1==len(name)-1:
            break
    review_poniter.append(i+1)
    i=i+1
review_poniter[-1]=review_poniter[-1]+1

#Converting text data into features using Word Tri-gram model
n=3
trigrams_list = []
for e in range(len(review)):
    b=review[e]
    trigram = ngrams(b.split(), n)
    for grams in trigram:
        s=grams[0]+" "+grams[1]+" "+grams[2]
        trigrams_list.append(s)

trigrams_list = list(set(trigrams_list))

#Creating Term-Document Matrix from features
termdoc=[[0 for p in range(len(trigrams_list))] for q in range(len(review))] 

for e in range(len(review)):
    b=review[e]
    trigrams=[]
    trigram = ngrams(b.split(), n)
    for grams in trigram:
        s=grams[0]+" "+grams[1]+" "+grams[2]
        trigrams.append(s)
    for a in range(len(trigrams_list)):
        sum=0
        for d in range(len(trigrams)):
            if trigrams[d] == trigrams_list[a]:
                sum=sum+1
                
        termdoc[e][a]=sum

#Positive and Negative state of reviews
#+ve is 1, -ve is 2
for f in range(len(state)):
    if state[f] == "positive":
        state[f]=1
    elif state[f] == "negative":
        state[f]=2

#Splitting data into training and testing datasets
train_x,test_x,train_y,test_y = train_test_split(termdoc,state,test_size=0.3)

#Using Naive Bayes Algorithm
nbc = naive_bayes.BernoulliNB()
nbc_scores = cross_val_score(nbc,termdoc,state,cv=10)
print 'Naive Bayes mean accuracy : %.2f'%(nbc_scores.mean())
print 'Naive Bayes std : %.2f'%(nbc_scores.std())

nbc.fit(train_x,train_y)
predict_train_y = nbc.predict(train_x)
predict_test_y = nbc.predict(test_x)
print "Confusion Matrix:"
print confusion_matrix(test_y,predict_test_y)

print 'Precision score is : %.2f'%(precision_score(test_y, predict_test_y))
print 'Recall Score is : %.2f'%(recall_score(test_y, predict_test_y))
print 'F score is : %.2f'%(f1_score(test_y, predict_test_y))

#Predicting the review states
predicted_all = nbc.predict(termdoc)

counter_dish=[0 for q in range(len(dishnames_list))]

#Predicting the best dish based on positive and negative reviews
for i in range(len(review_poniter)-1):
    for j in range(review_poniter[i],review_poniter[i+1]):
            if predicted_all[j] == 1:
                for k in range(len(dishnames_list)):
                    if dishnames_list[k] in review_unstemmed[j]:
                        counter_dish[k]=counter_dish[k]+1
                
    index=counter_dish.index(max(counter_dish))
    print "The best dish of "+name[j]+" is "+dishnames_list[index]


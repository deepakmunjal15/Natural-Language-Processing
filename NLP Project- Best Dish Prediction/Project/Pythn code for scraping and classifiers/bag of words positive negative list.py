import pandas
from nltk.stem import PorterStemmer
import re
from nltk.corpus import stopwords

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

for h in range(len(review_unstemmed)):
    f=review_unstemmed[h]
    f=re.sub(r'[?|$|.|!|,|\'|"|+|-|_|\(|\)|*|\^|#|@|~|`|/|;|:|<|>|-]',r'', f )
    f=f.lower()
    review_unstemmed[h]=' '.join([word for word in f.split() if word not in (stopwords.words('english'))])

#Using the list of positive and negative words to categorize reviews
negative_word=[]
positive_word=[]
positive_word_count=0.0
negative_word_count=0.0
final_score_normalized=[]

with open('Path to negative words.txt','r') as negative:
    for line in negative:
        for word in line.split():
           word=word.lower()
           word=porter.stem(word)
           negative_word.append(word)

with open('Path to positive words.txt','r') as positive:
    for line in positive:
        for word in line.split():
           word=word.lower()
           word=porter.stem(word)
           positive_word.append(word)


for e in range(len(review)):
    word_List_review = re.sub("[^\w]", " ",  review[e]).split()
    for r in range(len(word_List_review)):
        for t in range(len(positive_word)):
            if word_List_review[r]==positive_word[t]:
                positive_word_count=positive_word_count+1
                break
        for y in range(len(negative_word)):
            if word_List_review[r]==negative_word[y]:
                negative_word_count=negative_word_count-1
                break

    final_score_normalized.append(float((positive_word_count+negative_word_count)/(positive_word_count-negative_word_count)))

#Positive and Negative state of reviews
#+ve is 1, -ve is 2
for f in range(len(state)):
    if state[f] == "positive":
        state[f]=1
    elif state[f] == "negative":
        state[f]=2

correct=0
incorrect=0
for e in range(len(state)):
    if state[e] == 1 and final_score_normalized>=0:
        correct=correct+1
    elif state[e] == 2 and final_score_normalized<0:
        correct=correct+1
    else:
        incorrect=incorrect+1

accuracy=float(correct)/float(correct+incorrect)
print 'accuracy is : %.2f'%(accuracy)

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


counter_dish=[0 for q in range(len(dishnames_list))]

#Predicting the best dish based on positive and negative reviews
for i in range(len(review_poniter)-1):
    for j in range(review_poniter[i],review_poniter[i+1]):
            if final_score_normalized[j] >=0:
                for k in range(len(dishnames_list)):
                    if dishnames_list[k] in review_unstemmed[j]:
                        counter_dish[k]=counter_dish[k]+1
                        
    index=counter_dish.index(max(counter_dish))
    print "The best dish of "+name[j]+" is "+dishnames_list[index]


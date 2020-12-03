from collections import Counter  # gia thn xrhsh counter emfaniseon
import os  # gia diaxeirish directories
import math  # gia thn praxh ths rizas
import string  # gia thn afairesh stixhs


# voithitikes synarthshs gia ypologismo cos similarity

def dot_product(x, y):
    dot_product = 0
    for i, j in zip(x, y):  # h zip dhmiourgei lista me pairs ton diadoxikon stoixeion stis dyo listes
        dot_product += i * j
    return dot_product


def cos_sim_percent(x, y):
    cos_sim = dot_product(x, y) / math.sqrt((dot_product(x, x) * dot_product(y, y)))
    return round(cos_sim * 100)


# import ta files

files_num = 0
folder = "docs"
file_names = os.listdir(folder)  # epistrefei ta onomata olon ton files ston fakelo
file_paths = [os.path.join(folder, file) for file in file_names]  # apothikevoume ta paths olon ton files tou fakelou dhmiourgontas path me systatika to onoma tou fakelou kai to onoma arxeiou
files_list = []
for file in file_paths:
    files_list.append(open(file, 'r'))

print('Welcome to the Text Comparator Tool!')
print("Choose number of files to read (", len(file_names), "found ) :")

files_num = int(input())

while not (files_num <= len(file_names) and files_num>1):
    print("Please choose a number more than 1 and less than or equal to", len(file_names), ":")
    files_num = int(input())


# apothikefsh docs se listes

doc_list = []  # emfolevmeni lista pou periexei tis listes olon ton (non unique) lexeon se kathe document
for i in range(0, files_num):  # gia kathe doc
    doc_list.append([])  # ftiakse lista lexeon

for i in range(0, files_num):
    for line in files_list[i]:
        for word in line.split():

            word = word.translate(str.maketrans({symbol: "" for symbol in string.punctuation}))  # afairesh stikshs
            # dhmioyrghsame translation table pou metafrazei kathe "symbol" tou "string.punctuation" sto "word" se None
            # valame to table ayto san orisma sthn translate h opoia efarmozetai sto "word" kai apothikevetai sto "word"

            doc_list[i].append(word.lower())  # vazei kathe lexh (lower case) tou document sthn lista


# dhmiourgia counter objects

counter_list = []  # dhmiourgia listas me counters gia kathe document
for i in range(0, files_num):
    counter_list.append(Counter(doc_list[i]))  # arxikopoihsh counters me to doc_list pou antistoixei ston kathena


# dhmiourgia listas me oles tis unique lexeis se ola ta documents

all_words = []
for doc in doc_list:
    all_words += doc
all_words = list(set(all_words))  # krata mono ta unique words
all_words.sort()  # kai taxinomise ta (gia logous omorfias)


# apothikefsh emfaniseon lexeon se kathe document

occurences_list = []  # emfolevmeni lista tou noumerou ton emfaniseon kathe lexis apo to all_words gia kathe document
for i in range(0, files_num):  # gia kathe document
    occurences_list.append([])  # dhmiourgia neas listas ton emfaniseon ton lexeon
    for word in all_words:  # gia kathe lexh
        occurences_list[i].append(counter_list[i][word])  # apothikefsh noumerou emfaniseon ths lexis "word" sto "doc_list[i]" to opoio ypologizei o counter "counter_list[i]" opos arxikopoihsame parapano


# ypologismos omoiothtas gia kathe zevgari documents

pairs_similarity = []
for i in range(0, files_num):
    for j in range(i, files_num):  # ksekinaei apo i gia thn apofygh anestramenon pairs p.x. [1,2] == [2,1]
        if i != j:
            pair = (i, j)
            similarity = cos_sim_percent(occurences_list[i], occurences_list[j])  # occurences_list[i],occurences_list[j] ta dianysmata tou plithous emfaniseon lexeon
            pairs_similarity.append((pair, similarity))


# taxinomisi listas

pairs_similarity.sort(key=lambda pairs_similarity: pairs_similarity[1], reverse=True)  # taxinomisi se fthinousa seira me vasi to kleidi pou epistrefei h lambda synarthsh (dld to deftero pedio twn tuples, to pososto "similarity")


# ektyposh apotelesmaton

restart = True

while restart is not False:  # den theloume na vgei sthn periptosi pou kapoios katalathos den grapsei oute True oute False, oste na thn xeiristoyme katallhla
    print("Enter the number of the most similar pairs of documents you want to see ( maximum", len(pairs_similarity), ") :")
    k_most_similar = int(input())

    while not (k_most_similar <= len(pairs_similarity) and k_most_similar>0):  # an to k den einai sta oria ksanadose allo
        print("Please enter a positive number less than or equal to", len(pairs_similarity), ":")
        k_most_similar = int(input())

    for i in range(0, k_most_similar):  # apotelesmata
        document1 = pairs_similarity[i][0][0]
        document2 = pairs_similarity[i][0][1]
        similarity = pairs_similarity[i][1]
        print('{:<10}{:<25}{:<5}{:<25}{:<5}{:<3}{:<10}'.format("Documents", file_names[document1], "and", file_names[document2], "are", similarity, "% the same"))  # formatted morfh se steiles me orismenh apostash(10,20,..ktl)

    while True:  # leitourgia reset pou ekteleitai gia pada kai stamataei mono otan kapoios dosei me sosto tropo apanthsh mono "True" h "False"
        answer = input("Reprint results? True or False :\n")
        if answer == "True":
            restart = True
            break
        elif answer == "False":
            restart = False
            break

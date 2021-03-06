import math, os, glob, operator, csv
import Common

root, tests, _, trainSetId, _, resultFolder = Common.getNewFileInfo()
dataSet = Common.dataSet
token_c = Common.token_c
txt_c = Common.txt_c

def findJaccardSim(doc1,doc2):
    intersection = set(doc1).intersection(set(doc2))
    union = set(doc1).union(set(doc2))
    return len(intersection)/(len(union)-len(intersection))

def findCosineSim(docVec1,docVec2):
    num = 0
    deno1 = 0
    deno2 = 0
    for i in range(0,len(docVec1)):
        num += docVec1[i]*docVec2[i]
        deno1 += docVec1[i]*docVec1[i]
        deno2 += docVec2[i]*docVec2[i]
    
    similarity = num / (math.sqrt(deno1*deno2))
    return similarity

def freqVector(doc, wordlist):
    return [doc.count(word) for word in wordlist]

def tfidfVector(doc, wordlist):
    vec = []
    
    root, _, trainSet, _, _, _ = Common.getNewFileInfo()
    file = 'idf.txt'
    idf = Common.readToType(os.path.join(root,trainSet,file))
    tf = Common.calculateTF(doc)
        
    for word in wordlist:
        if word in tf.keys() and word in idf.keys():           
            vec_value = tf[word]*idf[word]
            vec.append(vec_value)   
        else: 
            vec.append(0)
                
    return vec
    

def cosineSimilarity(doc1, doc2):    
    
    wordlist = set(doc1)|set(doc2) 
     
    docVec11 = freqVector(doc1, wordlist)  
    docVec12 = freqVector(doc2, wordlist)
    cosineSim1=findCosineSim(docVec11, docVec12)
    '''
    docVec21 = tfidfVector(doc1, wordlist)    
    docVec22 = tfidfVector(doc2, wordlist)     
    cosineSim2=findCosineSim(docVec21, docVec22)
    '''
    return cosineSim1


def main():
    
    print("Finding similar files . . .")
    #top_sentences_tfidf = Common.readToType(os.path.join(root,tests,trainSetId,resultFolder,'ts_tfidf.txt'))
    #top_sentences_fcfound = Common.readToType(os.path.join(root,tests,trainSetId,resultFolder,'ts_fcfound.txt'))
    top_sentences_both = Common.readToType(os.path.join(root,tests,trainSetId,resultFolder,'ts_both.txt'))
    
    cosineSimList = {}
    jaccardSimList = {}    
    path = os.path.join(root,dataSet,token_c,'*.txt')
    
    for file in glob.glob(path):
        catchphrases = Common.readToType(file)
        
        doc1 = Common.flattenList(top_sentences_both) 
        doc2 = Common.flattenList(catchphrases)
        
        freqCosineSim = cosineSimilarity(doc1, doc2)
        jaccardSim = findJaccardSim(doc1, doc2)
        
        cosineSimList[Common.getFileName(file)] = freqCosineSim*100
        jaccardSimList[Common.getFileName(file)] = jaccardSim*100
        
    sortedCosine = sorted(cosineSimList.items(), key=operator.itemgetter(1))
    sortedJaccard = sorted(jaccardSimList.items(), key=operator.itemgetter(1))
     
    with open(os.path.join(root, tests, trainSetId, resultFolder, 'SimilarFiles.csv'), 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['FileName', 'FreqCosineSim', '', 'FileName', 'JaccardSim'])
        for i in range(1,6):
            filewriter.writerow([sortedCosine[-i][0], sortedCosine[-i][1], '', sortedJaccard[-i][0], sortedJaccard[-i][1]])


if __name__ == "__main__":
    main()
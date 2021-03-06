'''
This program runs for every new file to process using a processed trainset
Intended to: 
Parse XML to text
Parse text to tokens
Use vocabulary scores calculated in preprocessing phase to score sentences and find best candidates for catchphrases
'''

import os, datetime
import numpy
import Common

root, tests, trainSet, trainSetId, testFileId, resultFolder = Common.getNewFileInfo()
baseTestPath = os.path.join(root,tests,trainSetId,resultFolder)

'''
Input: sTokenized - nested list of sentences tokens in the file
       fcfound - dictionary of word:score for all words in corpus
       qty - # of sentences to be chosen as catchphrases. Depends on actual # of catchphrases present in the file
Returns: list of length qty of tokenized sentences with highest scores
'''
def fcfoundScoring(sTokenized,fcfound,qty):
    #print("\nIn using_fcfound")
    
    score = []
    top_sentences = [] 
    
    for sentence in sTokenized:
        sentence_score = 0
        number_of_terms = 0
        for term in sentence:
            number_of_terms+=1
            term_score = fcfound.get(term)
            if(term_score is None):
                term_score = 0.0;
            sentence_score+=term_score
        if number_of_terms==0:
            sentence_score = 0
        else:
            sentence_score = sentence_score/number_of_terms
        score.append(sentence_score)                                       #one-to-one correspondence between text list and score list
            
    index_top_sentence = (numpy.argsort(score)[::-1][:qty]).tolist()         #Get indices of the top scores
    for number in index_top_sentence:
        top_sentences.append(sTokenized[number])     
     
    return top_sentences

'''
Input: sTokenized - nested list of sentences tokens in the file
       idf - dictionary of word:score for all words in corpus
       qty - # of sentences to be chosen as catchphrases. Depends on actual # of catchphrases present in the file
Returns: list of length qty of tokenized sentences with highest scores
'''
def tfidfScoring(sTokenized,idf,qty):
    #print("\nIn using_tfidf")
    score = []
    top_sentences = []   
    tf = Common.calculateTF(sTokenized)
    
    for sentence in sTokenized:
        sentence_score = 0
        number_of_terms = 0
        for term in sentence:
            number_of_terms+=1
            if term not in idf.keys():
                term_score = 0
            else:
                term_score = tf[term]*idf[term]    
            sentence_score+=term_score
        if number_of_terms==0:
            sentence_score = 0
        else:
            sentence_score = sentence_score/number_of_terms
        score.append(sentence_score)  
    
    index_top_sentence = (numpy.argsort(score)[::-1][:qty]).tolist()         #Get indices of the top scores
    for number in index_top_sentence:
        top_sentences.append(sTokenized[number])      
    return top_sentences

'''
Input: sTokenized - nested list of sentences tokens in the file
       idf - dictionary of word:score for all words in corpus
       qty - # of sentences to be chosen as catchphrases. Depends on actual # of catchphrases present in the file
Returns: list of length qty of tokenized sentences with highest scores
'''
def doubleScoring(sTokenized,fcfound,idf,qty):
    #print("\nIn using_tfidf")
    score = []
    top_sentences = []   
    tf = Common.calculateTF(sTokenized)
    
    for sentence in sTokenized:
        sentence_score = 0
        number_of_terms = 0
        for term in sentence:
            number_of_terms+=1
            if term not in idf.keys():
                term_score = 0
            else:
                term_score = fcfound.get(term) + (tf[term]*idf[term])   
            sentence_score+=term_score
        if number_of_terms==0:
            sentence_score = 0
        else:
            sentence_score = sentence_score/number_of_terms
        score.append(sentence_score)  
  
    index_top_sentence = (numpy.argsort(score)[::-1][:qty]).tolist()         #Get indices of the top scores
    for number in index_top_sentence:
        top_sentences.append(sTokenized[number])      
    return top_sentences

'''
Input: No Input
Returns: tokenized sentences and catchphrases
Reads the xml file extracts the catchphrases and sentences from the file and processes the sentences and cathcphrases into tokens
'''
def processNewFile():
    print("\nProcessing new file . . .")
    
    Common.parseXmlFile(os.path.join(baseTestPath, '%s.xml' %testFileId))
    
    sTokenized = Common.parseTextFile(os.path.join(baseTestPath, 'sentences.txt'))
    Common.writeToFile(os.path.join(baseTestPath, 'sTokenized.txt'), sTokenized)    
               
    cTokenized = Common.parseTextFile(os.path.join(baseTestPath, 'catchphrases.txt'))
    Common.writeToFile(os.path.join(baseTestPath, 'cTokenized.txt'), cTokenized)
                
    return sTokenized, cTokenized
    
def main():  
    
    start_time = datetime.datetime.now()  
    #print('{:%Y-%b-%d %H:%M:%S}'.format(start_time)) 
    
    sTokenized, cTokenized = processNewFile() 
    
    qty = len(cTokenized)    
    amt = 10 if 10>qty else qty 
    
    fcfound = Common.readToType(os.path.join(root,trainSet,'fcfound.txt'))
    idf = Common.readToType(os.path.join(root,trainSet,'idf.txt')) 
        
    top_sent_fcfound = fcfoundScoring(sTokenized, fcfound, amt)
    top_sent_tfidf =  tfidfScoring(sTokenized, idf, amt) 
    top_sent_both = doubleScoring(sTokenized,fcfound,idf,amt) 
    
    Common.writeToFile(os.path.join(baseTestPath,'ts_fcfound.txt'), top_sent_fcfound) 
    Common.writeToFile(os.path.join(baseTestPath,'ts_tfidf.txt'), top_sent_tfidf)
    Common.writeToFile(os.path.join(baseTestPath,'ts_both.txt'), top_sent_both)
      
    end_time = datetime.datetime.now()    
    #print('{:%Y-%b-%d %H:%M:%S}'.format(end_time))
    
    time_taken = end_time - start_time
    print("TimeTaken: %s" %time_taken)
    
if __name__ == "__main__":
    main()
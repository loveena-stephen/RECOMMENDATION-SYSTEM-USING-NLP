'''
This program needs to run ONLY IF the train set has changed
Intended to:
parse XML to text
parse text to tokens
calculates fcfound and idf scores for the corpus vocabulary
'''

import glob, datetime, os
import Common


root, trainSet, dataSet, xml_files, txt_s, txt_c, token_s, token_c = Common.getPreprocessInfo()

'''
Input: words - set of words in corpus
       sentences - dictionary where keys are filenames and values are the words in the sentences of the corresponding file
       catchphrases - dictionary where keys are filenames and values are the words in the catchphrases of the corresponding file
       -- both have one to one correspondence among them --
Returns: fcfound - a dictionary where the keys are words and values are the scores associated with that word

fcfound(word) = # of files where word is in catchphrase 
                ---------------------------------------
                # of files where word is only in sentence
'''
def fcfoundCalculation(words, sentences, catchphrases):
    print("\nIn calculate_fcfound")
    fcfound = {}
    for word in words:
        present_C = 0
        present_onlyS = 0
        for k in catchphrases.keys():
            if word in catchphrases[k]:
                present_C += 1
            if word in sentences[k] and word not in catchphrases[k]:
                present_onlyS += 1    
        if present_onlyS == 0:
            fcfound[word] = float(present_C)
        else:
            fcfound[word] = present_C/present_onlyS
                
    return fcfound

'''
Input: words - set of words in corpus
       sentences - dictionary where keys are filenames and values are the words in the sentences of the corresponding file
       catchphrases - dictionary where keys are filenames and values are the words in the catchphrases of the corresponding file
       -- both have one to one correspondence among them --
Returns: idf - a dictionary where the keys are words and values are the scores associated with that word

idf(word) =        # of files in corpus
            ---------------------------------
            # of files that contain the word
'''
def idfCalculation(words, sentences, catchphrases):
    print("\nIn calculate_tfidf")
    idf = {}
    total_docs = len(sentences)
    for w in words:
        count = 0
        for k in sentences.keys():
            if w in sentences[k] or w in catchphrases[k]:
                count+=1
        idf[w] = total_docs/count
    return idf
        
    
'''
Input: path - to a directory containing textfiles of sentences or cathphrases
       cp - boolean value indicating if path is for catchphrases(True) or sentences(False)
Returns: tokens - dictionary where keys are the filenames and values are the list of words in corresponding file
         words - non repetitive list of words from all files i.e. "set" of all words in the corpus
'''
def processText(path, cp):
    if (cp == False):
        print("\nProcessing text for sentences")
        outputFolder = token_s
    elif (cp == True):
        print("\nProcessing text for catchphrases")
        outputFolder = token_c
        
    tokens = {}                                              #dictionary {'filename':[flat list of words in that file]}
    words = set()                                            #set of all words in corpus
                                               
    for file in glob.glob(path):
        fileName = Common.getFileName(file)
        
        file_words_nested = Common.parseTextFile(file) 
        Common.writeToFile(os.path.join(root, trainSet, outputFolder, "%s.txt" %fileName), file_words_nested)
                              
        file_words = Common.flattenList(file_words_nested)              #flatten into single list of all words in file
        
        words |= set(file_words)                     #bit wise or set union operator        
        tokens[file.split('\\')[-1]] = file_words
        
    return tokens, words

'''
Input: No input
Returns: Returns nothing
Reads the xml files and on each file, calls a method that extracts the catchphrases and sentences from the file
'''
def parseXml():    
    print("\nIn parseXml")
       
    for file in glob.glob(os.path.join(root, trainSet, xml_files, '*.xml')):
        Common.parseXmlFile(file)
    
    for file in glob.glob(os.path.join(root, dataSet, xml_files, '*.xml')):
        Common.parseXmlFile(file)

def main():
    
    Common.deleteFiles()
    
    start_time = datetime.datetime.now()  
    print('{:%Y-%b-%d %H:%M:%S}'.format(start_time))   
    
    parseXml()    
    
    path_sentences = os.path.join(root, trainSet, txt_s, '*.txt') 
    path_catchphrases = os.path.join(root, trainSet, txt_c, '*.txt')
    
    sentences, words1 = processText(path_sentences, False)
    catchphrases, words2 = processText(path_catchphrases, True)   
    
    words = words1|words2         

    fcfound = fcfoundCalculation(words, sentences, catchphrases)    
    idf = idfCalculation(words, sentences, catchphrases) 
    
    Common.writeToFile(os.path.join(root,trainSet,'fcfound.txt'),fcfound)   
    Common.writeToFile(os.path.join(root,trainSet,'idf.txt'),idf)  
    
    print("Processing text for catchphrases for similarity")
    for file in glob.glob(os.path.join(root, dataSet, txt_c, '*.txt')):
        cTokenized = Common.parseTextFile(file)
        fileName = Common.getFileName(file)
        Common.writeToFile(os.path.join(root, dataSet, token_c, "%s.txt" %fileName), cTokenized)
    
    end_time = datetime.datetime.now()    
    print('{:%Y-%b-%d %H:%M:%S}'.format(end_time))
    
    time_taken = end_time - start_time
    print("TimeTaken: %s" %time_taken)
    
if __name__ == "__main__":
    main()
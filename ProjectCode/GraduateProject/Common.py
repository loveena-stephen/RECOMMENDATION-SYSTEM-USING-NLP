'''
Contains all generic methods called in Preprocessing or Processing a new file
'''
import os, glob, re, pprint, collections
import bs4, nltk

'''
list of directory names used to create path dynamically where ever needed
Out in common to make it easy to make changes, if any
'''
root = 'C:/MySavedData/LakeheadUniversity/Project_547854/GradProject'
trainSet = 'TrainSet'
dataSet = 'DataSet'
xml_files = 'XML Files'
txt_s = 'TextSentences'
txt_c = 'TextCatchphrases'
token_s = 'TokenSentences'
token_c = 'TokenCatchphrases'

tests = 'TestResults'

#Use section with appropriate values when testing individual test file
'''
trainSetId = 'TS1'
testFileId = '06_436'
resultFolder = 'TF_'+testFileId
'''
# Use section when running BatchProcessing.py

trainSetId = ''
testFileId = ''
resultFolder = ''



'''
Input: No Input
Returns: root, trainSet, dataSet, xml_files, txt_s, txt_c, token_s, token_c
method to pass directory information to Preprocessing
'''
def getPreprocessInfo():
    return root, trainSet, dataSet, xml_files, txt_s, txt_c, token_s, token_c

'''
Input: No Input
Returns: root, trainSet, tests, testFileId, resultFolder
method to pass directory information to Processing New File
'''
def getNewFileInfo():
    return root, tests, trainSet, trainSetId, testFileId, resultFolder

'''
Input: path - complete path to a file
Returns: name_part - just the name of the file
method to extract fileName from a path to a file
'''
def getFileName(path):
    path_components = path.split("\\")        
    file_name=path_components[-1]       #Isolate file name with extension from the complete path
    name_part = file_name[:-4]
    
    return name_part

'''
Input: No input
Returns: Returns nothing
method to delete files from various folder while processing a new trainset
'''
def deleteFiles():
    
    paths = [os.path.join(root,trainSet,"*.txt"),
             os.path.join(root,trainSet,txt_c,"*.txt"),
             os.path.join(root,trainSet,txt_s,"*.txt"),
             os.path.join(root,trainSet,token_c,"*.txt"),
             os.path.join(root,trainSet,token_s,"*.txt"),
             os.path.join(root,dataSet,txt_c,"*.txt"),
             os.path.join(root,dataSet,txt_s,"*.txt"),
             os.path.join(root,dataSet,token_c,"*.txt")]
    
    for path in paths:
        if glob.glob(path):
            print("Deleting from %s" %path)
            for f in glob.glob(path):
                os.remove(f)
    
    
    
'''
Input: path - path to a file that has to be read
Returns: the contents of the file converted to list
method to read the text contents of a file that contains a list and return it as a list
'''        
def readToType(path):
    with open(path) as f:
        return eval(list(f)[0])
        
'''
Input: path - to the file
       content - text to be written in the file
Returns: None
Writes content into file specified by path
'''
def writeToFile(path, content):
    with open(path,'w', encoding='utf-8') as f_out:
        pprint.pprint(content, f_out, 1, 100000000, None)   


'''
 Input: raw_wordlist - list of unprocessed words
 Returns: List of words
 Helper function to filter out stop words and stem all words in a list
'''   
def filterWords(raw_wordlist):
    result = [nltk.stem.lancaster.LancasterStemmer().stem(word) 
            for word in raw_wordlist 
            if word.lower() not in nltk.corpus.stopwords.words('english')]
    return result

'''
Input: nested list
Returns: simple list
Takes any nested list and converts it to a simple flat list
'''
def flattenList(nested_list):
    return [item for sublist in nested_list for item in sublist]


'''
Input: file - a text file
Returns: A nested list, where each inside list is a tokenized line of the input
Tokenizes a single text file into a list of lists where each inside list is a list of word tokens
'''
def parseTextFile(file): 
    file_words_nested = [] 
                       
    fileName = getFileName(file)
    print("Parsing %s.txt" %fileName)
    
    with open(file, 'r', encoding='utf-8') as f:
        text_tokens = nltk.tokenize.sent_tokenize(f.read())         #text_tokens - list of sentences in the text
        
    for line in text_tokens:
        text_words = re.findall('[a-zA-Z]+', line)                  #text_words - list of words in sentence
        text_words_filtered = filterWords(text_words)               #filter stop words and stems  
        file_words_nested.append(text_words_filtered)               #appending filtered list to file_words
                      
    return file_words_nested


'''
Input: file - path to an xml file
Returns: Retuns nothing 
Takes one xml file and extracts sentences and catchphrases and write them into two separate text files
'''
def parseXmlFile(file):
    
    sentence_list = []
    catchphrase_list = []
    fileName = getFileName(file)
    setType = file.split("\\")[1]
    print("Parsing %s.xml" %fileName)
    
    with open(file, 'r', encoding='mbcs')as f_xml:                             
        content = f_xml.read()
        soupObj = bs4.BeautifulSoup(content,"html.parser")
        sentences_obj = soupObj.find_all('sentence') 
        catchphrases_obj = soupObj.find_all('catchphrase')
                    
        #Makes a list of all the sentences 
        for x in sentences_obj:
            sentence_list.append(x.text)   
            
        #Makes a list of all the catchphrases         
        for x in catchphrases_obj:
            catchphrase_list.append(x.text)
        
        if (setType == tests):
            path1 = os.path.join(root, tests, trainSetId, resultFolder, "sentences.txt")
            path2 = os.path.join(root, tests, trainSetId, resultFolder, "catchphrases.txt")
        else:
            path1 = os.path.join(root, setType, txt_s, "%s.txt" %fileName)
            path2 = os.path.join(root, setType, txt_c, "%s.txt" %fileName)
           
        #write each individual sentence into a text file
        with open(path1,'w', encoding='utf-8') as f_sentences:
            for x in sentences_obj:
                f_sentences.write(x.text)
                f_sentences.write("\n")
        
        #write each individual catchphrase into a text file
        with open(path2,'w', encoding='utf-8') as f_catchphrase:
            for x in catchphrases_obj:
                if(x.text[-1] != '.'):
                    f_catchphrase.write(x.text+'.')
                else:
                    f_catchphrase.write(x.text)
                f_catchphrase.write("\n")

'''
Input: text - nested list of tokens in a single document
Returns: tf - a dictionary in the form term:termfrequency for the set of words in the document
Takes a document and calculates term frequency for the wordset of the document
'''    
def calculateTF(text):
    
    tf= {}
    words_in_doc = flattenList(text) 
    
    word_count = collections.Counter(words_in_doc)
    doc_length = len(words_in_doc)
       
    terms = set(words_in_doc)
    for term in terms:
        tf[term] = word_count[term]/doc_length
    
    return tf

'''
Input: l1 - larger list
       l2 - smaller list
Returns: maxlen - length of the largest contiguous sequence in l2 contained in l1
A method to find the length of largest continuous common sequence of two lists
'''
def lccs(l1, l2):

    table = [[0 for _ in range(len(l2) + 1)] for _ in range(len(l1) + 1)]
    maxlen = 0
    lccs = []

    for i, item1 in enumerate(l1, 1):
        for j, item2 in enumerate(l2, 1):
            if item1 == item2:
                newlen = table[i - 1][j - 1] + 1
                table[i][j] = newlen
                if newlen > maxlen:
                    maxlen = newlen
                    lccs = l1[i-maxlen:i]
    return maxlen
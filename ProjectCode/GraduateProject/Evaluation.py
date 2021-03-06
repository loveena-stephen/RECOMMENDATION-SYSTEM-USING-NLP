'''
This program reads the given catchphrases of a file 
and compares it with candidate sentences chosen from the file.
There are four methods to check varying percentages of catchphrase and sentence match 
'''

import os
import Common

'''
Input: catchphrases - Given catchphrases in the file
       sentences - Sentences picked as candidate catchphrases
Output: found - number of catchphrases that were completely found in the sentences
'''
def check100(catchphrases, sentences): 
    found = 0
                
    for c in catchphrases:        
        if(c):                                  #Check if list1 is not empty
            for s in sentences:
                if (Common.lccs(s,c) == len(c)):
                    found+=1
                    break
    
                 
    return found

'''
Input: catchphrases - Given catchphrases in the file
       sentences - Sentences picked as candidate catchphrases
Output: found - number of catchphrases where more than 75% were found in the sentences
'''
def check75(catchphrases, sentences):
    
    found = 0
                
    for c in catchphrases:        
        if(c):                                  #Check if list1 is not empty
            for s in sentences:
                if (Common.lccs(s,c) >= len(c)*0.75):
                    found+=1
                    break
    
                 
    return found

'''
Input: catchphrases - Given catchphrases in the file
       sentences - Sentences picked as candidate catchphrases
Output: found - number of catchphrases where more than 50% were found in the sentences
'''
def check50(catchphrases, sentences):
    
    found = 0
                
    for c in catchphrases:        
        if(c):                                  #Check if list1 is not empty
            for s in sentences:
                if (Common.lccs(s,c) >= len(c)/2):
                    found+=1
                    break
    
                 
    return found

'''
Input: catchphrases - Given catchphrases in the file
       sentences - Sentences picked as candidate catchphrases
Output: found - number of catchphrases where more than 25% were found in the sentences
'''
def check25(catchphrases, sentences):
    
    found = 0
                
    for c in catchphrases:        
        if(c):                                  #Check if list1 is not empty
            for s in sentences:
                if (Common.lccs(s,c) >= len(c)*0.25):
                    found+=1
                    break
    
                 
    return found



def main():
    root, tests, _, trainSetId, _, resultFolder = Common.getNewFileInfo()
    baseTestPath = os.path.join(root,tests,trainSetId,resultFolder)
    
    fcf_file = 'ts_fcfound.txt'
    tfidf_file = 'ts_tfidf.txt'
    both_file = 'ts_both.txt'
    
    catchphrases = Common.readToType(os.path.join(baseTestPath, 'cTokenized.txt'))
    top_sent_fcfound = Common.readToType(os.path.join(baseTestPath,fcf_file))
    top_sent_tfidf = Common.readToType(os.path.join(baseTestPath,tfidf_file))
    top_sent_both = Common.readToType(os.path.join(baseTestPath,both_file))
    
    total_catchphrases = len(catchphrases)
    print("\nTotal Catchphrases: %s" %total_catchphrases)
    
    
    
    found_fcf100 = check100(catchphrases, top_sent_fcfound) 
    print("fcfound found100: %s" %found_fcf100)  
    
    '''
    found_fcf75 = check75(catchphrases, top_sent_fcfound) 
    print("fcfound found75+: %s" %found_fcf75)
    
    found_fcf50 = check50(catchphrases, top_sent_fcfound) 
    print("fcfound found50+: %s" %found_fcf50)
    
    found_fcf25 = check25(catchphrases, top_sent_fcfound) 
    print("fcfound found25+: %s" %found_fcf25)
    '''
      
    
    found_tfidf100 = check100(catchphrases, top_sent_tfidf) 
    print("tfidf found100: %s" %found_tfidf100)  
    
    '''
    found_tfidf75 = check75(catchphrases, top_sent_tfidf) 
    print("tfidf found75+: %s" %found_tfidf75)
    
    found_tfidf50 = check50(catchphrases, top_sent_tfidf) 
    print("tfidf found50+: %s" %found_tfidf50)
    
    found_tfidf25 = check25(catchphrases, top_sent_tfidf) 
    print("tfidf found25+: %s" %found_tfidf25)
    '''
    
    found_both100 = check100(catchphrases, top_sent_both) 
    print("both found100: %s \n" %found_both100)  
    
    
    return total_catchphrases, found_fcf100, found_tfidf100, found_both100
        
if __name__ == "__main__":
    main()

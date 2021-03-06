'''
A program that automates processing and E of multiple test files and writes Results in a csv file
'''


import os, csv
import Common, ProcessNewFile as PNF, Evaluation as E, SimilarityMeasures as SM

Common.trainSetId = 'TS8'

with open('C:/MySavedData/LakeheadUniversity/Project_547854/EvaluationResults/%s.csv' %Common.trainSetId, 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['FileName', 'TotalCatchphrases','fcfound100','tfidf100', 'both100'])

testSet = ['06_436', '06_552', '06_670', '06_790', '06_815',
           '06_844', '06_1018', '06_1086', '06_1114', '06_1124',
           '06_1184', '06_1360', '06_1391', '07_84', '07_182',
           '07_411', '07_412', '07_833', '07_843', '07_1428',
           '07_1514', '07_1594', '09_484', '09_570', '09_1340']


for item in testSet:
    Common.testFileId = item
    Common.resultFolder = 'TF_'+item
    
    PNF.root, PNF.tests, PNF.trainSet, PNF.trainSetId, PNF.testFileId, PNF.resultFolder = Common.getNewFileInfo()
    PNF.baseTestPath = os.path.join(PNF.root,PNF.tests,PNF.trainSetId,PNF.resultFolder)
    PNF.main()
    
    total_catchphrases, found_fcf100, found_tfidf100, found_both100 = E.main()
    
    with open('C:/MySavedData/LakeheadUniversity/Project_547854/EvaluationResults/%s.csv' %PNF.trainSetId, 'a') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow([item, total_catchphrases, found_fcf100, found_tfidf100, found_both100])
        
    SM.root, SM.tests, _, SM.trainSetId, _, SM.resultFolder = Common.getNewFileInfo()
    SM.main()
    
print("Process Completed")

    







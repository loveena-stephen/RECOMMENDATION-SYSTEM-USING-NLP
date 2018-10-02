* TOPICS IN THIS FILE *
1. File Split Information
2. Folder Information
3. Steps to run the code


1. FILE SPLIT INOFRMATION:
TrainSet: Files used to generate term scores
TestSet: Files used to apply the test scores and generate catchphrases
DataSet: Files used to compare extracted catchphrases and retrieve similar files


2. FOLDER INFORMATION:
Main Folder: Project_547854	
SubFolders
Corpus: Contains all the raw data files
    OtherFiles: Files not used as test files
    TestFiles: Files used as test files

EvaluationResults: Folder in which accuracy results are written in the form of csv files when running code file BatchProcessing.py

GradProject: Folder to write intermediate results for preprocessing of raw data files
    DataSet: Contains raw and intermediate files for dataset
    TestResults: Contains the raw and intermediate files, generated catchphrases and retrieved similar files for each test file for different runs
    TrainSet: Contains raw and intermediate files for trainset including the scores generated

ProjectCode: Contains the source files


3. STEPS TO RUN THE CODE
Step 1. Change the value of the variable 'root' in Common.py to the location of the folder Project_547854->GradProject. All other variabled to foldernames and file locations are preset relative to the root folder.

Step 2. Divide the files in the folder OtherFiles into 'TrainSet' and 'DataSet'

Step 3. Copy the files chosen for TrainSet in the folder GradProject->TrainSet->XMLFiles

Step 4. Copy the files chosen for DataSet intp the folder GradProject->DataSet->XMLFiles

Step 5. Run the file Preprocess.py to process the trains set, generate the term scores and proces the data set

Step 6. After running Preprocess.py, you could either process and generate catchphrases for multiple testfiles using BatchProcess.py(Refer step 6a) or process a single testfile using ProcessNewFile.py(Refer step 6b)

Step 6a.
i. Go to BatchProcess.py and change the variable Common.trainSetId to a unique value. Include the testfiles to be process in the array 'testSet'. Ensure the variables trainSetId, testFileId resultFolder in Common.py are initialized to empty values
ii. If using the same default 25 testfiles, make a copy of the Skeleton folder in GradProject->TestResults and rename it with the chosen trainSetId. 
iii. If usng custom testfiles, create a new folder in GradProject->TestResults and name it with the chosen trainsetId. Inside that folder, create one folder for each testfile in 'testSet' and name each folder in the format TF_<testfilename>.   
iv. Run BatchProcess.py.
Once the code completes running, it will generate catchphrases for all the testfiles in 'testSet' and find the accuracy and write the accuracy results in a csv file by the name of the trainSetId in the folder Project_547854->EvaluationResults. It will also run the code to retrieve similar files for each test file and write the results in a csv file in the respective testfile folder.

Step 6b. 
i. Ensure the variables trainSetId, testFileId, resultFolder in Common.py are initialized to proper values depending on the unique value chosen for trainSetId, the testfile going to be processed
ii. Create a new folder in GradProject->TestResults and name it with the trainSetId. Inside that folder, create a folder with the name TF_<testfilename>.
iii. Run ProcessNewFile.py. This will generate catchphrases for the test file being processed.
iv. Run Evaluation.py to get the accuracy results printed in the console for the current testfile.
v. To retrieve the similar files to a current test file, run the file SimilarityMeasures.py. It will write the similarity results in a file by the name SimilarFiles in the corresponding folder created for the testfile
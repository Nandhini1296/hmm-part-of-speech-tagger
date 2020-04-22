# hmm-part-of-speech-tagger
Implementation of a Hidden Markov Model Part of Speech tagger for Italian and Japanese language text.

## Data

A set of training and development data containing the following files:

 - Two files (one Italian, one Japanese) with tagged training data in the word/TAG format, with words separated by spaces and each sentence on a new line.
 - Two files (one Italian, one Japanese) with untagged development data, with words separated by spaces and each sentence on a new line.
 - Two files (one Italian, one Japanese) with tagged development data in the word/TAG format, with words separated by spaces and each sentence on a new line, to serve as an answer key.

## Programs

hmmlearn3.py will learn a hidden Markov model from the training data, and hmmdecode3.py will use the model to tag new data.

The learning program can be executed the following way: ```python hmmlearn3.py /path/to/training_data``` 

The argument is a single file containing the training data; the program will learn a hidden Markov model, and write the model parameters to a file called hmmmodel.txt. 

The tagging program will be executed the following way: ```python hmmdecode3.py /path/to/test_data```

The argument is a single file containing the test data; the program will read the parameters of a hidden Markov model from the file hmmmodel.txt, tag each word in the test data, and write the results to a text file called hmmoutput.txt in the same format as the training data.

The accuracy of the tagger is determined by a scoring script which compares the output of your tagger to a reference tagged text. 

## Results

### Results for Japanese

Correct : 10458\
Total: 11491\
Accuracy: 0.910103559307

### Results for Italian 

Correct: 11114\
Total: 11942\
Accuracy: 0.930664880255

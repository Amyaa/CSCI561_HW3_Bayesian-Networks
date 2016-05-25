# CSCI561_HW3_Bayesian-Networks

### Input:
- 1st line: two numbers (n and k) separated by a white space: the number of diseases and number of patients
- Next 4*n lines: the details about the diseases and their findings/symptoms, 4 lines for each disease.
- n*k lines: the inputs for various patients

### Output:
- If the input file name is “abc.txt” then the output file name for that input file must be “abc_inference.txt”
- Question-1: For each of the diseases, what is the probability that the patient has the disease?
- Question-2: If not all the test results are available for a particular disease for a patient, search the values for the unknown tests that would produce the maximum and minimum probabilities for each disease: help guide the patient, doctor (and insurance company) in deciding whether or not further tests are needed.
- Question-3: In the case that there are undetermined lab values, to help the doctor decide which test to run next, the program should figure out which of the tests not done yet for each disease (result either true or false) would produce the biggest increase and which would produce the biggest decrease in the probabilities for that diseases.

### The command line for the program:
- python bayes.py –i inputfilename

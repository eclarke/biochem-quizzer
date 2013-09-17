import pandas as pd
import numpy as np
import signal
import sys

def sig_handler(signal, frame):
    print("\n****\nOf {} questions, you got {} correct. You missed the following:".format(total, correct))
    for failure in missed:
        print("\t"+failure)
    print("****")
    sys.exit()

signal.signal(signal.SIGINT, sig_handler)

aa_df = pd.read_table('aa.csv', sep=',')

total = 0
correct = 0
missed = []


questions = {"question": ["What is the 3L code for {}?",
                          "What is the 1L code for {}?",
                          "What is the name of the AA represented by {}?",
                          "What is the name of the AA represented by {}?",
                          "What is the polarity of {}?",
                          "What is the charge of {}?"],
             "params": [[0,1], # The params go by column: [test, answer]
                        [0,2], 
                        [1,0], 
                        [2,0], 
                        [0,3],
                        [0,4]]}
compliments = pd.read_table('compliments.csv', sep=',')
questions = pd.DataFrame(questions)
while True:
    row_idx = np.random.randint(0, len(aa_df) - 1)
    q_idx = np.random.randint(0, len(questions) - 1)
    compliment_idx = np.random.randint(0, len(compliments) - 1)
    test_row = aa_df.irow(row_idx)
    q = questions.irow(q_idx)
    params = q["params"]
    question = q["question"]
    answer = test_row[params[1]].lower()
    print(question.format(test_row[params[0]]))
    if params[1] == 3 or params[1] == 4:
        print("\tOptions: "+", ".join(aa_df.icol(params[1]).unique()))
    ans = raw_input().lower()
    if ans == answer:
        print("\t Congratulations! You're {}.\n".format(compliments.irow(compliment_idx)[0]))
        correct += 1
        total += 1
    else:
        print("\t Incorrect! You are not so {}. The correct answer is: {}\n".format(compliments.irow(compliment_idx)[0], 
                                                                                           test_row[params[1]]))
        total += 1
        missed.append(question.format(test_row[params[0]]))
        

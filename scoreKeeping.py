"""
scoreKeeping.py
Programmer: Corey Walker
EMail: cwalker62@cnm.edu
Date: Dec 1, 2023
Purpose: Handles writing and reading of lifetime scores from /Resources/scores.csv

TODO: delete the scores.csv file before turning in so the grader can see error
        handling
"""
import os

def getCurrentScores():
    '''
    Open /Resources/scores.csv and return a dictionary of currentl saved scores

    @Return: scores -> dict {sore_name(str): score_value(str)}
    '''
    try:
        # Look for the scores save file. Return an error message if it has been deleted
        saveFilePath = os.path.join('./Resources', 'scores.csv')
        f = open(saveFilePath, 'r')
        scores = {}
        # read each line of the csv, storing the first entry as the score key
        #   and the second entry as the score value
        while True:
            line = f.readline().strip()
            if not line: break
            else:
                # 
                splitLine = line.split(',')
                # get the old total safe and store it
                scores[splitLine[0]] = splitLine[1]
        f.close()
    # If the save file is not found, don't crash the programclear
    except Exception as e:
        # This should really return a dictionary of each score type set to 0
        # However, I am intentionally catching it this way so it is more obvious
        #   when the save file has been deleted, just to easily show off
        #   error handling
        return f"oops: {e}"

    return scores

def updateScores(scores):
    '''
    Iterate through a dictionary of score values, writing each one on a new line
        to /Resources/scores.csv

    @Param: scores {str:str} -> {scoreType:scoreValue}
    '''
    try:
        saveFilePath = os.path.join('./Resources', 'scores.csv')
        f = open(saveFilePath, 'w')
        # for each key:value pair, write it the file in the appropriate form
        for scorePair in scores.items():
            f.write(f"{scorePair[0]},{scorePair[1]}\n")
        f.close()

    except Exception as e:
        print(f'oops: {e}')
    

if __name__ == '__main__':
    print(getCurrentScores())
    scoreDict = getCurrentScores()
    if type(scoreDict) ==  dict:
        # testing setting each score into it's own var
        safe = scoreDict.get('safe')
        crashed = scoreDict.get('crashed')
        print(f"safe: {safe}, crashed: {crashed}")
        # testing using a loop to get all scores from the file
        #  this allows me to add more scores to the program much easier
        for scorePair in scoreDict.items():
            print(f"{scorePair[0]},{scorePair[1]}")# cast safe to an int, add one, recast to string
        safe = str(int(safe) + 1) 
        # test that updating the score works
        scoreDict['safe'] = safe
        updateScores(scoreDict)
        scoreDict = getCurrentScores() 
        print(f"safe: {safe}, crashed: {crashed}")
    # updateScores(3,1)
    # current_scores = (getCurrentScores(), getCurrentScores())
    # print(f"current scores: {current_scores}")
    
import sys
import os
import subprocess
import git
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

def compare_by_index(diffs, vector):
    # while input is not q or Q
    while True:
        # read input
        print("Enter the index of the diff you want to compare (q to quit):")
        line = input()
        if line == 'q' or line == 'Q':
            break
        # input is index
        if not (line.isdigit()):
            print("Invalid input")
            continue
        index = int(line)
        if(index < 0):
            print("Invalid index")
            continue
        # *_index.txt
        for path in Path(diffs).glob(f'diff_*_{index}.txt'):
            # read diff
            with open(path, 'r') as f:
                diff = f.read()
            # get lenght of diff
            diff_len = len(diff.splitlines())
        # get length of vector of that index
        with open(vector, 'r') as f:
            vector_len = len(f.readlines()[index].split(','))
        
        # print diff and vector length
        print(f"given input index: {index}")
        print(f"diff length: {diff_len}")
        print(f"vector length: {vector_len}")
        print("=====================================")
    return

def compare_and_plot(diffs, vectors):
    # read vector file
    with open(vectors, 'r') as f:
        vectors = f.readlines()
    # read diff file
    with open(diffs, 'r') as f:
        diffs = f.readlines()
    
    # plot x as index, y as diff length
    # also plot x as index, y as vector length
    x = []
    y1 = []
    y2 = []
    for i in range(len(vectors)):
        # get diff length
        diff_len = len(diffs[i].splitlines())
        # get vector length
        vector_len = len(vectors[i].split(','))
        # append to x, y1, y2
        x.append(i)
        y1.append(diff_len)
        y2.append(vector_len)

def main(args):
    # folder holding diff_{reponame}_{index}.txt
    diffs = args[1]
    # gumtree vector file
    vector = args[2]

    if not os.path.exists(diffs):
        print(f"{diffs} does not exist")
        return
    if not os.path.exists(vector):
        print(f"{vector} does not exist")
        return
    
    #compare_by_index(diffs, vector)
    compare_and_plot(diffs, vector)
    

if __name__ == '__main__':
    main(sys.argv)
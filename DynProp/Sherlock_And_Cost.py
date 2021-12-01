#!/bin/python

import math
import os
import random
import re
import sys

# Complete the cost function below.

def getA(A_prev, B_curr):
    if(abs(A_prev - B_curr) > abs(A_prev - 1)):
        return B_curr
    else:
        return 1

def cost(B):
    A = range(len(B))
    
    #if B[0] > B[1]:
    A[0] = max(1, B[0])
    #else:
        #A[0] = min(1, B[0])
    
    for i in range(1, len(A)):
        A[i] = getA(A[i-1], B[i])

    print A
    D = [abs(A[i] - A[i-1]) for i in range(1,len(A))]
    print D
    return sum(D)


if __name__ == '__main__':
    # fptr = open(os.environ['OUTPUT_PATH'], 'w')

    t = int(raw_input())

    for t_itr in xrange(t):
        n = int(raw_input())

        B = map(int, raw_input().rstrip().split())

        result = cost(B)

        #fptr.write(str(result) + '\n')
        print str(result)

    #fptr.close()

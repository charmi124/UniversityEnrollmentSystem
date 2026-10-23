def fact(n):
    #Base case: 
    # no base case = recursion error with call stack because there is a limit! Normally it will go on forever!!
    if n == 1:
        return 1
    #recursive step
    return n * fact(n-1)

print(fact(5))
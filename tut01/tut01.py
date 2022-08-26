def factorial(num):
    if (num==0 or num==1):
        return 1
    else:
        x = 1
        while(num>1):
            x = x*num
            num = num-1
        return x

num = int(input("Enter a number "))
if(num >= 0):
    print("Factorial of",num, "is",factorial(num))
else:
    print("Invalid input") # Negative integer is invalid
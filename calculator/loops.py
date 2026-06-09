# signs = ["^", "^^", "^^^", "^^^^", "^^^^^", "^^^^^^", "^^^^^^", "^^^^^^^", "^^^^^^^^", "^^^^^^^^^", "^^^^^^^^^^" ]
# for x in signs:
#   if x == "^^^^^^^^^^":
#     print(x)
#     break
# for i in range (0, 5):
#   print("="*i)
  
# for i in range (10, 0, -2):
#    print("="*i)

# city = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]
# for x in city:
#   if x == "Chicago":
#     print(x)
#     break
#   print(x)

# # condition statement
# if (city == "Chicago"):
#     print("Found!")
# else:
  #  print("Not found")

# for x in range(1 , 6):
#    for y in range(0, x+1):
#     print(y, end=" ") 
# print()


# for x in range(5): # I understand why this loop works, its fairly simple
#     for y in range(x+1):
#         print(y, end='')
#     print('')

#This is a nested loop that prints a pattern of numbers. The outer loop iterates from 0 to 4, and for each iteration of the outer loop, the inner loop iterates from 0 to the current value of x (inclusive). The inner loop prints the value of y followed by a space, and after the inner loop completes, it prints a newline character to move to the next line.
for x in range(10):
    for y in range(x+1):
        print(y, end=' ')
    print(' ')
    question: str = input("Do you want to continue? (yes/no): ")
    if question.strip().lower() == "no":
            break
        
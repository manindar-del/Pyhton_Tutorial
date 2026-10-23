# a = int(input("enter Number:"))
# b = int(input("enter Number:"))
# add = a + b
# multi =  a * b
# divided = a/b

# if a >= 80 or a <=90:
#  print("Old Age")
# elif a >= 60:
#     print("Good")
# elif a>= 40:
#     print("Average")
    
    
    
# a = input("enter your name:")
# print(a)

from ast import comprehension


a = "python"
# print(a[-1])
# f_name = "rita"
# l_name ="singha"
# full_name = f"{f_name} {l_name}"
# print(full_name)

# palidrome
# strNum = input("Enter a word: ")
# word = strNum.lower()
# lenth = len(word)
# isPalidrome = True
# for i in range(lenth//2):
#     if word[i] != word[lenth-1-i]:
#         print(" Not Palidrome")
#         break
 
#     else:
#         print("Palidrome")
#         break
      
   
#  List and tuples 
# array =  ["apple","mango","Sugrcane"]
# array.append("khira")
# print(array)

# point = (2,3)
# x,y = point
# point[0] = 6
# print(point)

# i =0
# while i< 5 :
#     print(i)
#     i +=1


# for i in range(5):
#     if i == 5 :
#         break
#     if i%2 == 0:
#         continue
#     print(i)
    

# function
# def greet(name, greeting="hello"):
#     return f"{greeting},{name}"

# print(greet("Allice"))

# def factorial(n):
#     if n <=1:
#         return 1
#     return n * factorial(n -1)
        
# print(factorial(4))

# project
# import random
# def determine_choice():
#     choices = ["rock","paper","scissor"]
#     return random.choice(choices)

# def determine_winner(user_choice, computer_choice):
#     if user_choice == computer_choice:
#         return "draw!"
#     if(
#         (user_choice =="rock" and computer_choice =="paper") or
#          (user_choice =="paper" and computer_choice =="scissor") or
#           (user_choice =="scissor" and computer_choice =="rock") 
        
#     ):
#         return "You win!"
#     return "computer win!"

# user_choice = input("enter your choice: ")
# if user_choice not in ["rock","paper","scissor"]:
#     print("invalid selection")
# else:
#     computer_choice = determine_choice()
#     print("your selection", user_choice)
#     print("computer selection", computer_choice)
#     result = determine_winner(user_choice, computer_choice)
#     print(result)
    
    
    # file
# with open("data.txt", "w") as f:
    
#     f.write("hello world\n")
    
    
#     with open("data.txt","r") as f:
#         content = f.read()
#         print(content)

# function
# class Dog:
#     def __init__(self, name,breed):
        
#         self.name= name
#         self.breed = breed
        
#     def bark(self):
#             print(f"{self.name} and wof!")
            
# d1 = Dog("alice","labrour")          
# d1.bark()
 
# class Animal:
#     def speak(self):
#         return "speak more"
    
# class Dog(Animal):
    
#   def speak(self):       
#     return "Bark"


# print(Dog().speak())  


# class bank_account:
    
#     def __init__(self, balance):
#         self.balance = balance
        
#     def get_balance(self):
#         print(f"Balance:{self.balance}")
    
    
# d1 = bank_account(2000)
# d1.get_balance()
    
    
    
 # ploymorhism
 
# class Payment:
#     def pay(self):
#         print("processing payment")
        
# class CreditCard(Payment):        
#     def pay(self, amount):
#         print(f"pay {amount} using credit card")
            
        
             
# class UPI(Payment):        
#     def pay(self, amount):
#         print(f"pay {amount} using UPI")
            
        
# d1 = CreditCard()
# d2 = UPI()
# d1.pay(300)
# d2.pay(3000)
    
    
    # lambada
    
# a = lambda x, y: x + y
# print(a(23, 30))
a = [1,2,3,4,5]
# map = list(map(lambda x : x*x, a))
# filter = list(filter(lambda x : x % 2 == 0, a))
# print(filter)

# exceptional handling

# try:
#     a = 10
#     b =0
    
#     print(a/b)
# except ZeroDivisionError:
#     print("can not be divided")
     
     
     
# try:
#     number = int(input("Enter number: "))
#     a = 100/number
#     print(a)
# except ValueError:
#     print("invalid input")
# except ZeroDivisionError:
#     print("number can not divisible")   
    
# else:
#     print("you entered", number)


# age =12
# if age < 18:
#     raise ValueError("age must be  18  or above")


# def add(a,b):
#     return a +b

# print(add(12,23))
# try:
#     a = int(input("Enter number: "))
#     a1 = 100/a
#     print(a1)

# except ValueError:
#  print("invalid input")
# except ZeroDivisionError:
#     print(" number can not divisible")

# args  and kwargs

# def add(*numbers):
#     total = 0
#     for number in numbers:
#         total += number
#     return total
    
# print(add(10,30,30))

# def user_Details(**kwargs):
#     print(kwargs)
#     print(kwargs["name"])
#     print(kwargs["mobile"])
    
# user_Details(
#         name="test",
#         mobile=123456789
#     )


# # normal list

# result =[]
# for i in range(1,6):
#     result.append(i*i)
#     print(result)

# kwarg
# def user_details(**kwargs):
#     print(kwargs["age"])

# user_details(
#     name="tester",
#     age=32 )


# list comprehension
# number =[i*i for i in range(1,6) if i%2 == 0]
# print(number)

# set comprehension
# arr ={1,2,2,2}
# print(arr)

# def  loggers(func):
#     def wrapper():
#         print("first part")
        
#         func()
#         print("2nd part")
#     return wrapper
         
# @loggers
# def user():
#     print("Hello")
    
# user()   


# import json
# user={
#     "name":"tester",
#     "age":30
# }

# with open("user.json", "w") as file:
#   json.dump(user,file, indent=4 )


# with open("user.json","r") as file:
#     users = json.load(file)
#     print(users)



def loggers(func):
    def wrapper():
        print("First")
        func()
        print("second")
        
    return wrapper

@loggers
def user():
    print("hello")    
    
user()
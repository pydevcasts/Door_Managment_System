# def goodbye(name, adjective):
#     print('Goodbye, %s, it was %s to meet you.' % (name, adjective))

# import atexit
# atexit.register(goodbye, adjective='nice', name='Donny')



# @atexit.register
# def goodbye2():
#     print("You are now leaving the Python sector.")

# def all(iterable):
#     for element in iterable:
#         if element:
#             print(True)
#     print(False)

# def any(iterable):
#     for element in iterable:
#         if element:
#             print(True)
#     print('ok')
# any((1,2,))

# x = ["gf","hg"]
# print(list(reversed(x)))

# x = ('Guru99', 20, 'Education') # tuple packing

# (company, emp, profile) = x # tuple unpacking

# print(company)

# print(emp)

# print(profile)

# x = 'hello world'
# print(eval(repr(x)))
# print(eval(str(x)))
# x = [True, True, True]

# if any(x):
#     print("At least one True")

# if all(x):
#     print("Not one False")

# if any(x) and not all(x):
#     print("At least one True and one False")

x =int("hello") 
# print(x.__repr__())
print(str(x).__str__())
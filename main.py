import ctypes
import csv_reader

money = csv_reader.read_column_from_csv('friends.csv', 'money')
print("Money", money)


#load the shared c library
lib = ctypes.CDLL('./libsum.dll')

#Tells python the argument types and return type of the C function.
lib.sum_array.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int]
lib.sum_array.restype = ctypes.c_double

arr = (ctypes.c_double * len(money))(*money)
result = lib.sum_array(arr, len(money))
print("Sum of total money among friends: %.2f" % result)

from collections import Counter

arr = [4, 8, 2, 8, 9]
def odd_occurring_num(arr):
    return [i for i in arr if arr.count(i) < 2]

print(odd_occurring_num(arr))
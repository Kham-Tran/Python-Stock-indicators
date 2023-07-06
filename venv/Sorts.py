def mergeSort(arr):
    mid_point = len(arr)//2
    return arr[:mid_point],arr[mid_point:]


def merge(arr1,arr2):
    c1 = 0
    c2 = 0
    temp = []
    for n in range(c1,len(arr1)):
        if c1 == len(arr1)-1 and c2 == len(arr2)-1:
            if arr1[c1] < arr2[c2]:
                temp.append(arr1[c1])
                temp.append(arr2[c2])
            else:
                temp.append(arr2[c2])
                temp.append(arr1[c1])
    return temp


arr = [1]
a , b = mergeSort(arr)
print(a,b)

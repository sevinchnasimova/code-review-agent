def doBinarySearch(array, target):
    l, r = 0, len(array) - 1

    while l <= r:
        mid = (l + r) // 2
        if target > array[mid]:
            l = mid + 1
        elif target < array[mid]:
            r = mid - 1
        else:
            return mid
        
    return -1


doBinarySearch([1, 2, 3, 4, 5, 6], 5)
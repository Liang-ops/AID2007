"""
 给你一个长度为n的数组，其中只有一个数字出现大于n/2次，问如何快速找到这个数字
"""
list01 = [2,2,2,2,6,6,6,6,6]
list01.sort()
def build_dict(list):
    dict = {}
    for item in list:
        if item not in dict:
            dict[item] = 1
        else:
            dict[item] += 1
    return dict
def find_number(dict,list):
    for key, value in dict.items():
        if value > len(list)/2:
           return key
if __name__ == '__main__':
    dict01 = build_dict(list01)
    print(find_number(dict01,list01))



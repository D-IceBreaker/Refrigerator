import collections

def merge_the_tools(string, k):
    for i in range( int(len(string) / k) ):
        u = ''
        for j in range(k):
            u += string[(k * i) + j]
        print(''.join(collections.OrderedDict.fromkeys(u).keys()))

if __name__ == '__main__':
    string = input()
    k = int(input())
    merge_the_tools(string, k)
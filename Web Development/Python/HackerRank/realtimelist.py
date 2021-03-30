if __name__ == '__main__':
    N = int(input())

    my_list = []

    for i in range(N):
        inp = input().split()
        if inp[0] == 'insert':
            my_list.insert(int(inp[1]), int(inp[2]))
        elif inp[0] == 'print':
            print(my_list)
        elif inp[0] == 'remove':
            my_list.remove(int(inp[1]))
        elif inp[0] == 'append':
            my_list.append(int(inp[1]))
        elif inp[0] == 'sort':
            my_list.sort()
        elif inp[0] == 'pop':
            my_list.pop()
        elif inp[0] == 'reverse':
            my_list.reverse()
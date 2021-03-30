def second_min(arr):
    maximum = float('inf')
    first, second = maximum, maximum
    for n in arr:
        if n[1] < first:
            first, second = n[1], first
        elif first < n[1] < second:
            second = n[1]
    return second if second != maximum else None

if __name__ == '__main__':
    students = []
    ans = []

    for _ in range(int(input())):
        name = input()
        score = float(input())

        students.append([name, score])

    res = second_min(students)

    for i in students:
        if i[1] == res:
            ans.append(i[0])
    
    for j in sorted(ans):
        print(j)



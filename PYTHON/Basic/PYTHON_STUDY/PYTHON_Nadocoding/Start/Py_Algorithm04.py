
#문제 4-1
#아래와 같은 패턴의 별(*)을 출력하는 프로그램을 작성해 보세요. 참고로 print('*', end='')와 같이 print 함수를 사용하면 줄바꿈 없이 화면에 출력할 수 있습니다.

print('*'*5, end='')
print()
print()

#문제 4-2
#아래와 같은 패턴의 별(*)을 출력하는 프로그램을 작성해보세요. (힌트: 중첩 루프 사용)
#내 방법
for i in range(4):
    print('*'*5)
print()
print()

#책방법
for i in range(4):
    for j in range(5):
        print('*', end='')
    print()

#문제 4-3
for i in range(5):
    for j in range(i+1):
        print('x',end='')
    print()

print()
#문제 4-4
for i in range(5):
    for j in range(5-i):
        print('x', end='')
    print()

print()
#문제 4-5
for i in range(5):
    for j in range(4-i):
        print(' ', end='')
    for j in range(i+1):
        print('x', end='')
    print()

print()
#문제 4-6
for i in range(5):
    for j in range(i):
        print(' ', end='')
    for j in range(5-i):
        print('x', end='')
    print()

print()
#문제 4-7
for i in range(5):
    for j in range(2*(i+1)-1):
        print('x', end='')
    print()

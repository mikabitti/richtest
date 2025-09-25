import time

target = 0
while True:
    target = input("Give me number between 1 and 20: ")
    try:
        target = int(target)
        if 1 <= target and target <= 20:
            break
    except ValueError as e:
        print("Try again!")


print(f"Counting to {target}: ", end='')

for count in range(0, target-1):
    print(f'{count+1}...', end='')
    time.sleep(0.5)
print(f"{target}!!!!!!!!!")

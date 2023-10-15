import re
ip = input()
if re.match(r'((25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}|[0-9]{2}|[0-9])(\.)){4}', ip):
    print(True)
else:
    print(False)


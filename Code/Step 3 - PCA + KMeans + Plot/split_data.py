f = open('LAtest_5.txt')
header = f.readline()
s = set()
count = 0

for line in f:
  ll = line.split(',')
  name = ll[0] + '-' + ll[1] + '-' + ll[2]
  if name not in s :
    tmp = open('SplitFiles/' + name + '.csv', 'w')
    tmp.write(header)
    tmp.write(line)
    tmp.close()
    s.add(name)
  else :
    tmp = open('SplitFiles/' + name + '.csv', 'a')
    tmp.write(line)
    tmp.close()
  count = count + 1
  if count % 1000000 == 0 :
    print count

f.close()

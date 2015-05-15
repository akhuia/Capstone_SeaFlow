#Date: 5/4/2015
#Description: Pipeline - Downloads File - Splits File by (Cruise-Day-File_Id)

from pandas.io.parsers import read_csv
import pandas as pd
import urllib

# Command Line - USE wget.exe -O <FileToStoreURLContents> --no-check-certificate <URL>

f = open('C:\\Users\\NYU\\Cap\\seaflow_data.csv')
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

if __name__ == "__main__":
 main()
# coding=utf8

import commands
import pdb
import sys
from collections import Counter

des = sys.argv[1]
cmd = "rm -rf name.log && find -name '*.txt' >> name.log"
result = commands.getstatusoutput(cmd)
f = open('name.log', 'r')
line = f.readline()
dic = {}
n = 0
while line:
    real_file = open(line.strip('\n'), 'r')
    each_line = real_file.readline().decode('gbk').encode('utf-8')
    while each_line:
        found = each_line.find(des)
        if found != -1:
            dic[line.strip('\n') + str(n)] = each_line
            n += 1
        each_line = real_file.readline().decode('gbk').encode('utf-8')
    real_file.close()
    line = f.readline()
f.close()
for key in dic:
    print key, dic[key]
print 'we find the keyword for ', len(dic), ' times.'


path ='D:\\spark-2.0.1-bin-hadoop2.7\\bin\\'
f = open(path+'20161031-1116.export.CSV','a')
for each in range(1,10):
#    f.write('\n')
    f.write(open(path+'2016110' + str(each) +'.export.CSV','r').read())
for each in range(11,17):
#    f.write('\n')
    f.write(open(path+'201611' + str(each) +'.export.CSV','r').read())
f.close()

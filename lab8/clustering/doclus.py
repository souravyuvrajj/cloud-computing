import os
i = 1
no_of_resumes = 8
SS = set()
Cluster = dict()
while i<=8:
    name = str(i)+".txt"
    f = open(name,"r")
    j=1
    no_of_line=7
    while j<=no_of_line:
        line = f.readline()
        a = line.split(" ")
        if a[0]=="Skills-":
            skill = a[1]
            SS.add(skill[:len(skill)-1])
            Cluster[name] = skill[:len(skill)-1]
            #print skill
        j+=1

    i+=1
#print SS
#print Cluster

for x in SS:
    print x,
    print ":"
    for key, value in Cluster.iteritems():
        if value==x:
            print key,
            print "\t",
    print

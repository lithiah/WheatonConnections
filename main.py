import re
import requests
from bs4 import BeautifulSoup 

def main():
    data = {'submit_btn' : 'Search Catalog', 'schedule_beginterm':'201510', 'subject_cat':'CONX'}
    url = 'https://weblprod1.wheatonma.edu/PROD/bzcrschd.P_OpenDoor'

    r = requests.post(url=url, data=data)

    doc = BeautifulSoup(r.content.decode('utf-8'))
    doc.prettify().encode('utf-8')


    connectionNames = re.compile(r'CONX [0-9][0-9][0-9][0-9][0-9]')
    descriptions = re.compile(r'[A-Z][a-z][a-z][a-z]?[a-z]? |(or three) course connection')
    nameList = []
    descriptionList = []
    rows = doc.find_all('tr')

    for i in range(len(rows)):
        arow = rows[i]
        content = arow.find('td').getText().encode('utf-8').strip()
        if connectionNames.match(content):
            nameList.append(str(content).replace('\'','`'))
        if descriptions.match(content):
            descriptionList.append(str(content).replace('\'','`').replace('\n', ' '))

    courseNum = re.compile(r'[A-Z]{2,4} [0-9]{3}')
    orCourse = re.compile(r'([A-Z]{2,4} [0-9]{3})(?:(?!with).)* or ([A-Z]{2,4} [0-9]{3})(?:(?!with).)*| ([A-Z]{2,4} [0-9]{3})(?:(?!with).)* or ([0-9]{3})(?:(?!with).)*')
    andCourse = re.compile(r'([A-Z]{2,4} [0-9]{3})(?:(?!or).)* with ([A-Z]{2,4} [0-9]{3})(?:(?!or).)*')
    departmentList = []
    linkList = []
    newDepartment = {}
    
    with open('graph.json', 'w') as graphFile:
        graphFile.write("{\"nodes\": [\n")
        # Add Departments
        for i in xrange(len(descriptionList)):
            oneRow = descriptionList[i]
            if courseNum.search(oneRow):
                matchCourse = courseNum.findall(oneRow)
                for j in xrange(len(matchCourse)):
                    oneDepartment = matchCourse[j][0:(len(matchCourse[j])-4)]
                    if not oneDepartment in departmentList:
                        departmentList.append(str(oneDepartment))

        connectionList = []

        # Add Courses
        for i in xrange(len(descriptionList)):
            oneRow = descriptionList[i].replace('\n', ' ')
            if courseNum.search(oneRow):
                matchCourse = courseNum.findall(oneRow)
                for j in xrange(len(matchCourse)):
                    if not matchCourse[j] in departmentList:
                        departmentList.append(str(matchCourse[j]))
                        tempList = []
                        tempList.append(str(matchCourse[j][0:(len(matchCourse[j])-4)]))
                        tempList.append(str(matchCourse[j]))
                        connectionList.append(tempList)

        # Add Connections
        for i in xrange(len(descriptionList)):
            oneRow = descriptionList[i].replace('\n', ' ')
            if orCourse.search(oneRow):
                groupOne = []
                groupTwo = []
                count = 0
                matchCourse = orCourse.findall(oneRow)
                for j in xrange(len(matchCourse)):
                    oneCourse = matchCourse[j]
                    if not oneCourse in connectionList:
                        count+=1

                        if count <= (len(matchCourse) / 2):
                            someGroup = groupOne
                        else:
                            someGroup = groupTwo
                        
                        if oneCourse[0] != '':
                            someGroup.append(str(oneCourse[0]))
                            someGroup.append(str(oneCourse[1]))
                        else:
                            someGroup.append(str(oneCourse[2]))
                            someGroup.append(str(oneCourse[2][0:(len(oneCourse[2])-4)])+' '+str(oneCourse[3]))
                            departmentList.append(str(oneCourse[2][0:(len(oneCourse[2])-4)])+' '+str(oneCourse[3]))
                            tempList = []
                            tempList.append(str(oneCourse[2][0:(len(oneCourse[2])-4)])+' '+str(oneCourse[3]))
                            tempList.append(str(oneCourse[2][0:(len(oneCourse[2])-4)]))
                            connectionList.append(tempList)

                for j in xrange(len(groupOne)):
                    for k in xrange(len(groupTwo)):
                        tempList = []
                        tempList.append(groupOne[j])
                        tempList.append(groupTwo[k])
                        connectionList.append(tempList)

            elif andCourse.search(oneRow):
                matchCourse = andCourse.findall(oneRow)
                for j in xrange(len(matchCourse)):
                    oneCourse = matchCourse[j]
                    if not oneCourse in connectionList:
                        tempList = []
                        tempList.append(oneCourse[0])
                        tempList.append(oneCourse[1])
                        connectionList.append(tempList)

        for i in xrange(len(departmentList)):
            newDepartment.update({"name":departmentList[i]})
            if (i != len(departmentList)-1):
                graphFile.write('\t'+str(newDepartment).replace('\'', '"')+','+'\n')
            else:
                graphFile.write('\t'+str(newDepartment).replace('\'', '"')+'\n')

        graphFile.write("],\n\"links\": [\n")

        for i in xrange(len(connectionList)):
            oneLink = {}
            sourceLocation = departmentList.index(connectionList[i][0])
            targetLocation = departmentList.index(connectionList[i][1])
            oneLink.update({"source":sourceLocation})
            oneLink.update({"target":targetLocation})
            if (i != len(connectionList)-1):
                graphFile.write('\t'+str(oneLink).replace('\'', '"')+','+'\n')
            else:
                graphFile.write('\t'+str(oneLink).replace('\'', '"')+'\n')

        graphFile.write("]}")

        with open('connections.json', 'w') as outputFile:
            outputFile.write("{\"ConnectionDescriptions\": [\n")
            for i in xrange(len(nameList)):
                oneConnection = {}
                oneConnection.update({"CourseName":nameList[i]})
                oneConnection.update({"CourseDescription":descriptionList[i]})
                outputFile.write('\t'+str(oneConnection).replace('\'', '"')+'\n')
            outputFile.write("],\n\"Connections\": [\n")
            outputFile.write('\t'+str(connectionList).replace('\'', '"')+'\n]}')
    
if __name__ == '__main__':
    main()
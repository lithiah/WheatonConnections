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
            descriptionList.append(str(content).replace('\'','`'))

    with open('connections.json', 'w') as outputFile:
        outputFile.write("{\"connections\": [\n")
        for i in xrange(len(nameList)):
            oneConnection = {}
            oneConnection.update({"nodes":nameList[i]})
            oneConnection.update({"CourseDescription":descriptionList[i]})
            outputFile.write('\t'+str(oneConnection).replace('\'', '"')+'\n')
        outputFile.write("]}")


    courseNum = re.compile(r'[A-Z][A-Z][A-Z]?[A-Z]? [0-9]{3}')
    orCourse = re.compile(r'[A-Z][A-Z][A-Z]?[A-Z]? [0-9]{3}[.]* or [0-9]{3}')
    andCourse = re.compile(r'[A-Z][A-Z][A-Z]?[A-Z]? [0-9]{3}[.]* with [A-Z][A-Z][A-Z]?[A-Z]? [0-9]{3}')
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

        # Add Courses
        for i in xrange(len(descriptionList)):
            oneRow = descriptionList[i]
            if courseNum.search(oneRow):
                matchCourse = courseNum.findall(oneRow)
                for j in xrange(len(matchCourse)):
                    if not matchCourse[j] in departmentList:
                        departmentList.append(str(matchCourse[j]))

        # Add Connections
        for i in xrange(len(descriptionList)):
            oneRow = descriptionList[i]
            if orCourse.search(oneRow):
                # print "here"
                matchCourse = orCourse.findall(oneRow)
                for j in xrange(len(matchCourse)):
                    oneCourse = matchCourse[j][0:(len(matchCourse[j]))]
                    # print oneCourse
                    if not oneCourse in departmentList:
                        departmentList.append(str(oneCourse))
            if andCourse.search(oneRow):
                matchCourse = andCourse.findall(oneRow)
                for j in xrange(len(matchCourse)):
                    oneCourse = matchCourse[j][0:(len(matchCourse[j]))]
                    # print oneCourse
                    if not oneCourse in departmentList:
                        departmentList.append(str(oneCourse))
                    
        for i in xrange(len(departmentList)):
            newDepartment.update({"name":departmentList[i]})
            graphFile.write('\t'+str(newDepartment).replace('\'', '"')+'\n')
                
        graphFile.write("],\n\"links\": [\n")

        for i in xrange(len(departmentList)):
            oneLink = {}
            oneLink.update({"source":i})
            graphFile.write('\t'+str(oneLink).replace('\'', '"')+'\n')
        graphFile.write("]}")
    
if __name__ == '__main__':
    main()
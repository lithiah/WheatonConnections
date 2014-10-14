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


    courseNum = re.compile(r'[A-Z][A-Z][A-Z]?[A-Z]? [0-9][0-9][0-9]')
    department = re.compile(r'[A-Z][A-Z][A-Z]?[A-Z]?')
    departmentList = []
    linkList = []
    
    with open('graph.json', 'w') as graphFile:
        graphFile.write("{\"nodes\": [\n")
        for i in xrange(len(descriptionList)):
            oneRow = descriptionList[i]
            searchStart = 0
            searchEnd = len(oneRow)
            while (searchStart != searchEnd) :
                newDepartment = {}
                if courseNum.search(oneRow[searchStart:searchEnd]) != "none":
                    matchCourse = courseNum.search(oneRow[searchStart:searchEnd])
                    match = department.search(oneRow[matchCourse.start():searchEnd])
                    print "match"

                    oneDepartment = oneRow[match.start():match.end()]
                    if not oneDepartment in departmentList:
                        print oneRow[match.start():match.end()]
                        departmentList.append(str(oneDepartment))
                    searchStart = match.end()
                else:
                    print "here"
                    searchStart = searchEnd
                    
        for i in xrange(len(departmentList)):
            newDepartment.update({"name":departmentList[i]})
            graphFile.write('\t'+str(newDepartment).replace('\'', '"')+'\n')
                
        graphFile.write("],\n\"links\": [\n")

        for i in xrange(len(descriptionList)):
            if department.match(descriptionList[i]):
                departmentList.append(str(descriptionList[i]).replace('\'','`'))
            oneLink = {}
            oneLink.update({"source":i})
            graphFile.write('\t'+str(oneLink).replace('\'', '"')+'\n')
        graphFile.write("]}")
    
if __name__ == '__main__':
    main()
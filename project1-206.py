import os
import filecmp
from dateutil.relativedelta import *
from datetime import date

#git commands
#git add [filename]
#git commit -m "[message]"
#git push



def getData(fileName):
# get a list of dictionary objects from the file
#Input: file name
#Ouput: return a list of dictionary objects where
#the keys are from the first row in the data. and the values are each of the other rows

	inFile= open(fileName, "r")
	lines= inFile.readlines()
	inFile.close()

	outputdict=[]
	columntitles = lines[0].strip('\n').split(',')
	datalines= lines[1:] #everything after line 0
	for rawline in datalines:
		line = rawline.strip('\n')
		current_dict={}
		datavalues=line.split(',')
		for i in range(len(columntitles)):
			current_dict[columntitles[i]]= datavalues[i]
		outputdict.append(current_dict)
	return outputdict



def mySort(data,col):
# Sort based on key/column
#Input: list of dictionaries and col (key) to sort on
#Output: Return the first item in the sorted list as a string of just: firstName lastName
	datacopy=data.copy()
	datacopy.sort(key=lambda x: x[col])
	firstitem=datacopy[0]
	outputstring=firstitem['First']+ ' ' + firstitem['Last']
	return outputstring


def classSizes(data):
# Create a histogram
# Input: list of dictionaries
# Output: Return a list of tuples sorted by the number of students in that class in
# descending order
# [('Senior', 26), ('Junior', 25), ('Freshman', 21), ('Sophomore', 18)]

	tallydict={'Senior':0, 'Junior':0, 'Freshman':0, 'Sophomore':0}
	for student in data:
		tallydict[student['Class']]+=1
	classtupleslist=[(classkey, tallydict[classkey]) for classkey in tallydict.keys()] #list of tuples
	classtupleslist.sort(key=lambda x: x[1], reverse=True)
	return classtupleslist
	#we need to turn dictionary into tuples list and then sort



def findMonth(a):
	# Find the most common birth month form this data
	# Input: list of dictionaries
	# Output: Return the month (1-12) that had the most births in the data
	bdict={}
	for student in a:
		dateparts=student["DOB"].split("/")[0]
		birthstrip= dateparts.strip()
		if birthstrip not in bdict:
			bdict[birthstrip]=1
		else:
			bdict[birthstrip]+=1
	sortedmonthlist= sorted(bdict.items(), key=lambda x: x[1], reverse=True)
	return int((sortedmonthlist[0][0]))

def mySortPrint(a,col,fileName):
#Similar to mySort, but instead of returning single
#Student, the sorted data is saved to a csv file.
# as fist,last,email
#Input: list of dictionaries, col (key) to sort by and output file name
#Output: No return value, but the file is written
	datacopy=a.copy()
	datacopy.sort(key=lambda x: x[col])
	outFile= open(fileName, "w")
	for student in datacopy:
		linetowrite=student["First"] + ',' + student["Last"] + ',' + student["Email"] + '\n'
		outFile.write(linetowrite)
	outFile.close()


def findAge(a):
# def findAge(a):
# Input: list of dictionaries
# Output: Return the average age of the students and round that age to the nearest
# integer.  You will need to work with the DOB and the current date to find the current
# age in years.

	cumulativeage=0
	numstudents=0
	for student in a:
		dobstring= student['DOB']
		dateparts=dobstring.split('/')
		born=date(month=int(dateparts[0]), day=int(dateparts[1]), year=int(dateparts[2]))
		today = date.today()
		age= today.year - born.year - ((today.month, today.day) < (born.month, born.day)) #age function comes from https://stackoverflow.com/questions/2217488/age-from-birthdate-in-python
		cumulativeage+=age
		numstudents+=1
	return int(round(1.0 * cumulativeage / numstudents))


################################################################
## DO NOT MODIFY ANY CODE BELOW THIS
################################################################

## We have provided simple test() function used in main() to print what each function returns vs. what it's supposed to return.
def test(got, expected, pts):
  score = 0;
  if got == expected:
    score = pts
    print(" OK ", end=" ")
  else:
    print (" XX ", end=" ")
  print("Got: ",got, "Expected: ",expected)
  return score


# Provided main() calls the above functions with interesting inputs, using test() to check if each result is correct or not.
def main():
	total = 0
	print("Read in Test data and store as a list of dictionaries")
	data = getData('P1DataA.csv')
	data2 = getData('P1DataB.csv')
	total += test(type(data),type([]),50)

	print()
	print("First student sorted by First name:")
	total += test(mySort(data,'First'),'Abbot Le',25)
	total += test(mySort(data2,'First'),'Adam Rocha',25)

	print("First student sorted by Last name:")
	total += test(mySort(data,'Last'),'Elijah Adams',25)
	total += test(mySort(data2,'Last'),'Elijah Adams',25)

	print("First student sorted by Email:")
	total += test(mySort(data,'Email'),'Hope Craft',25)
	total += test(mySort(data2,'Email'),'Orli Humphrey',25)

	print("\nEach grade ordered by size:")
	total += test(classSizes(data),[('Junior', 28), ('Senior', 27), ('Freshman', 23), ('Sophomore', 22)],25)
	total += test(classSizes(data2),[('Senior', 26), ('Junior', 25), ('Freshman', 21), ('Sophomore', 18)],25)

	print("\nThe most common month of the year to be born is:")
	total += test(findMonth(data),3,15)
	total += test(findMonth(data2),3,15)

	print("\nSuccessful sort and print to file:")
	mySortPrint(data,'Last','results.csv')
	if os.path.exists('results.csv'):
		total += test(filecmp.cmp('outfile.csv', 'results.csv'),True,20)

	print("\nTest of extra credit: Calcuate average age")
	total += test(findAge(data), 40, 5)
	total += test(findAge(data2), 42, 5)

	print("Your final score is " + str(total))

# Standard boilerplate to call the main() function that tests all your code
if __name__ == '__main__':
    main()

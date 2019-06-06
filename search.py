import argparse
import csv
import time


class Search():


	def __init__(self):

		self.searchTime = 0.0
		self.qryList    = []
		self.itemList   = []
		self.results    = []
		self.itemIndex  = {}

		self.readArgs()


	def readArgs(self):
		parser = argparse.ArgumentParser()

		parser.add_argument('--csv', help='csv file', required=True)
		parser.add_argument('--qry', help='query file', required=True)
		parser.add_argument('--timeit', help='print time info', required=False, default=False)

		args = parser.parse_args()

		self.csvFile = args.csv
		self.qryFile = args.qry
		self.timeIt = args.timeit


	def loadCSV(self):

		with open(self.csvFile, 'r') as csvfile:

			csvReader = csv.reader(csvfile, delimiter=',')

			itemPos = 0

			for id, name, brand in csvReader:

				lowerCaseTokens = " ".join(name.split()).lower().split() + " ".join(brand.split()).lower().split()

				# Sort and create index to improve speed
				lowerCaseTokens.sort()
				tokenIndex = {}

				for lowerCaseToken in lowerCaseTokens:

					# Get first character
					firstChar = lowerCaseToken[0]

					if firstChar not in self.itemIndex:
						self.itemIndex[firstChar] = {lowerCaseToken:{itemPos:1}}
					else:
						if lowerCaseToken not in self.itemIndex[firstChar]:
							self.itemIndex[firstChar][lowerCaseToken] = {itemPos:1}
						else:
							if itemPos not in self.itemIndex[firstChar][lowerCaseToken]:
								self.itemIndex[firstChar][lowerCaseToken][itemPos] = 1
							else:
								self.itemIndex[firstChar][lowerCaseToken][itemPos] += 1

				self.itemList.append({'id':id.strip(),'name':name,'brand':brand})

				itemPos +=1


	def getScore(self,ocurrences,qryToken,itemToken):
		return (ocurrences * len(qryToken)) / float(len(itemToken))


	def processQuery(self,query):

		# List containing all our matches
		matchesDict = {}

		# For each query token
		for qryToken in query:

			# Get qryToken first character
			firstChar = qryToken[0]

			# Check if we have something starting with the same character
			if firstChar in self.itemIndex:

				for itemToken in self.itemIndex.setdefault(firstChar,{}):

					#this means we have a match
					if itemToken.startswith(qryToken):

						for itemPos in self.itemIndex[firstChar][itemToken]:
							ocurrences = self.itemIndex[firstChar][itemToken][itemPos]
							matchesDict.setdefault(itemPos,{'score':0,'unmatchedTokens':query.copy()})['score'] += self.getScore(ocurrences,qryToken,itemToken)
							matchesDict[itemPos]['unmatchedTokens'].discard(qryToken)

		self.results.append(matchesDict)



	def printResults(self):

		for result in self.results:

			resultList = []

			for itemPos in result:

				if len(result[itemPos]['unmatchedTokens']) == 0:
					resultList.append([itemPos,result[itemPos]['score']])

			print len(resultList)

			# Sort the match list score based
			resultList.sort(key=lambda x:(x[1]),reverse=True)

			for itemPos,score in resultList[:10]:
				print("%f,%s,%s,%s" % (score,self.itemList[itemPos]['id'],self.itemList[itemPos]['name'],self.itemList[itemPos]['brand']))


	def loadQry(self):
		with open(self.qryFile, 'r') as qryfile:
			lines = qryfile.readlines()

			for line in lines:
				self.qryList.append(set(item.lower() for item in line.split()))


	def processQueries(self):
		start = time.time()

		for qry in self.qryList:
			self.processQuery(qry)

		end = time.time()

		self.searchTime = end - start


	def printTiming(self):
		if self.timeIt:
			print("\n%d queries processed in %f seconds. %f seconds per query" % (len(self.qryList), self.searchTime, ((self.searchTime) / (len(self.qryList)))))


	def do(self):
		self.loadCSV()
		self.loadQry()
		self.processQueries()
		self.printResults()
		self.printTiming()


if __name__ == '__main__':
	search = Search()
	search.do()


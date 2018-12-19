import pandas
from bs4 import BeautifulSoup
import csv
import argparse
from politeness.helpers import set_corenlp_url
from politeness.classifier import Classifier

#example command to run the server from the command line
#java -mx5g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -timeout 1000000

def write(args):
	#Set up the stanford corenlp server
	set_corenlp_url("http://localhost:9000")
	cls = Classifier()

	#read in the data file 
	data = pandas.read_csv(args.read_file, sep=',', error_bad_lines=False)

	#Set the write file
	outFile = open(args.write_file, 'w', newline='')
	fieldnames = ["Id", "PostTypeId", "AcceptedAnswerId", "ParentId", "CreationDate", "DeletionDate", "Score", "ViewCount", "Body", "BodyNOHTML", "PolitenessConfidence", "ImpolitenessConfidence", "OwnerUserId", "OwnerDisplayName", "LastEditorUserId", "LastEditorDisplayName", "LastEditDate", "LastActivityDate", "Title", "Tags","AnswerCount", "CommentCount", "FavoriteCount", "ClosedDate", "CommunityOwnedDate"]
	w = csv.DictWriter(outFile, fieldnames = fieldnames)
	w.writeheader() 

	skips = 0

	#Create the CSV of processed data
	for i in range(data.shape[0]):
		try:
			tempDict = {}
			
			tempDict["Id"] = str(data.iloc[i, 0])
			tempDict["PostTypeId"] = str(data.iloc[i, 1])
			tempDict["AcceptedAnswerId"] = str(data.iloc[i, 2])
			tempDict["ParentId"] = str(data.iloc[i, 3])
			tempDict["CreationDate"] = str(data.iloc[i, 4])
			tempDict["DeletionDate"] = str(data.iloc[i, 5])
			tempDict["Score"] = str(data.iloc[i, 6])
			tempDict["ViewCount"] = str(data.iloc[i, 7])
			tempDict["Body"] = str(data.iloc[i, 8])
			
			#Remove html and code snippets
			temp = str(data.iloc[i, 8])
			soup = BeautifulSoup(str(data.iloc[i, 8]), "lxml")
			removals = soup.find_all('code')
			for match in removals:
				match.decompose()
			text = soup.get_text()
			text = text.replace('\n', ' ').replace('\r', '').replace('\t', '') #remove newlines and such

			#get the predictions for the classifier
			output = cls.predict(text)
			vals = list(output[-1].values()) #The last entry in the analyzed array of values are the scores for the entire doc
			
			tempDict["BodyNOHTML"] = text
			
			tempDict["PolitenessConfidence"] = str(vals[0][0])
			tempDict["ImpolitenessConfidence"] = str(vals[0][1])
			tempDict["OwnerUserId"] = str(data.iloc[i, 9])
			tempDict["OwnerDisplayName"] = str(data.iloc[i,10])
			tempDict["LastEditorUserId"] = str(data.iloc[i, 11])
			tempDict["LastEditorDisplayName"] = str(data.iloc[i, 12])
			tempDict["LastEditDate"] = str(data.iloc[i, 13])
			tempDict["LastActivityDate"] = str(data.iloc[i, 14])
			tempDict["Title"] = str(data.iloc[i, 15])
			tempDict["Tags"] = str(data.iloc[i, 16])
			tempDict["AnswerCount"] = str(data.iloc[i, 17])
			tempDict["CommentCount"] = str(data.iloc[i, 18])
			tempDict["FavoriteCount"] = str(data.iloc[i, 19])
			tempDict["ClosedDate"] = str(data.iloc[i, 20])
			tempDict["CommunityOwnedDate"] = str(data.iloc[i, 21])
			
			if (i % 1000 == 0): 
				print("entry: " + str(i) + " of " + str(data.shape[0]))
			w.writerow(tempDict)
		except:
			print("Total skips = " + str(skips)) #keep track of how many strings were skipped 
			skips += 1
			continue
	
def sortCSV(args):
	pythonData = pandas.read_csv(args.write_file, sep=',', error_bad_lines=False)
	#Sort the data by politeness values
	pythonData = pythonData.sort_values(by='PolitenessConfidence', ascending=False)

def createSample(args):
	#Create Sample file
	temp = pythonData.iloc[0:20, :]
	bottom = pythonData.iloc[-38:-18, :]
	temp = temp.append(bottom, ignore_index=True)

	temp = temp.sample(frac=1).reset_index(drop=True)
	temp.to_csv(str(args.write_file) + "_TEST.csv")
	

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Politeness_Classifier")
	parser.add_argument('--read_file', type=str, help='File to read from')
	parser.add_argument('--write_file', type=str, help='File to write to')
	args = parser.parse_args()

	if (args.read_file or args.write_file) is None:
		print("To run this program a read and write file are necessary")
		print("Declare these files with --read_file and --write_file")
		exit

	print("Read file = " + args.read_file)
	print("Write file = " + args.write_file)

	write(args)
	#sortCSV(args)
	#createSample(args)





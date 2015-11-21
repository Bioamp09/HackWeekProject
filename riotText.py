import json
import requests
import os
import sys
apiKey = 'api_key=56e4a12d-bbdd-4572-9722-368d93494a51'
getNameRequest = "https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/"
getRankedStats = "https://na.api.pvp.net/api/lol/na/v1.3/stats/by-summoner/"
rankedStats = "/ranked?season=SEASON2015&"
championParse = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/"
champParseTwo = "?" + apiKey

#os.remove("test.txt")
#print("Succesussfully removed a file!")


#summoner = requests.get("https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/Bioamp09?api_key=56e4a12d-bbdd-4572-9722-368d93494a51");
#r.json
#print summoner.content

summonerRequest = raw_input('What summoner would you like to find? ')
#print summonerRequest
fullRequest = getNameRequest + summonerRequest + '?' + apiKey
#print fullRequest
newRequest = requests.get(fullRequest)
#print newRequest.content

#x = unicode(newRequest.content, 'latin-1')

#x = json.loads(x)

#print x['stcloud']['id']

#print ('\n\n\n')
#print x
#print ('\n\n\n')


jsonInfo = open('info.json','w+')
jsonInfo.write(newRequest.text)
jsonInfo.close();

with  open('info.json', 'rw+') as jsonRead:
	jsonLoad = json.load(jsonRead)
	with open('output.json', 'w+') as output:
		json.dump(jsonLoad, output, sort_keys = True, indent = 4)
		output.close();
	jsonRead.close();

#summonerRequest = raw_input('What summoner would you like to find? ')

#print summonerRequest
#fullRequest = getNameRequest + summonerRequest + '?' + apiKey
#print fullRequest
#newRequest = requests.get(fullRequest)
#print newRequest.content
#print ('Now Looking Up Ranked Stats...\n\n\n')
try:
	with open('output.json', 'r') as sumId:
		loader = json.load(sumId)
		summonerRequest = summonerRequest.replace(" ", "")
		#print summonerRequest
		summonerId = loader[summonerRequest.lower()]['id']
		#print summonerId
		sumId.close()
		rankedLookup = getRankedStats + str(summonerId) + rankedStats + apiKey
		#print rankedLookup
		rankedRequest = requests.get(rankedLookup)
		#print rankedRequest.content
#		os.remove("ranked.json")
#		os.remove("parsedRanked.json")
except ValueError:
	print 'Decoding JSON has failed'
with open('ranked.json', 'rw+') as writeRanked:
	writeRanked.write(rankedRequest.content)
	writeRanked.close()	
with open('ranked.json', 'rw+') as parseRanked:
	parse = json.load(parseRanked)
	with open('parsedRanked.json', 'rw+') as parsed:
		json.dump(parse, parsed, sort_keys = True, indent = 4)
		parsed.close()
	parseRanked.close()

rankedRequest = raw_input('What champion would you like stats for? ')
rankedRequest = rankedRequest.lower()
print("Now searching for champion stats...")

with open('parsedRanked.json', 'rw+') as champ:
	champObj = json.load(champ)
	if champObj == None:
		print 'champObj was null'
		sys.exit(100)
	for value in champObj['champions']:
		
		#champRequest = requests.get(championParse + str(value['id']) + champParseTwo)
		#print str(value['id'])
		print(".")
		
		#sys.stdout.write(".")
		if (str(value['id']) != '0'):
			champRequest = requests.get(championParse + str(value['id']) +  champParseTwo)
			champObj = json.loads(champRequest.content)
			champName = str(champObj['name'])
			#print champName + ('\n')
			if(rankedRequest == champName.lower()):
				print ('\nSuccessfully found ' + rankedRequest)
				print ('Total Kills on ' + rankedRequest.upper() + ': ' + str(value['stats']['totalChampionKills']))
				print ('Double Kills: ' + str(value['stats']['totalDoubleKills']))
				print ('Triple Kills: ' + str(value['stats']['totalTripleKills']))
				print ('Quadra Kills: ' + str(value['stats']['totalQuadraKills']))
				print ('Penta Kills: ' + str(value['stats']['totalPentaKills']))
				kda = float(float((value['stats']['totalChampionKills']+value['stats']['totalAssists']))/value['stats']['totalDeathsPerSession'])
				print ('KDA: %.2f' % kda)
				break
				#print ('this should print, and it does\n\n\n')
			
		else:
			#print('this shouldnt pring, and it doesnt\n\n\n')
			continue
		#print champRequest.content
		#champLoad = json.load(champRequest.content)
		#champName = champRequest['key'].lower()
		#if (rankedRequest == champName):
		#	identifier = str(value['id'])
		#	break
	#print identifier
		
def main():
	print('To keep using this application, be sure to delete the contents of ranked.json and parsedRanked.json')


main()

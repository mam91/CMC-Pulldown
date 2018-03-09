import requests
import pyodbc
import json
	
def loadConfig(filename):
	config = open(filename)
	data = json.load(config)
	return data
	
def convertNullStr(stringVal):
	if(stringVal == ''):
		return "0"
	else:
		return stringVal
	
def main():
	config = loadConfig('cmc-pull.config')
	dbConfig = loadConfig('C:\AppCredentials\CoinTrackerPython\database.config')
	response = requests.get(config[0]["cmc_endpoint"]).json()

	#Pull individual coins
	con = pyodbc.connect(dbConfig[0]["sql_conn"])
	cursor = con.cursor()
	
	for i in range(len(response)):
		params = (response[i]["name"], response[i]["symbol"], response[i]["rank"], response[i]["price_usd"], response[i]["price_btc"], response[i]["24h_volume_usd"], response[i]["market_cap_usd"], response[i]["available_supply"], response[i]["total_supply"], response[i]["max_supply"], response[i]["percent_change_1h"], response[i]["percent_change_24h"], response[i]["percent_change_7d"])
		cursor.execute("{CALL RefreshMarket (?,?,?,?,?,?,?,?,?,?,?,?,?)}", params)
	
	cursor.commit()
	
	#Pull global market down
	response = requests.get(config[0]["cmc_global_endpoint"]).json()
	params = (response["total_24h_volume_usd"], response["total_market_cap_usd"])
	cursor.execute("{CALL RefreshMarketGlobal (?,?)}", params)
	cursor.commit()
		
main()
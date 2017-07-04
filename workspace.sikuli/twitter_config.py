import socket

ipaddrs = socket.gethostbyname(socket.gethostname())

jenkins_scr_tr = "10.10.24.77"
local_development = "10.10.24.103"
jenkins_simple_bp = "10.10.24.44"

# Jenkins SCR/TR Machine
if ipaddrs == jenkins_scr_tr:
	# Access keys for Client twitter account
	consumer_key = "v4sCBP56e3PZsEICO43tq9AxX"
	consumer_secret = "JDqc1QtK9e5tb1nLGq3rhqBIt4dDSWmfOgVIy8w57DHP69pN7G"
	access_token = "735531183321272320-G7ROaV1h9BiOvsn4nDGG8DioX8hkdfy"
	access_token_secret = "T9bvGgD2Y5HDlJWu596lbmHz4je8cSR5hTWkG9usQcOAT"
	tw_screen_name = "poonam_prasher"
	tw_id = "735531183321272320"

	# Access keys for Agent twitter
	agent_consumer_key = "l0pKW2IqeyK7KbIf3mLD5esOM"
	agent_consumer_secret = "CaahMgekMgsPuzqGqt7Xq7HLbu8p01Rs219eRzc3ahFalKTynI"
	agent_access_token = "735475791266500608-3c7e7YFALUd1cLNWf361bT5cchsaauR"
	agent_access_token_secret = "dWXZDAlOaQVEN4Zaf9cPgPutfx1LahxK04lzD77tv2C82"
	tw_agent_screen_name = "naveenprasher1"
	tw_agent_id = "735475791266500608"

# Local Development Machine
elif ipaddrs == local_development:
	# Access keys for Client twitter account
	consumer_key = "UpOWJeXIm0ULao0FMLWo4gl0f"
	consumer_secret = "c86Neu9C1atxwfDGckBxNTY1rFCXOVP3oYKOIaz3HdVV2R52z0"
	access_token = "822409454784131072-NJNyRt881Hnj5nhpfgAlRCs3gQ5hbH1"
	access_token_secret = "ClcB3EDEJFrH232NK27oiapSf3gOjVCNRbXwI4jH2EjdB"
	tw_screen_name = "KumarVedas2015"
	tw_id = "822409454784131072"

	# Access keys for Agent twitter
	agent_consumer_key = "u36jbBXvI9Pt4UYs9hDtcDSIP"
	agent_consumer_secret = "ekp68gAOA4Y7a9ZIuPxoTNN7Kx9RiPKitaT2RsLBvcB7tuwwzq"
	agent_access_token = "788346129754849280-yCxkAJ52IsYiSoHeOUftp2mw1iWiuCK"
	agent_access_token_secret = "jZWidESbZVFDMg32ZHb867X38SAznksnPl8qyWSiwSMzG"
	tw_agent_screen_name = "TechflkSoftware"
	tw_agent_id = "788346129754849280"

# Jenkins Simple BP MAchine
elif ipaddrs == jenkins_simple_bp:
	# Access keys for Client twitter account
	consumer_key = "hS1NKi7wg0Zb2TflcljcIY3GU"
	consumer_secret = "fPfHvsxTeHWd8rzKpHHFwe2LpQrQ0tLdSmbxVR5wr6WNZvFy1k"
	access_token = "735538587370987520-xy2mKeCr0KanPtsXBQUxPGkVbhe3RIU"
	access_token_secret = "3lEGmZvTu1YRTMB4HA5iA17jW1Swdxn4kIEPlynkjA0OW"
	tw_screen_name = "anila_prasher"
	tw_id = "735538587370987520"

	# Access keys for Agent twitter
	agent_consumer_key = "mduYqSvPrDYfDjl1hVgUrmJGp"
	agent_consumer_secret = "n2rAXlhDIEdMplwXTxtFYH3j8PK9pS55dgr2ic62ae41eCIJE9"
	agent_access_token = "737264238109044736-sG82peAmBhTJ6UCtDix2KmuPMKaFXTs"
	agent_access_token_secret = "41u3fg6njxBY9QEWQBzIESmYgS1ACHG78mTXamJc0Bdpa"
	tw_agent_screen_name = "srijan_prasher"
	tw_agent_id = "737264238109044736"
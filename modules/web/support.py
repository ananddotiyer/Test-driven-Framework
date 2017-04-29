import json

def import_from_postman (folder, from_file, to_file):
	import_result = False
	
	from_file = folder + "\\" + from_file

	try:
		line_string = ""
		
		print from_file
		with open (from_file) as fp:
			for line in fp:
				line_string += line.strip ()
				
		dump = json.loads (line_string)
		
		td_category = to_file
		
		to_file = folder + "\\" + to_file + ".py" #to_file doesn't have the extension .py
		fw = open (to_file, "w")
		fw.write ("%s = [\n" % (td_category))
		
		for test in dump["item"]:
			td_test = {}
			td_test["api_name"] = test["name"]
			td_test["api_url"] = test["request"]["url"]
			td_test["api_type"] = test["request"]["method"]
			
			api_header = {}
			for header in test["request"]["header"]:
				api_header[header["key"]] = header["value"]
			
			td_test["api_header"] = api_header
			
			try:
				if test["request"]["body"]["mode"] == "raw":
					td_test["api_params"] = json.loads (test["request"]["body"]["raw"])
			except:
				td_test["api_params"] = {}
			
			td_test["api_function"] = "api_export"
			td_test["api_expected"] = {"response_schema":"write",
									   "schema_file":td_test["api_name"],
									   "specific": 0,
									   "row_json_path":"$",
									   "rowcount":0,} #specific will be interpreted as a boolean in api_object.py
			td_test["api_repl"] = {}
			td_test["api_store"] = {}
			td_test["output_mode"] = 'w'
		
			fw.write (json.dumps (td_test, indent=4) + ",\n") #sort_keys=True
		
		fw.write ("]\n")
		fw.close ()
		
		import_result = True
	except:
		pass
	
	return import_result
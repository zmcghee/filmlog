from conf.secret import ENV_PATH

if ENV_PATH.startswith("/Users"):
	DEBUG = True
else:
	DEBUG = False

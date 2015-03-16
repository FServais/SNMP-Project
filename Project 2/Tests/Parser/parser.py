import re

# Read file
config_file = open('config.txt', 'r')

ip = config_file.readline()
configs = []

for line in config_file:
	configs.append(line)

# Matching the IP
match_ip = re.match('([0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3})/([0-9]{1,2})', ip)
#print "IP:     ", match_ip.group(1)
#print "PREFIX: ", match_ip.group(2)

ip = match_ip.group(1)
prefix = match_ip.group(2)

# tuple containing the IP line
t_ip = (ip, prefix)

# list of tuple containing the fields of the configurations
t_configs = []

# Matching the configurations
for config in configs:
	comp_config = re.compile('([0-9]+) ([123]) (\S+)')
	match_config = re.match(comp_config, config)
	
	if match_config.group(1) is None or match_config.group(2) is None or match_config.group(3) is None:
		continue

	port = match_config.group(1)
	version = match_config.group(2)
	sec_name = match_config.group(3)
	auth_proto = None
	auth_pwd = None
	priv_proto = None
	priv_pwd = None

	if version is "3":
		comp_config = re.compile('([0-9]+) ([123]) (\S+)( (MD5|SHA) (\S*)( (DES|AES) (\S*))?)?')
		match_config = re.match(comp_config, config)
		
		if match_config.group(5) is None or match_config.group(6) is None:
			continue

		auth_proto = match_config.group(5)
		auth_pwd = match_config.group(6)

		if match_config.group(8) is None or match_config.group(9) is None:
			continue

		priv_proto = match_config.group(8)
		priv_pwd = match_config.group(9)

	
#	print port, version, sec_name, auth_proto, auth_pwd, priv_proto, priv_pwd

	t_configs.append((port, version, sec_name, auth_proto, auth_pwd, priv_proto, priv_pwd))

print "Configurations: ", t_configs


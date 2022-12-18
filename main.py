from LogAnalyzer import logAnalyzer

with open("hosts.txt", "r") as f:
    lines = f.readlines()
hosts = [line.strip() for line in lines]

la = logAnalyzer(hosts, "./logs/")

la.get_logs()
la.read_logs()

print(la.logs_df)
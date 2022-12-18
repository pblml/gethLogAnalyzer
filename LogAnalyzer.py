import os
import pandas as pd
from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient
import re, string
from tqdm import tqdm
regex = re.compile('[%s]' % re.escape(string.punctuation))

class logAnalyzer():
    def __init__(self, ip_list=None, log_dir=None):
        self.ip_list = ip_list
        self.log_dir = log_dir
    def ssh_scp_files(self, source_volume, destination_volume, ssh_host, ssh_user="ifm", ssh_password="block"):
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(ssh_host, username=ssh_user, password=ssh_password, look_for_keys=False)

        with SCPClient(client.get_transport()) as scp:
            print(destination_volume)
            scp.get(remote_path=destination_volume, local_path=source_volume, recursive=True)

    def get_logs(self):
        for ip in tqdm(self.ip_list):
            filename = regex.sub('', ip)
            try:
                self.ssh_scp_files(ssh_host=ip, source_volume=f"{self.log_dir}/{filename}.txt", destination_volume="log.txt")
            except Exception as e:
                print(e)
                pass
        return self

    def geth_logs_to_dataframe(self, log_file):
        # Read in the log file as a list of lines
        with open(log_file, "r") as f:
            logs = f.readlines()
        
        # Extract the log data from each line
        log_data = [line.strip().split(None, 2) for line in logs]
        
        # Create a Pandas dataframe from the log data
        df = pd.DataFrame(log_data, columns=["level", "timestamp", "message"])
        
        return df

    def read_logs(self):
        # Create an empty dataframe to store the combined data
        combined_df = pd.DataFrame()
        
        # Loop through all the CSV files in the directory
        for file in tqdm(os.listdir(self.log_dir)):
            if file.endswith(".txt"):
            # Read in the CSV file
            
                df = self.geth_logs_to_dataframe(os.path.join(self.log_dir, file))
                
                # Add the name of the CSV file as a column
                df["filename"] = file
                
                # Append the data to the combined dataframe
                combined_df = combined_df.append(df, ignore_index=True)
        self.logs_df = combined_df

        return self


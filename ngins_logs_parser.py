import re
from user_agents import parse
import pandas as pd
from datetime import datetime


with open('nginx.log') as f:
    log_file = f.readlines()

regexp_patterns = {
    'ipv4': r'^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]?)',
    'time': r'(3[01]|[12][0-9]|[1-9])\/\w{3}\/202[0-9]:(2[0-4]|[01][0-9]):[0-6][0-9]:[0-6][0-9] \+\d{4}',
    'http_method': r'"\w{3,7} ',
    'path': r' (\/\S+){1,5} ',
    'status_code': r'HTTP\/2\.0" \d{3}',
    'bandwidth_part': r'\d{1,3}',
    'referrer': r'https?:\/\/([\w-]{1,32}\.[\w-]{1,32})[^\s@]*',
    'user_agent': r'"Mozilla\/.+"',
}

parsed_data_list = []
for line in log_file:
    ipv4 = re.match(pattern=regexp_patterns['ipv4'], string=line).group()
    time_ = re.search(pattern=regexp_patterns['time'], string=line).group()
    http_method = re.search(pattern=regexp_patterns['http_method'], string=line).group().strip().replace('"', '')
    path = re.search(pattern=regexp_patterns['path'], string=line).group().strip()
    status_code = re.search(pattern=regexp_patterns['status_code'], string=line).group().strip().replace('HTTP/2.0" ', '')
    bandwidth = re.search(pattern=f'{status_code} {regexp_patterns["bandwidth_part"]}', string=line).group().replace(status_code, '').strip()
    referrer = re.search(pattern=regexp_patterns['referrer'], string=line).group().replace('"', '')
    user_agent = re.search(pattern=regexp_patterns['user_agent'], string=line).group().replace('"', '')
    parsed_user_agent = str(parse(user_agent)).split(' / ')
    device = parsed_user_agent[0]
    os = parsed_user_agent[1]
    software = parsed_user_agent[2]

    parsed_data_list.append({
        'ipv4': ipv4,
        'time': time_,
        'http_method': http_method,
        'path': path,
        'status_code': status_code,
        'bandwidth': bandwidth,
        'referrer': referrer,
        'user_agent': user_agent,
        'device': device,
        'os': os,
        'software': software,
    })

df = pd.DataFrame(parsed_data_list)
df.to_csv(f'nginx_logs_parsed_{datetime.today().strftime("%Y-%m-%d")}.csv', index=False, sep='@')

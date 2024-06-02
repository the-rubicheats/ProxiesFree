import requests
import os

# Configuração inicial
repo_owner = 'im-razvan'
repo_name = 'proxy_list'
github_token = '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'  # Seu token de acesso pessoal do GitHub
output_directory = 'C:\\Users\\Administrator\\Pictures\\Proxies\\'  # Caminho de saída atualizado

# Garante que o diretório de saída existe
os.makedirs(output_directory, exist_ok=True)

def download_file(url, filename):
    headers = {'Authorization': f'token {github_token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open(filename, 'w') as file:
            file.write(response.text)
    else:
        print(f'Falha ao baixar o arquivo {filename}')

def get_commits():
    commits_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/commits'
    headers = {'Authorization': f'token {github_token}'}
    params = {'per_page': 100}  # Máximo de commits por página
    all_commits = []

    while commits_url and len(all_commits) < 17761:
        response = requests.get(commits_url, headers=headers, params=params)
        commits = response.json()
        all_commits.extend(commits)
        if 'next' in response.links:
            commits_url = response.links['next']['url']
        else:
            break

    return all_commits[:17761]

def download_files_from_commits(commits):
    for commit in commits:
        sha = commit['sha']
        # URLs para os arquivos específicos em cada commit
        http_url = f'https://raw.githubusercontent.com/{repo_owner}/{repo_name}/{sha}/http.txt'
        socks5_url = f'https://raw.githubusercontent.com/{repo_owner}/{repo_name}/{sha}/socks5.txt'
        
        # Caminhos dos arquivos onde serão salvos
        http_path = os.path.join(output_directory, f'{sha}_http.txt')
        socks5_path = os.path.join(output_directory, f'{sha}_socks5.txt')
        
        # Fazer download dos arquivos
        download_file(http_url, http_path)
        download_file(socks5_url, socks5_path)
        print(f'Arquivos do commit {sha} baixados.')

# Executar o script
commits = get_commits()
download_files_from_commits(commits)

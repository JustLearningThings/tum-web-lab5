import socket
from bs4 import BeautifulSoup
from urllib.parse import unquote

from cache import Cache
from argument_parser import parse_arguments
from page_parser import parse_page

data = b''
def empty_buffer():
    global data
    data = b''

def parse_url(url):
    if '://' in url:
        url = url.split('://')[1]

    parts = url.split('/', 1)
    hostname = parts[0]
    path = '/' + parts[1] if len(parts) > 1 else '/'

    return hostname, path


def request(url: str):
    hostname, path = parse_url(url)

    try:
        global data
        empty_buffer()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((hostname, 80))

            http_request = f"GET {path} HTTP/1.1\r\nHost: {hostname}\r\n\r\n"

            s.sendall(http_request.encode())

            while True:
                chunk = s.recv(4096)

                if not chunk:
                    break

                data += chunk    

        return data.decode()
    except socket.timeout:
            print("Done.\n")

            return None
    except Exception as e:
        print("An error occurred:", e)

        return None
    finally:
        s.close()

def search_term(word):
    print(f'Searching Google for \'{word}\'...')
    request(f'www.google.com/search?q={word}')

    soup = BeautifulSoup(data, 'html.parser')        
    headers = soup.find_all('h3')

    for i, h in enumerate(headers[:10]):
        a = h.find_parent('a')
        print(f'{i + 1}. {h.text}')

        if a:
            link = a.get('href').split('q=')[-1]
            link = unquote(link)
            link = link.split('&sa=')[0]
            print(link)
        else:
            print('- No link -')
        
        print()


def main():
    cache = Cache()    
    url = parse_arguments().url
    search = parse_arguments().search
    
    if url:
        if cache.has(url):
            response = cache.get(url)
            print(f'Getting response for {url} from cache.')
        else:
            request(url)
            response = parse_page(data, cache, url)

        print(f'{"=" * 50}\nResponse from https://{url}\n{"=" * 50}\n{response}\n{"=" * 50}\n')

    if search:
        for word in search:
            delimiter = "=" * 50
            print(f'{delimiter}\nSearch results for {word}\n{delimiter}')
            search_term(word)
            print(delimiter)        


main()

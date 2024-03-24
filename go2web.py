import socket

from cache import Cache
from argument_parser import parse_arguments
from page_parser import parse_page

data = b''
def empty_buffer():
    data = b''

def parse_url(url):
    # Remove the scheme (http://, https://) if present
    if '://' in url:
        url = url.split('://')[1]

    # Split the remaining URL into hostname and path
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



def main():
    url = parse_arguments().url
    search = parse_arguments().search
    
    if url:
        print(f'Searching {url}...')
        request(url)
        response = parse_page(data)

        print(response)

    if search:
        print(search)



main()

import argparse
import socket
from bs4 import BeautifulSoup

data = b''
def empty_buffer():
    data = b''

def parse_arguments():
    parser = argparse.ArgumentParser(description='go2web')
    parser.add_argument('--url', '-u', type=str, help='website URL')
    parser.add_argument('--search', '-s', type=list, help='search the term followed by the flag')

    args = parser.parse_args()

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
            print("Socket timed out.")

            return None
    except Exception as e:
        print("An error occurred:", e)

        return None
    finally:
        s.close()




request('www.google.com')
html_start = data.find(b"\r\n\r\n") + 4
html = data[html_start:]

soup = BeautifulSoup(html, 'html.parser')
for s in soup.select('script'):
    s.extract()
body = soup.find('body')
for e in body.find_all(True):
    if 'style' in e.attrs:
        del e['style']
for style in soup.find_all('style'):
    style.extract()
print(body.text)
from bs4 import BeautifulSoup

def parse_page(data) -> str:
    if data in [b'', None, '', 0, '0']:
        return 'No content.'
    
    html_start = data.find(b"\r\n\r\n") + 4
    html = data[html_start:]
    soup = BeautifulSoup(html, 'html.parser')

    # clean the content
    for s in soup.select('script'):
        s.extract()

    body = soup.find('body')

    for e in body.find_all(True):
        if 'style' in e.attrs:
            del e['style']

    for style in soup.find_all('style'):
        style.extract()

    return body.text
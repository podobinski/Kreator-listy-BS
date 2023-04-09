import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def affiliation_check(url):
    # Add scheme if it's missing
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        url = f'http://{url}'

    bps_found = False
    sgb_found = False

    try:
        response = requests.get(url)  # Re-enable SSL verification
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            links = soup.find_all('a', href=True)

            for link in links:
                href = link['href']

                parsed_href = urlparse(href)
                if parsed_href.netloc.endswith('bankbps.pl'):
                    bps_found = True
                elif parsed_href.netloc.endswith('sgb.pl'):
                    sgb_found = True

                if bps_found and sgb_found:
                    break

        else:
            return f"Request failed with status code {response.status_code}"
    except requests.exceptions.SSLError as e:
        return f"SSL Error: {str(e)} for URL {url}"
    except Exception as e:
        return f"Error: {str(e)} for URL {url}"

    if bps_found and sgb_found:
        return "BPS i SGB"
    elif bps_found:
        return "BPS"
    elif sgb_found:
        return "SGB"
    else:
        return "nie znaleziono"

# Example usage
url = "https://example.com"
result = affiliation_check(url)
print(result)

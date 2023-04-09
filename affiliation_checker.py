import requests


def affiliation_check(website_url):
    try:
        response = requests.get(website_url)
        source_code = response.text

        bps_present = "BPS" in source_code
        sgb_present = "SGB" in source_code

        if bps_present and sgb_present:
            return "BPS i SGB"
        elif bps_present:
            return "BPS"
        elif sgb_present:
            return "SGB"
        else:
            return "nie znaleziono"
    except Exception as e:
        print(f"Error checking affiliation for {website_url}: {e}")
        return "nie znaleziono"

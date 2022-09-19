import requests
from bs4 import BeautifulSoup


def main():
    url = 'https://www.eia.gov/dnav/pet/pet_cons_prim_dcu_nus_m.htm'
    page = requests.get(url)


if __name__ == "__main__":
    main()
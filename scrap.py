from bs4 import BeautifulSoup
import requests
import pandas as pd

EBIT_URL = (
    "https://www.biznesradar.pl/spolki-raporty-finansowe-rachunek-zyskow-i-strat/"
    "indeks:WIG20,Y,IncomeEBIT,2,2,0"
)
AMORTISATION_URL = (
    "https://www.biznesradar.pl/spolki-raporty-finansowe-przeplywy-pieniezne/"
    "indeks:WIG20,Y,CashflowAmortization"
)
HEADERS = {"User-Agent": "Mozilla/5.0"}
REQUEST_TIMEOUT = 15

# Banks are excluded — they report under different income-statement standards
# and EBIT + amortisation doesn't map cleanly to EBITDA for them.
EXCLUDED_TICKERS = {"SPL1", "PEO", "PKO"}


def scrape_metric(url: str, column: str) -> pd.DataFrame:
    resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")
    rows = []
    for tr in soup.find_all("tr")[1:]:
        name_tag = tr.find("a")
        value_tag = tr.find("span", class_="pv")
        if not name_tag or not value_tag or not value_tag.span:
            continue
        rows.append(
            {"Name": name_tag.text.strip(), column: value_tag.span.text.replace(" ", "")}
        )
    return pd.DataFrame(rows)


def compute_ebitda() -> pd.DataFrame:
    ebit = scrape_metric(EBIT_URL, "EBIT")
    amort = scrape_metric(AMORTISATION_URL, "Amortisation")

    df = ebit.merge(amort, on="Name")
    df["EBIT"] = pd.to_numeric(df["EBIT"], errors="coerce")
    df["Amortisation"] = pd.to_numeric(df["Amortisation"], errors="coerce")
    df["EBITDA"] = df["EBIT"] + df["Amortisation"]

    df = df[~df["Name"].isin(EXCLUDED_TICKERS)]
    return df[["Name", "EBITDA"]].set_index("Name").dropna()


if __name__ == "__main__":
    print(compute_ebitda())

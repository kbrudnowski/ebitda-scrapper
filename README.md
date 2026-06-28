# ebitda-scrapper

Scrapes EBIT and amortisation figures for WIG20 companies from [biznesradar.pl](https://www.biznesradar.pl) and computes EBITDA. The site normally gates this data behind a premium account; this script reconstructs it from publicly available financial statement pages.

Banks (SPL1, PEO, PKO) are excluded — their income statements follow different conventions and the EBIT + amortisation formula doesn't apply cleanly.

## Install

```
pip install -r requirements.txt
```

## Run

```
python scrap.py
```

Prints a dataframe of WIG20 non-bank tickers and their EBITDA (in thousands PLN, as reported on biznesradar.pl).

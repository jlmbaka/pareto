__author__ = "jeanlouis.mbaka"

import pandas as pd
import numpy as np

if __name__ == "__main__":
	data = pd.read_excel("september2014-2.xlsx")
	byArticle = data.groupby("Article", sort=True).sum()
	print(byArticle)
	# print(byArticle["Consommation valorisee"].describe())
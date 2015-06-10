__author__ = "jeanlouis.mbaka"

import csv
import sys

import pandas as pd
import numpy as np


class Pareto():
	def __init__(self):
		pass

	def read_data(self, filename):
		"""
		Read data from filename
		"""
		results = read_csv(filename)
		self.header = results[0]
		self.raw_data = results[1]
		self.data = self.raw_data

	def write_data(self, filename):
		"""
		Write data to filename
		"""
		write_csv(filename, self.header, self.data)

	def format_data(self):
		pass

	def pareto(self):
		"""
		Pareto analysis
		"""
		self.valorised_consumption()
		self.cumulative_valorised_consumption()
		self.abc_segmentation()
		self.fmr_segmentation()

	def valorised_consumption(self):
		"""
		computes the valorised consumption.
		"""
		self.header.append("consommation valorisee")

		num_of_data = len(self.data)
		print(num_of_data)
		for i in range(num_of_data):
			try:
				monthly_consumption = self.data[i][1]
				unit_price = self.data[i][2]
				self.data[i].append(unit_price * monthly_consumption)
			except IndexError:
				print("faulty index = {}".format(i))
				print("len(self.data) = {}".format(len(self.data)))
				print(self.data[i])
				sys.exit(2)
			
	def cumulative_valorised_consumption(self):
		"""
		Sorted and cumululative consumption.
		"""
		self.header.append("consommation cumulee")
		self.data = sorted(self.data, key=lambda row: row[-1], reverse=True) # sort by valorised consumption		
		for index in range(len(self.data)):
			if index == 0:
				self.data[index].append(self.data[index][-1])
			else:
				self.data[index].append(self.data[index][-1] + self.data[index-1][-1])
		
		self.print_debug(heading="sorted cumulalive valorised consumption")

	def abc_segmentation(self):
		"""
		ABC segmentation.
		"""
		self.header.append("PCT cumule")
		self.header.append("ABC Categorie")

		for index in range(len(self.data)):
			cumulative_pct_consumption = self.data[index][-1] / self.data[-1][-1]
			self.data[index].append(cumulative_pct_consumption)
			if (cumulative_pct_consumption <= 0.8):
				self.data[index].append("A")
			elif (cumulative_pct_consumption > 0.8 and cumulative_pct_consumption <= 0.95):
				self.data[index].append("B")
			else:
				self.data[index].append("C")
		
		self.print_debug(heading="ABC Segmentation")

	def fmr_segmentation(self):
		"""
		FRM Segmention.
		"""
		self.header.append("QTY cumule")
		self.header.append("FMR Categorie")
		# cumulative quantity
		# 	sort by quantity
		self.data = sorted(self.data, key=lambda row:row[1], reverse=True)
		# 	compute cumulative quantities
		for index in range(len(self.data)):
			if index == 0:
				self.data[index].append(self.data[index][1])
			else:
				self.data[index].append(self.data[index][1] + self.data[index-1][-1])

		# FRM Segmentation
		for index in range(len(self.data)):
			cumulative_pct_qty = self.data[index][-1] / self.data[-1][-1]
			self.data[index].append(cumulative_pct_qty)
			if (cumulative_pct_qty <= 0.8):
				self.data[index].append("F")
			elif (cumulative_pct_qty > 0.8 and cumulative_pct_qty <= 0.95):
				self.data[index].append("M")
			else:
				self.data[index].append("R")
		self.print_debug(heading="ABC/FMR Segmention")

	def print_debug(self, heading=""):
		print("<====={}=====>".format(heading))
		print(self.header)
		[print(row) for row in self.data]

def read_csv(filename):
	"""
	Read a csv file and print the content row by row
	:param filename: name/path to the csv file
	"""
	delimiter = ";"

	header = []
	data = []

	with open(filename, 'rt') as csv_file:
		reader = csv.reader(csv_file, dialect='excel-tab') # type CSV.READER
		i = 0
		for row in reader:
			row_content = row[0] # in excel-tab dialect, a row is an array containing one str
			row_content = str.split(row_content, delimiter) # split the string by ;

			# header content
			if i == 0:
				header = row_content
				i += 1
				continue

			# data content
			data_row = []
			for item in row_content:
				if str.strip(item) == "":
					break
				try:
					data_row.append(float(item.replace(",", ".")))
				except ValueError:
					data_row.append(item)

			if data_row != []:
				data.append(data_row)
			i += 1
	return [header, data]

def write_csv(filename, header, data):
	"""
	Write paretor data to csv
	:param filename: output filename
	"""
	with open(filename, 'wt') as csv_file:
		writer = csv.writer(csv_file, dialect="excel")
		writer.writerow(header)
		for row in data:
			writer.writerow(row)

def parse_filename():
	"""
	:return: filename
	"""
	filename = ""
	if (len(sys.argv) > 1):
		filename = sys.argv[1]
	else:
		sys.exit(2)
	return filename


if __name__ == "__main__":
	my_pareto = Pareto()
	filename = parse_filename()
	my_pareto.read_data(filename)
	my_pareto.pareto()
	my_pareto.write_data("{}_pareto.csv".format(filename))
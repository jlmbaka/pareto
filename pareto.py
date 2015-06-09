__author__ = "jeanlouis.mbaka"


import csv
import sys


class Pareto():
	def __init__(self):
		pass

	def read_data(self, filename):
		"""
		"""
		results = read_csv(filename)
		print(results)
		self.header = results[0]
		self.data = results[1]

	def compute_pareto(self):
		"""
		"""
		self.valorised_consumption()
		self.cumulative_valorised_consumption()
		self.abc()

	def valorised_consumption(self):
		"""
		computes the valorised consumption.
		"""
		num_of_data = len(self.data)
		self.data[0].append("consommation valorisee")

		for i in range(1,num_of_data):
			monthly_consumption = self.data[i][1]
			unit_price = self.data[i][2]
			self.data[i].append(unit_price * monthly_consumption)
			print(self.data[i]) # debug
			

	def cumulative_valorised_consumption(self):
		"""
		"""
		print(self.data)
		sorted(self.data, key=lambda row: row[-1]) # sort by valorised consumption
		

	def abc(self):
		"""
		"""
		pass


def read_csv(filename):
	"""
	Read a csv file and print the content row by row
	:param filename: name/path to the csv file
	"""
	delimiter = ";"
	print(csv.list_dialects())
	header = []
	data = []
	with open(filename, 'rt') as csv_file:
		reader = csv.reader(csv_file, dialect='excel-tab') # type CSV.READER
		i = 0
		for row in reader:
			row_content = row[0]
			row_content = str.split(row_content, delimiter)

			if (i==0):
				header = row_content
				continue

			result = []
			for item in row_content:
				try:
					result.append(float(item.replace(",", ".")))
				except ValueError:
					result.append(item)
			data.append(result)
			print(result) # debug
			i += 1
	return [header, data]


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
	pareto = Pareto()
	filename = parse_filename()
	pareto.read_data(filename)
	pareto.compute_pareto()
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
		self.header = results[0]
		self.data = results[1]

	def pareto(self):
		"""
		"""
		self.valorised_consumption()
		self.cumulative_valorised_consumption()
		self.abc_segmentation()

	def valorised_consumption(self):
		"""
		computes the valorised consumption.
		"""
		self.header.append("consommation valorisee")

		num_of_data = len(self.data)
		for i in range(num_of_data):
			monthly_consumption = self.data[i][1]
			unit_price = self.data[i][2]
			self.data[i].append(unit_price * monthly_consumption)
			
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
		self.header.append("Categorie")

		for index in range(len(self.data)):
			cumulative_pct = self.data[index][-1] / self.data[-1][-1]
			self.data[index].append(cumulative_pct)
			if (cumulative_pct <= 0.8):
				self.data[index].append("A")
			elif (cumulative_pct > 0.8 and cumulative_pct <= 0.95):
				self.data[index].append("B")
			else:
				self.data[index].append("C")
		
		self.print_debug(heading="ABC Segmentation")

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

			if (i==0):
				header = row_content
				i += 1
				continue

			data_row = []
			for item in row_content:
				try:
					data_row.append(float(item.replace(",", ".")))
				except ValueError:
					data_row.append(item)
			data.append(data_row)
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
	my_pareto = Pareto()
	filename = parse_filename()
	my_pareto.read_data(filename)
	my_pareto.pareto()
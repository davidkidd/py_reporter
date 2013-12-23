import io
import csv

class Reporter:

	def __init__(self, name="", rows=[]):
		self.name = name
		self.rows = rows
		self.header_row = []

		self.max_columns = 0
		self.widths = {}

		self.auto_widths = []
		self.default_auto_width_min = 20

		self.default_width = 20
		self.default_header_padding_symbol = " "
		self.default_cell_padding_symbol = ' '
		self.default_col_padding_symbol = '|'
		self.default_header_line_symbol = '-'
		self.default_col_padding = 1
		self.default_fill_empty_symbol = ''
		self.add_header_separator = True

		self.justification_options = ["<", ">", "^"]
		self.default_cell_justification = "<"
		self.default_header_justification = "^"
		self.justifications = {}

	def add_row(self, row, header=False):
		if header:
			self.header_row = row
		else:
			self.rows.append(row)
		cols = len(row)
		for c in range(cols):
			if c not in self.widths:
				self.widths[c] = self.default_width

			if c not in self.justifications:
				self.justifications[c] = self.default_cell_justification
		
		self.max_columns = max(self.max_columns, len(row))

	def auto_adjust_col_widths(self):
		for col in self.auto_widths:
			self.widths[col] = len(self.header_row[col])
			for row in self.rows:
				self.widths[col] = max(self.widths[col], len(str(row[col])))
			self.widths[col] = max(self.widths[col], self.default_auto_width_min)

	def set_auto_col_width(self, *indexes):
		if len(indexes) == 0:
			for col in range(self.max_columns):
				self.auto_widths.append(col)
		else:
			for i in indexes:
				if not i in self.auto_widths:
					self.auto_widths.append(i)

	def add_header_row(self, header):
		self.add_row(header, True)

	def set_column_width(self, col_index, width):
		self.widths[col_index] = width

	def set_cell_justification(self, col_index, justification):
		if justification not in self.justification_options:
			print "Justification symbol", justification, "is not valid."
		else:
			self.justifications[col_index] = justification

	def set_default_cell_justification(self, justification):
		self.default_cell_justification = justification
		for cell in self.justifications.keys():
			self.justifications[cell] = self.default_cell_justification

	def adjust_row(self, row, use_fill_char=True):
		col_diff = self.max_columns - len(row)
		if col_diff > 0:
			for i in range(col_diff):
				if (use_fill_char):
					row.append(self.default_fill_empty_symbol) 
				else:
					row.append('')


	def get_html_table(self, title=True, border=1):
		table_html = '<table border="' + str(border) + '">'
		if title and len(self.name) > 0:
			table_html += "<caption>" + self.name + "</caption>"
		if self.header_row:
			table_html += "<thead><tr>"
			for header in self.header_row:
				table_html += "<th>" + header + "</th>"
			table_html += "</tr></thead>"

		table_html += "<tbody>"
		for r in self.rows:
			table_html += "<tr>"
			for cell in r:
				table_html += "<td>" + cell + "</td>"
			table_html += "</tr>"
		table_html += "</tbody>"
		table_html += "</table>"
		
		return table_html

	def get_csv(self, title=True, fill_empty=True):
		output = io.BytesIO()
		writer = csv.writer(output)

		if title:
			if fill_empty:
				self.adjust_row(self.header_row)
			writer.writerow(self.header_row)

		for row in self.rows:
			if fill_empty:
				self.adjust_row(row)
			writer.writerow(row)

		return output.getvalue()

	def __str__(self):
		output = []
		# Adjust all rows to fill empty cells
		self.adjust_row(self.header_row)

		sep_row = []
		self.adjust_row(sep_row, False)

		for r in self.rows:
			self.adjust_row(r)

		# Before printing anything, make auto adjustments to col widths
		self.auto_adjust_col_widths()

		# Add title
		if len(self.name) > 0:
			table_width = sum(self.widths.values())
			table_fmt = '{:^%d}' % table_width
			output.append(table_fmt.format(self.name))

		header_fmt = self.default_col_padding_symbol.join(
			['{%d:%s%s%d}' % (	i, 
								self.default_header_padding_symbol, 
								self.default_header_justification, 
								self.widths[i] + self.default_col_padding*2)
				for i in range(self.max_columns)])

		output.append(header_fmt.format(*self.header_row))

		# Output header separator, if required
		if self.add_header_separator:
			sep_fmt = self.default_col_padding_symbol.join(
				['{%d:%s%s%d}' % (	i, 
									self.default_header_line_symbol, 
									self.default_header_justification, 
									self.widths[i] + self.default_col_padding*2)
					for i in range(self.max_columns)])

			output.append(sep_fmt.format(*sep_row))

		# Output data

		fmt = self.default_col_padding_symbol.join(
			['{%d:%s%s%d}' % (	i, 
								self.default_cell_padding_symbol, 
								self.justifications[i],
								self.widths[i] + self.default_col_padding*2)
				for i in range(self.max_columns)])

		for r in self.rows:
			output.append(fmt.format(*r))

		return "\n".join(output)
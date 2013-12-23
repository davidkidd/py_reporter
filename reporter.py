import io
import csv

class Reporter:

	def __init__(self, name="", rows=[]):
		self.name = name
		self.rows = rows
		self.header_row = []

		self.max_columns = 0
		self.widths = {}
		self.width_overrides = {}

		self.auto_widths = []
		self.default_auto_width_min = 20

		self.default_width = 20
		self.default_header_padding_symbol = " "
		self.default_cell_padding_symbol = ' '
		self.default_col_padding_symbol = '|'
		self.default_header_line_symbol = '-'
		self.default_col_padding = 1
		self.default_fill_empty_symbol = ' '
		self.add_header_separator = True

		self.justification_options = ["<", ">", "^"] # Represents left, right and centre justification
		self.default_cell_justification = "<"
		self.default_header_justification = "^"
		self.justifications = {}

	def set_title(self, name):
		"""
		Sets the title of the table. This may be added to the output, depending on output method.
		"""
		self.name = name;

	def set_empty_cell_character(self, char):
		"""
		If the table contains rows of irregular length, shorter rows will be appended with empty cells filled with this character.
		"""
		self.default_fill_empty_symbol = char

	def add_row(self, row, header=False):
		"""
		Adds a row or header row, updates the max number of columns and assigns 
		default column widths and justification option if not previously set.
		"""
		if header:
			self.header_row = row
		else:
			self.rows.append(row)
		
		""" 
		Check if the number of columns is greater than what we've seen previously.

		If it is, then adjust the max columns and configure some defaults.
		"""
		cols = len(row)

		if cols > self.max_columns:
			
			self.max_columns = cols

			for c in range(cols):
				# Make sure the column key is recorded
				if c not in self.widths:
					self.widths[c] = self.default_width

				if c not in self.justifications:
					self.justifications[c] = self.default_cell_justification

	def auto_adjust_col_widths(self):
		"""
		Finds the max width of all cells in a row, adjusting the overall col width as it goes along.
		"""
		for col in self.auto_widths:
			self.widths[col] = len(self.header_row[col])
			for row in self.rows:
				self.widths[col] = max(self.widths[col], len(str(row[col])))
			self.widths[col] = max(self.widths[col], self.default_auto_width_min)

	def apply_col_width_overrides(self):
		"""
		Applies width overrides to the final col width.
		"""
		for c in range(self.max_columns):
			if c in self.width_overrides:
				self.widths[c] = self.width_overrides[c]
			else:
				self.widths[c] = self.default_width

	def set_auto_col_width(self, *indexes):
		"""
		Specify which columns should auto adjust to the largest cell. 
		If no indices supplied, all columns will auto adjust.
		"""
		if len(indexes) == 0:
			for col in range(self.max_columns):
				self.auto_widths.append(col)
		else:
			for i in indexes:
				if not i in self.auto_widths:
					self.auto_widths.append(i)

	def add_header_row(self, header):
		"""
		Records the header row separately, so it can be distinctly formatted and tagged appropriately for HTML output.
		"""
		self.add_row(header, True)


	def set_default_column_width(self, width):
		"""
		The default column width will apply to any column that has not been explicitly assigned a width via
		set_column_width(), or has not been set to auto adjust.

		"""
		self.default_width = width

	def set_column_width(self, col_index, width):
		"""
		Specify a max width for a column. If not specified, a default value will be assigned.

		To automatically adjust the column width, use:
			set_auto_col_width(col_index)
		"""
		self.width_overrides[col_index] = width

	def set_column_justification(self, col_index, justification):
		"""
		Change justification type for column:

			'<': left
			'>': right
			'^': centre

		"""
		if justification not in self.justification_options:
			print "Justification symbol", justification, "is not valid."
		else:
			self.justifications[col_index] = justification

	def set_default_column_justification(self, justification):
		"""
		Change default justification type for non-specified columns. See set_column_justification() for valid symbols.

		"""
		self.default_cell_justification = justification
		for cell in self.justifications.keys():
			self.justifications[cell] = self.default_cell_justification

	def adjust_row(self, row, use_fill_char=True):
		"""
		Adjusts the row to add empty cells if the row contains fewer cells than the table's max columns.

		Because it must first record every row before knowing many columns are in the table, it must be called when all rows
		have been added to the Reporter object. Consequently, this is only called when the table is output.

		By default, a fill character will also be added. Use set_empty_cell_character() to specify a different fill character. 

		Note that this will become the new default fill character for subsequent row adjustments.

		"""
		col_diff = self.max_columns - len(row)
		if col_diff > 0:
			for i in range(col_diff):
				if (use_fill_char):
					row.append(self.default_fill_empty_symbol) 
				else:
					row.append('')


	def get_html_table(self, title=True, fill_empty=True, border=1):
		"""Outputs the rows as a standard HTML table. """
		table_html = '<table border="' + str(border) + '">'
		if title and len(self.name) > 0:
			table_html += "<caption>" + self.name + "</caption>"
		if self.header_row:
			table_html += "<thead><tr>"

			if fill_empty:
					self.adjust_row(self.header_row)
			
			for header in self.header_row:

				table_html += "<th>" + header + "</th>"
			table_html += "</tr></thead>"

		table_html += "<tbody>"
		for r in self.rows:

			if fill_empty:
				self.adjust_row(r)

			table_html += "<tr>"
			for cell in r:
				table_html += "<td>" + cell + "</td>"
			table_html += "</tr>"
		table_html += "</tbody>"
		table_html += "</table>"
		
		return table_html

	def get_csv(self, header=True, fill_empty=True):
		"""
		Outputs the rows as a string in a CSV format. 

		The format is the default format used by Python's csv module.

		"""
		output = io.BytesIO()
		writer = csv.writer(output)

		if header:
			if fill_empty:
				self.adjust_row(self.header_row)
			writer.writerow(self.header_row)

		for row in self.rows:
			if fill_empty:
				self.adjust_row(row)
			writer.writerow(row)

		return output.getvalue()

	def __str__(self):
		"""
		Prints all rows, according to column widths (including auto widths) and justification options.

		The table title and header row will also be added, if available.

		"""

		output = []
		# Adjust all rows to fill empty cells
		self.adjust_row(self.header_row)

		sep_row = []
		self.adjust_row(sep_row, False)

		for r in self.rows:
			self.adjust_row(r)

		# Before printing anything, make auto adjustments to cols flagged as being auto adjustable
		self.auto_adjust_col_widths()

		# If any columns have a hard width set, apply it now
		self.apply_col_width_overrides()

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
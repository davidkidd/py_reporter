py_reporter
===========

A simple Python module for easy column printing.

Just feed py_reporter each row as a list, and it will auto adjust widths, pad cells, handle irregular row lengths, justify text, add a title, and more - see default variables.

For example:

	  reporter = Reporter()
	  
	  reporter.add_header(["Filename", "SHA256"])
	  
	  for row in get_records_from_somewhere():
	    reporter.add_row(row)
	    
	  reporter.set_auto_col_width()
	  
	  print reporter
  
Outputs:

	            Filename          |                              SHA256                              
	  ----------------------------|------------------------------------------------------------------
	  TotalEclipseOfTheHeart.txt  |14e872388fcfc8c7bec73fbfbf8d35999d09a925d02b3c51c78dae38e4e6781b  
	  GoodByeToTheIsland.txt      |2146ffb2c919b7bda7f0dfe1d9077e3ac45e1e238b215c201df59d79d78ee4a0  
	  AllInOneVoice.txt           |346136668cb2fc843d4313daeaeba49732e0ccdd8c3ee46694f7227c05ee9d0d  
	  TheWorldStartsTonight.txt   |e3b3b130e6d290bd8fc77346b310cb965c14b14a74e06bc5a94be63dc2652658  
	  DiamondCut.txt              |8967d7e2accf4e6752ae9b8c4ab58ce22aec26287f3225b91e63cba7bcf37d85

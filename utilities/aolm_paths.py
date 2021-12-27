
data_paths = {}
data_paths["root"] = "..{0}..{0}data{0}".format(os.sep)

data_paths["dickinson"] = {
	
	"bolts": "{0}dickinson{1}bingham{1}processed{1}".format(data_paths["root"], os.sep) + \
			 "bingham_bolts_of_melody_internetarchive_accessed021021_processed.txt",

	"eda": "{0}dickinson{1}eda{1}tei{1}".format(data_paths["root"], os.sep)
}

data_paths["hathi"] = { }

data_paths["twain"] = { 

	"autobio": "{0}twain{1}autobiography{1}tei{1}". format(data_paths["root"], os.sep),
}
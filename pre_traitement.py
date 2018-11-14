import os

input_directory = "annotated_job_offers"
output_directory = "jo"

def verify_annotation(current_line):
	words = current_line.split("\t")
	if len(words) < 2:
		word = words[0]
		if "\n" in word:
			word = word[:-1]
		line = "\t".join([word, "O"]) + "\n"
	else:
		annotation = words[1]
		if annotation == "\n":
			annotation = "O"
		if "\n" in annotation:
			annotation = annotation[:-1]
		classification = annotation.split(" ")
		if len(classification) > 1:
			union = "_".join(classification)
			line = "\t".join([words[0], union]) + "\n"
		else:
			line = "\t".join([words[0], annotation]) + "\n"
	return line

def verify_file(input_directory, output_directory, file_name):
	input_file_name = os.path.join(input_directory, file_name)
	output_file_name = os.path.join(output_directory, file_name)
	with open(output_file_name, "w") as output:
		with open(input_file_name, "r") as input:
			line = input.readline()
			while line:
				output.write(verify_annotation(line))
				line = input.readline()

def verify_directory(input_directory, output_directory, first_file=1, last_file=5428):
	file_list = sorted(os.listdir(input_directory))[first_file-1:last_file]
	for counter, file in enumerate(file_list):
		verify_file(input_directory, output_directory, file)
		print("Element {}\{} - File {} reviewed".format(str(counter+first_file), last_file, file))



if __name__ == "__main__":
	# 5428 file max
	verify_directory(input_directory, output_directory)

import os

path_directory = os.getcwd()
job_offers_directory = os.path.join(path_directory, 'jo')
train_number = 250
test_number = 5428-train_number-1
start = 1
gz_name = str(train_number) + "train-" + str(test_number) + "test"
if start != 1:
    gz_name += "-" + str(start) + "start"
gz_name = "ner-model." + gz_name + ".gz"

def list_elements_in_file(list_elements):
    tsv_list = ""
    for file_name in list_elements:
        tsv_list += os.path.join('jo', file_name + ",")
    tsv_list = tsv_list[:-1]
    return tsv_list

def build_train_and_test_list(path_directory, train_number, test_number, start):
    list = os.listdir(path_directory)
    train_list = list_elements_in_file(sorted(os.listdir(path_directory))[start-1:start-1+train_number])
    test_list = list_elements_in_file(sorted(os.listdir(path_directory))[start-1+train_number:start-1+train_number+test_number])
    return train_list, test_list

def write_austen_prop(train_list, archive_name):
    with open("austen.prop", "w") as new_file:
        with open("original_austen.prop", "r") as original_file:
            line = original_file.readline()
            while line:
                if "trainFile" in line:
                    if len(train_list) == 1:
                        line = "trainFile = " + train_list + "\n"
                    else:
                        line = "trainFileList = " + train_list + "\n"
                    new_file.write(line)
                elif "serializeTo" in line:
                    line = "serializeTo = " + archive_name + "\n"
                    new_file.write(line)
                else:
                    new_file.write(line)
                line = original_file.readline()

def train_model():
    with open("train_model.sh", "w") as file:
        command = "java -Xms4g -Xmx16g -cp stanford-ner.jar edu.stanford.nlp.ie.crf.CRFClassifier -prop austen.prop"
        file.write(command)

def test_model(archive_name, test_list):
    if "," in test_list:
        test = " -testFiles "
    else:
        test = " -testFile "
    with open("test_model.sh", "w") as file:
        command = "java -Xms4g -Xmx16g -cp stanford-ner.jar edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier " +  archive_name + test + test_list
        file.write(command)

def main():
    train_list, test_list = build_train_and_test_list(job_offers_directory, train_number, test_number, start)
    write_austen_prop(train_list, gz_name)
    train_model()
    test_model(gz_name, test_list)

def main_final_conl():
    train_list = os.path.join("jo","final_conl.tsv")
    write_austen_prop(train_list, "ner-model.final_conl.gz")
    train_model()

if __name__ == "__main__":
    main_final_conl()
    print("\n\n.......... BUILD MODEL ..........\n\n")
    os.system("sh train_model.sh")
    #print("\n\n.......... TEST MODEL ..........\n\n")
    #os.system("sh test_model.sh")

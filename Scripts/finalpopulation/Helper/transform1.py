
from __future__ import division
import os



def read_file_return_list(filename):
    return open("../"+filename, "r").readlines()

def get_dataset(filename):
    convert_names = {"CPM_APACHE": "../../../Problems/CPM/data/Apache_AllMeasurements.csv",
                     "CPM_BDBC": "../../../Problems/CPM/data/BDBC_AllMeasurements.csv",
                     "CPM_BDBJ": "../../../Problems/CPM/data/BDBJ_AllMeasurements.csv",
                     "CPM_LLVM": "../../../Problems/CPM/data/LLVM_AllMeasurements.csv",
                     "CPM_SQL": "../../../Problems/CPM/data/SQL_AllMeasurements.csv",
                     "cpm_X264": "../../../Problems/CPM/data/x264_AllMeasurements.csv"
                     }
    filename = convert_names[filename]
    temp_list = open(filename, "r").readlines()[1:]
    temp_list = [t.replace("\r\n", "") for t in temp_list]
    # content = [[[",".join(map(str, t[:-1])), t[-1]] for t in line.split(",")] for line in temp_list]
    content = {}
    rank_list = []
    for t in temp_list:
        temp = t.replace("Y","1").replace("N", "0").split(",")
        content[",".join(temp[:-1])] = float(temp[-1])
        rank_list.append(float(temp[-1]))

    return content, sorted(rank_list)



def validate(solution):
    if sum(solution) == 0: return False
    if solution[0] != 1: return False
    if solution[1] != 1: return False
    if solution[2] != 1: return False
    if sum([solution[3], solution[4]]) != 1: return False
    if solution[4] == 1 and solution[5] != 1: return False
    if solution[4] == 0 and sum(solution[5:10]) != 0: return False
    if solution[4] == 1 and solution[6] != 1: return False
    if solution[6] == 1 and sum([solution[7], solution[8]]) != 1: return False
    if solution[10] != 1: return False
    if solution[10] == 1 and sum([solution[11], solution[12]]) != 1: return False
    if solution[13] != 1: return False
    if solution[14] != 1: return False
    if solution[19] == 1 and solution[15] != 1: return False
    if solution[16] != 1: return False
    if solution[16] == 1 and solution[17] != 1: return False
    if solution[16] == 1 and solution[18] != 1: return False
    if solution[20] == 1 and solution[21] != 1: return False
    if solution[20] == 1 and solution[22] != 1: return False
    if solution[22] == 1 and sum([solution[23], solution[24]]) != 1: return False
    if solution[20] == 0 and sum(solution[21:25]) != 0: return False
    return True

def values_for_sql(file_names):
    algorithms = [ "NSGAII"]
    list_of_files = os.listdir("..")

    from collections import defaultdict
    file_dict = defaultdict(list)

    for file_name in file_names:
        for file in list_of_files:
            if file_name in file:
                for algorithm in algorithms:
                    if algorithm in file:
                        file_dict[file_name + "#" + algorithm + "#" + file.split("_")[3]].append(file)


    count = 0
    ranks = defaultdict(list)
    final_list = []
    for key in file_dict.keys():
        content = []
        values = []
        for f in file_dict[key]: content.extend(read_file_return_list(f))
        for cont in content:
            values.append([[cont.split(":")[0]], float(cont.split()[-1])])
        final_list.append(sorted(values, key=lambda x: x[-1])[0][-1])

    import numpy as np
    print "Median: ", np.percentile(final_list, 50), "IQR: ", np.percentile(final_list, 75) - np.percentile(final_list, 25)



def get_ranks(file_names):
    algorithms = [ "NSGAII"]
    list_of_files = os.listdir("..")

    from collections import defaultdict
    file_dict = defaultdict(list)
    for file_name in file_names:
        for file in list_of_files:
            if file_name in file:
                for algorithm in algorithms:
                    if algorithm in file:
                        file_dict[file_name + "#" + algorithm + "#" + file.split("_")[3]].append(file)

    count = 0
    ranks = defaultdict(list)
    for key in file_dict.keys():
        content = []
        for f in file_dict[key]: content.extend(read_file_return_list(f))
        dataset, rank_list = get_dataset(file_names[-1])
        transform_content = [c.split(":")[0].replace(" ", "") for c in content]

        # only for BDBJ
        # for index, tc in enumerate(transform_content):
        #     temp_tc = map(int, tc.split(","))
        #     indexes_iTracting = [21, 22, 23, 24]
        #     indexes_new_io = [5, 6, 7, 8, 9]
        #     if temp_tc[20] == 0:
        #         for ind in indexes_iTracting: temp_tc[ind] = 0
        #     if temp_tc[4] == 0:
        #         for ind in indexes_new_io: temp_tc[ind] = 0
        #
        #     assert(validate(temp_tc) is True), "Something is wrong"
        #     transform_content[index] = ",".join([str(i) for i in temp_tc])




        for tc in transform_content:
            # print tc
            if key in ranks.keys():
                try:
                    ranks[key].extend([rank_list.index(float(dataset[tc]))])
                except:
                    count += 1
                    pass
            else:
                # print "> "*10
                # try:
                try:
                    ranks[key] = [rank_list.index(float(dataset[tc]))]
                except:
                    # print tc
                    count += 1
                    pass

    # print len(ranks.keys())
    # raw_input()
    best_scores = []
    for key in ranks.keys():
        # print key, ranks[key]
        best_scores.append(sorted(ranks[key])[0])
    # raw_input()
    print "count: ", count
    return best_scores


def _values_for_sql():
    file_names = ["CPM_SQL"]
    for file_name in file_names:
        print file_name,
        values_for_sql([file_name])

def _values_for_rest():
    file_names = ["CPM_APACHE", "CPM_BDBC", "CPM_BDBJ",  "CPM_LLVM", "CPM_SQL","cpm_X264",]
    # file_names = ["cpm_X264", "CPM_APACHE", "CPM_BDBC", "CPM_LLVM", "CPM_SQL",]
    for file_name in file_names:
        print file_name,
        rank_list = get_ranks([file_name])
        rank_list = sorted(rank_list)
        print rank_list
        tw5 = int(len(rank_list)/4)
        hlf = 2 * tw5
        thrds = 3 * tw5
        _, ranklst = get_dataset(file_name)
        length = len(ranklst)
        # x = lambda x: int((x/length) * 100)
        x = lambda x: x
        # Ranks:
        # print " 25: ",x(rank_list[tw5])," Median: ", x(rank_list[hlf]), " 75: ", x(rank_list[thrds])
        # Scores:
        # print " y25: ",x(ranklst[tw5])," y50: ", x(ranklst[hlf]), " y75: ", x(ranklst[thrds])
        print " Median: ", x(ranklst[hlf]), " IQR: ", x(ranklst[thrds]) - x(ranklst[tw5])

if __name__ == "__main__":
    _values_for_sql()
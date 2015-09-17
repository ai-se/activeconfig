def evaluation_data():
    eval = {}

    apache = {}
    apache["random_where"] = [8, 8, 16, 16, 16, 16, 16, 16, 16]
    apache["base_line"] = [20, 39, 58, 77, 96, 116, 135, 154, 173]
    apache["exemplar_where"] = [8, 8, 16, 16, 16, 16, 16, 16, 16]
    apache["east_west_where"] = [16, 16, 32, 32, 32, 32, 32, 32, 32, 32]
    eval["apache"] = apache

    bdbj = {}
    bdbj["random_where"] = [8, 8, 15, 16, 16, 16, 16, 16, 16]
    bdbj["base_line"] = [18, 36, 55, 72, 90, 108, 126, 145, 163]
    bdbj["exemplar_where"] = [8, 8, 15, 16, 16, 16, 16, 16, 16]
    bdbj["east_west_where"] = [16, 16, 30, 32, 32, 30, 30, 32, 32]
    eval["bdbj"] = bdbj

    bdbc = {}
    bdbc["random_where"] = [30, 30, 30, 52, 52, 52, 52, 51, 51]
    bdbc["base_line"] = [256, 512, 768, 1024, 1280, 1536, 1792, 2049, 2305]
    bdbc["exemplar_where"] = [30, 30, 30, 52, 52, 52, 52, 51, 51]
    bdbc["east_west_where"] = [60, 60, 60, 104.6, 105.1, 100.8, 103.7, 102.6, 100.3]
    eval["bdbc"] = bdbc

    sql = {}
    sql["random_where"] = [30, 33, 52, 53, 56, 51, 49, 51, 82]
    sql["base_line"] = [466, 931, 1396, 1862, 2327, 2796, 3258, 3723, 4188]
    sql["exemplar_where"] = [30, 33, 52, 53, 50, 51, 51, 52, 81]
    sql["east_west_where"] = [60, 65, 104, 103, 102, 103, 103, 101, 161]
    eval["sql"] = sql


    X264 = {}
    X264["random_where"] = [16, 22, 30, 30, 30, 29, 30, 29, 51]
    X264["base_line"] = [116, 231, 346, 461, 576, 692, 807, 922, 1037]
    X264["exemplar_where"] = [16, 22, 30, 30, 30, 29, 30, 29, 52]
    X264["east_west_where"] = [32, 45, 59, 59, 60, 60, 60, 60, 59, 108]
    eval["X264"] = X264

    LLVM = {}
    LLVM["random_where"] = [16, 16, 31, 30, 30, 30, 30, 30, 30]
    LLVM["base_line"] = [103, 205, 308, 410, 512, 615, 717, 820, 922]
    LLVM["exemplar_where"] = [16, 16, 30, 30, 30, 30, 30, 30, 30]
    LLVM["east_west_where"] = [32, 31, 60, 59, 60, 58, 58, 58, 60, 59]
    eval["LLVM"] = LLVM

    return eval

def median_mre_scores():
    def list_files():
        log_directory = "../Logs/"
        import os
        files = [log_directory+file for file in os.listdir(log_directory) if file[-4:]==".txt"]
        return files

    def get_data(filename):
        data = {}
        lines = open(filename, "r").readlines()
        for i, line in enumerate(lines):
            if i == 0: continue
            temp = line.split(",")
            temp[-1] = temp[-1].replace("\n", "")
            if temp[-1] in data.keys(): data[temp[-1]].append(round(float(temp[1]) * 100, 2))
            else:  data[temp[-1]] = [round(float(temp[1])*100, 2)]
        return data

    data = {}
    files = list_files()
    for file in files:
        name = file[:-4].split("_")[1]
        data[name] = get_data(file)

    return data


left, width = .55, .5
bottom, height = .25, .5
right = left + width
top = bottom + height


#
print median_mre_scores().keys()
# print evaluation_data()["apache"]["east_west_where"]

import numpy as np
import matplotlib.pyplot as plt
x_axis = [0.1 * i for i in xrange(1, 10)]

f, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(6, 1, sharex='col')
# plt.subplot(3, 2, 1)
ax1.plot(x_axis, median_mre_scores()["apache"]["exemplar_where"], 'ko-', color='r')
ax1.plot(x_axis, median_mre_scores()["apache"]["random_where"], 'kv-', color='y')
ax1.plot(x_axis, median_mre_scores()["apache"]["east_west_where"], 'kx-', color='g')
ax1.plot(x_axis, median_mre_scores()["apache"]["base_line"], 'kx-', color='b')
ax1.set_xlim(0.05, 0.95)
ax1.set_ylim(0.0, 30)
ax1.set_yticks(np.arange(0, 30, 10))
ax1.text(right, 0.5*(bottom+top), 'Apache',
        horizontalalignment='center',
        verticalalignment='center',
        rotation=270,
        fontsize=11,
        transform=ax1.transAxes)
# ax1.set_ylabel("MRE")

# plt.subplot(3, 2, 2)
ax2.plot(x_axis, median_mre_scores()["BDBC"]["exemplar_where"], 'ko-', color='r')
ax2.plot(x_axis, median_mre_scores()["BDBC"]["random_where"], 'kv-', color='y')
ax2.plot(x_axis, median_mre_scores()["BDBC"]["east_west_where"], 'kx-', color='g')
ax2.plot(x_axis, median_mre_scores()["BDBC"]["base_line"], 'kx-', color='b')
# ax2.set_title('Berkeley DB C')
ax2.set_xlim(0.05, 0.95)
ax2.set_ylim(-5, 70)
ax2.set_yticks(np.arange(0, 70, 20))
# ax2.set_ylabel("MRE")
ax2.text(right, 0.5*(bottom+top), 'BDBC',
        horizontalalignment='center',
        verticalalignment='center',
        rotation=270,
        fontsize=11,
        transform=ax2.transAxes)

# plt.subplot(3, 2, 3)
ax3.plot(x_axis, median_mre_scores()["BDBJ"]["exemplar_where"], 'ko-', color='r')
ax3.plot(x_axis, median_mre_scores()["BDBJ"]["random_where"], 'kv-', color='y')
ax3.plot(x_axis, median_mre_scores()["BDBJ"]["east_west_where"], 'kx-', color='g')
ax3.plot(x_axis, median_mre_scores()["BDBJ"]["base_line"], 'kx-', color='b')
ax3.set_ylim(0.0, 40)
ax3.set_yticks(np.arange(0, 40, 10))
ax3.set_xlim(0.05, 0.95)
# ax3.set_xlabel("Training Data (% of data)")
# ax3.set_ylabel("MRE")
ax3.text(right, 0.5*(bottom+top), 'BDBJ',
        horizontalalignment='center',
        verticalalignment='center',
        rotation=270,
        fontsize=11,
        transform=ax3.transAxes)

# plt.subplot(3, 2, 4)
ax4.plot(x_axis, median_mre_scores()["X264"]["exemplar_where"], 'ko-', color='r')
ax4.plot(x_axis, median_mre_scores()["X264"]["random_where"], 'kv-', color='y')
ax4.plot(x_axis, median_mre_scores()["X264"]["east_west_where"], 'kx-', color='g')
ax4.plot(x_axis, median_mre_scores()["X264"]["base_line"], 'kx-', color='b')
ax4.set_ylim(-1, 18)
ax4.set_xlim(0.05, 0.95)
# ax4.set_ylabel("MRE")
ax4.text(right, 0.5*(bottom+top), 'X264',
        horizontalalignment='center',
        verticalalignment='center',
        rotation=270,
        fontsize=11,
        transform=ax6.transAxes)

# plt.subplot(3, 2, 5)
ax5.plot(x_axis, median_mre_scores()["SQL"]["exemplar_where"], 'ko-', color='r')
ax5.plot(x_axis, median_mre_scores()["SQL"]["random_where"], 'kv-', color='y')
ax5.plot(x_axis, median_mre_scores()["SQL"]["east_west_where"], 'kx-', color='g')
ax5.plot(x_axis, median_mre_scores()["SQL"]["base_line"], 'kx-', color='b')
ax5.set_xlim(0.05, 0.95)
ax5.set_ylim(0, 13)
ax5.set_yticks(np.arange(0, 13, 5))
# ax5.set_ylabel("MRE")
ax5.text(right, 0.5*(bottom+top), 'SQL',
        horizontalalignment='center',
        verticalalignment='center',
        rotation=270,
        fontsize=11,
        transform=ax5.transAxes)

# plt.subplot(3, 2, 6)
ax6.plot(x_axis, median_mre_scores()["LLVM"]["exemplar_where"], 'ko-', color='r')
ax6.plot(x_axis, median_mre_scores()["LLVM"]["random_where"], 'kv-', color='y')
ax6.plot(x_axis, median_mre_scores()["LLVM"]["east_west_where"], 'kx-', color='g')
ax6.plot(x_axis, median_mre_scores()["LLVM"]["base_line"], 'kx-', color='b')
ax6.set_xlim(0.05, 0.95)
ax6.set_ylim(0, 10)
ax6.set_yticks(np.arange(0, 10, 5))
# ax6.set_ylabel("MRE")
ax6.text(right, 0.5*(bottom+top), 'LLVM',
        horizontalalignment='center',
        verticalalignment='center',
        rotation=270,
        fontsize=11,
        transform=ax4.transAxes)

# plt.subplots_adjust(left=0.35, bottom=0.04, right=0.90, top=0.97, wspace=0.10, hspace=0.10)
plt.figlegend([ax1.lines[0], ax1.lines[1], ax1.lines[2], ax1.lines[3]], ["Where Exemplar", "Where Random", "Where East West", "Baseline"], frameon=False, loc='lower center', bbox_to_anchor=(0.5, -0.025), fancybox=True, ncol=2)

f.set_size_inches(5, 9)
f.subplots_adjust(wspace=0, hspace=0)
f.text(0.04, 0.5, 'MRE', va='center', rotation='vertical', fontsize=11)
plt.xlabel("Percentage of Data")
# plt.subplot_tool()
# f.tight_layout()
plt.savefig('destination_path.eps', format='eps')
# plt.show()
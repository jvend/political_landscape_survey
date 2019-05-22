# Generates histogram of authors per article count

import numpy as np

filename="final_count.txt"
with open(filename) as f:
    lines = f.read().splitlines()

count=[]
for line in lines:
    count_line = line.split()[3]
    count.append(np.log10(1+float(count_line)))

count = np.array(count)
print(np.max(count))

import matplotlib.pyplot as plt 
plt.figure()
plt.hist(count,bins=100);
plt.title("Histogram of Authors with given Article Counts");
plt.xlabel("Log$_{10}$( 1 + Article Number )");
plt.ylabel("Number of Authors");
plt.show()


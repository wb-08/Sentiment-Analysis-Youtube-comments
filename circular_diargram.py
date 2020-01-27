import matplotlib.pyplot as plt
from parsing_comments import result_analysis
skip , negative,positive,neutral , speech_act_class=result_analysis()
labels=['skip','negative','positive','neutral','speech']
values=[skip , negative,positive,neutral , speech_act_class]
fig1, ax1 = plt.subplots()
wedges, texts, autotexts = ax1.pie(values, labels=labels, autopct='%1.2f%%')
ax1.axis('equal')
plt.savefig('diagram.png')
# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd


# data = {
#     'q': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
#     'Bot1': [0.7, 0.8, 0.85, 0.6, 0.55, 0.4, 0.35, 0.2, 0.1, 0.05],
#     'Bot2': [0.8, 0.85, 0.9, 0.7, 0.65, 0.5, 0.45, 0.3, 0.2, 0.1],
#     'Bot3': [0.9, 0.85, 0.8, 0.75, 0.65, 0.55, 0.5, 0.45, 0.3, 0.2],
#     'Bot4': [0.95, 0.9, 0.85, 0.8, 0.7, 0.6, 0.55, 0.5, 0.4, 0.3]
# }


# df = pd.DataFrame(data)


# q_values = df['q']
# bar_width = 0.2
# index = np.arange(len(q_values))

# fig, ax = plt.subplots(figsize=(10, 6))

# ax.bar(index, df['Bot1'], bar_width, label='Bot 1')
# ax.bar(index + bar_width, df['Bot2'], bar_width, label='Bot 2')
# ax.bar(index + 2 * bar_width, df['Bot3'], bar_width, label='Bot 3')
# ax.bar(index + 3 * bar_width, df['Bot4'], bar_width, label='Bot 4')

# ax.set_xlabel('q Values')
# ax.set_ylabel('Success Ratio')
# ax.set_title('Success Ratio vs q Values for Each Bot (Bar Chart)')
# ax.set_xticks(index + 1.5 * bar_width)
# ax.set_xticklabels(df['q'])
# ax.legend()


# plt.show()


# fig, ax = plt.subplots(figsize=(10, 6))

# ax.plot(q_values, df['Bot1'], marker='o', label='Bot 1')
# ax.plot(q_values, df['Bot2'], marker='o', label='Bot 2')
# ax.plot(q_values, df['Bot3'], marker='o', label='Bot 3')
# ax.plot(q_values, df['Bot4'], marker='o', label='Bot 4')


# ax.set_xlabel('q Values')
# ax.set_ylabel('Success Ratio')
# ax.set_title('Success Ratio vs q Values for Each Bot (Line Graph)')
# ax.legend()


# plt.show()
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


data = {
    'q': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],


    'Bot1': [0.94, 0.90, 0.81, 0.74, 0.70, 0.66, 0.53, 0.51, 0.56, 0.5],


    'Bot2': [0.88, 0.86, 0.78, 0.68, 0.73, 0.67, 0.62, 0.47, 0.46, 0.45],


    'Bot3': [0.93, 0.87, 0.80, 0.74, 0.79, 0.75, 0.61, 0.54, 0.50 , 0.49],


    'Bot4': [0.95, 0.94, 0.83, 0.76, 0.69, 0.68, 0.70, 0.57, 0.59, 0.55]
}

df = pd.DataFrame(data)

q_values = df['q'] 
bar_width = 0.4     
index = np.arange(len(q_values))  


bots = ['Bot1', 'Bot2', 'Bot3', 'Bot4']


for bot in bots:
    plt.figure()  
    plt.bar(index, df[bot], bar_width, label=bot)
    

    plt.xlabel('q Values')
    plt.ylabel('Success Ratio')
    plt.title(f'Success Ratio vs q Values for {bot}')
    plt.xticks(index, df['q']) 
    

    plt.ylim(0.0, 1.0)
    plt.yticks(np.arange(0.0, 1.1, 0.1))  
    
    plt.legend()


    plt.show()




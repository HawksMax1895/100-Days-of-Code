# with open('weather_data.csv') as file:
#     data = file.readlines()
#     print(data)

# import csv
#
# with open('weather_data.csv') as file:
#     data = csv.reader(file)
#     temperatures = []
#     for row in data:
#         if row[1] != 'temp':
#             temperatures.append(int(row[1]))
# print(temperatures)

# import pandas
#
# data = pandas.read_csv('weather_data.csv')
# # print(data)
# # print(data['temp'])
# # data_dict = data.to_dict()
# # print(data_dict)
# #
# # temp_list = data['temp'].to_list()
# # print(temp_list)
# #
# # mean_temp = data['temp'].mean()
# # print(mean_temp)
# #
# # max_temp = data['temp'].max()
# # print(max_temp)
# #
# # print(data.condition)
#
# print(data[data.temp == data.temp.max()])
#
# monday = data[data.day == 'Monday']
# print((monday.temp*9/5)+35)

import pandas as pd

df = pd.read_csv('squirrel_data.csv')
color = df['Primary Fur Color'].dropna().unique()
fur_sum = []
for fur in color:
    fur_sum.append(df['Primary Fur Color'][df['Primary Fur Color'] == fur].count())
print(fur_sum)
data = pd.DataFrame()
data['Fur Color'] = color
data['Count'] = fur_sum
data.to_csv('Squirrel_color_count.csv')

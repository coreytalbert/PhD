import pandas as pd

df = pd.read_csv('data_master.csv', header=[0,1,2])

regex_pattern = '(Fruits|Vegetables|Proteins|Dairy and Dairy Substitutes|Grains)'
selected_column_names = df.filter(regex=regex_pattern, axis=1).columns.tolist()
# print(selected_column_names)

field_map = {}
for multi_column in selected_column_names:
        field_map[multi_column] = (f"{multi_column[0]}_b", f"{multi_column[1]}_binary", '')
# print(field_map)
        
positive_response_set = {'I eat this food regularly (at least once per week)', 'I would be willing to eat this food if it was served to me'}
negative_response_set = {'This food is not part of my diet/I do not eat this food'}

for key, value in field_map.items():
    df[value] = df[key].apply(lambda response: 0 if response in negative_response_set else 1)

df = df.copy()

regex_patterns = ['Fruits.*binary', 'Vegetables.*binary', 'Proteins.*binary', 'Dairy and Dairy Substitutes.*binary', 'Grains.*binary']
for regex_pattern in regex_patterns:
    column_subset = df.filter(regex=regex_pattern, axis=1).columns.tolist()
    # print(column_subset)
    subset_sum = df[column_subset].sum(axis=1)
    # print("subset_sum = ", subset_sum)
    new_sum_multi_column_header = (f"{regex_pattern}_s", f"{regex_pattern}_sum", '')
    # print(new_sum_multi_column_header)
    df[new_sum_multi_column_header] = subset_sum

# print(df.columns)
df.to_csv('output.csv', index=False)

import pandas as pd
from datetime import date

df = pd.read_csv('merged.csv', header=[0,1,2])

binary_regex_pattern = '(Fruits|Vegetables|Proteins|Dairy and Dairy Substitutes|Grains)'
selected_column_names = df.filter(regex=binary_regex_pattern, axis=1).columns.tolist()
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

binary_regex_patterns = ['Fruits.*binary', 'Vegetables.*binary', 'Proteins.*binary', 'Dairy and Dairy Substitutes.*binary', 'Grains.*binary']
for binary_regex_pattern in binary_regex_patterns:
    binary_column_subset = df.filter(regex=binary_regex_pattern, axis=1).columns.tolist()
    # print(column_subset)
    subset_sum = df[binary_column_subset].sum(axis=1)
    # print("subset_sum = ", subset_sum)
    row_0_header = binary_regex_pattern.split(sep = ".")[0] + " binary sum"
    row_1_header = binary_regex_pattern.split(sep = ".")[0] + " binary sum"
    new_sum_multi_column_header = (row_0_header, row_1_header, '')
    # print(new_sum_multi_column_header)
    df[new_sum_multi_column_header] = subset_sum

# Calculating the sum for all foods
binary_sum_regex_pattern = ".*binary sum"
binary_sum_column_subset = df.filter(regex=binary_sum_regex_pattern, axis=1).columns.tolist()
subset_sum = df[binary_sum_column_subset].sum(axis=1)
new_sum_multi_column_header = ("All Foods binary sum", "All foods binary sum", '')
df[new_sum_multi_column_header] = subset_sum

# print(df.columns)
df.to_csv(date.today().isoformat() + '-output.csv', index=False)

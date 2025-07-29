import pandas as pd
from Data_Preprocessing import Load_and_preprocessing_data

data_frame = Load_and_preprocessing_data()

# Phần 2: Phân tích thống kê cơ bản
# Câu 5: Tính tổng doanh thu từng tháng.
print("Câu 5: ")
Sales_Month = data_frame.groupby('Month').agg({
    'Sales' : 'sum',
    'Price' : 'first'
}).reset_index()
print(Sales_Month)
print('\n')

# Câu 6: Tìm tháng có doanh thu cao nhất.
print("Câu 6: ")
Max_Sales = Sales_Month.max()
print('The Month have max Sales is: ', Max_Sales['Month'], ' with sales: ', Max_Sales['Sales'])
print('\n')

# Câu 7: Tính sản phẩm bán chạy nhất theo số lượng.
print("Câu 7: ")
Most_Productive = data_frame.groupby('Product').agg({
    'Quantity' : 'sum',
    'Price'    : 'first'
}).reset_index()
Result_Most_Productive = Most_Productive.sort_values(by = 'Quantity', ascending=False)
print(Result_Most_Productive.head(1))
print('\n')

# Câu 8: Tính doanh thu trung bình theo sản phẩm.
print("Câu 8: ")
Mean_Sales = data_frame.groupby('Product').agg({
    'Sales'    : 'sum',
    'Quantity' : 'sum',
    'Price'    : 'first'
}).reset_index()
Mean_Sales['Mean Sales per Unit'] = Mean_Sales['Sales']/Mean_Sales['Quantity']
print(Mean_Sales[['Product','Mean Sales per Unit']])
print('\n')

# Câu 9: Tìm 10 sản phẩm có giá trung bình cao nhất.
print("Câu 9: ")
Mean_Sales = Mean_Sales.sort_values(by = 'Mean Sales per Unit', ascending = False)
print(Mean_Sales.head(10))
print('\n')
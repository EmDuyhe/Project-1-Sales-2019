from Data_Preprocessing import Load_and_preprocessing_data
import pandas as pd

data_frame = Load_and_preprocessing_data()

# PHẦN 3: Phân tích theo địa lý và thời gian
# Câu 11: Phân tích doanh thu theo từng thành phố:
print("Câu 11: ")
City_List = data_frame['City'].unique()
for City in City_List:
    print( f"\nCity: ----- {City} ----- ")
    City_df = data_frame[data_frame['City'] == City][['Product', 'Price Each', 'Quantity Ordered','Sales']]
    City_df = City_df.groupby('Product').agg({
        'Price Each' : 'mean',
        'Quantity Ordered': 'sum',
        'Sales' : 'sum'
    }).reset_index()
    
    print(City_df)
    
# Câu 12: Phân tích lượng đơn hàng theo giờ trong ngày.
print("Câu 12: ")                                            
for Hour in sorted(data_frame['Hour'].unique()):
    print(f'\nTime: {Hour}')
    Hour_df = data_frame[data_frame['Hour']==Hour][['Product','Price Each','Quantity Ordered','Sales','Purchase Address']]
    Hour_df = Hour_df.groupby('Product').agg({
        'Price Each' : 'mean',
        'Quantity Ordered': 'sum',
        'Sales' : 'sum'
    }).reset_index
    
print(Hour_df)
print('\n')

# Câu 13: Tính ngày có nhiều đơn hàng nhất
print("Câu 13: ")
Date_df = data_frame[['Order Date','Quantity Ordered']].copy()
Date_df['Date'] = Date_df['Order Date'].dt.date
Date_df = Date_df.groupby('Date').agg({
    'Quantity Ordered' : 'sum'        
}).reset_index()
Date_df = Date_df.sort_values(by='Quantity Ordered', ascending = 0).reset_index()
print(Date_df.head(1))
print('\n')

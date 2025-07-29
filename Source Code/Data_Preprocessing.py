import pandas as pd

def Load_and_preprocessing_data():
    # Phần 1: Tiền xử lý dữ liệu:
    # 1: Gộp tất cả dữ liệu từ các file CSV.
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    dfs = []
    for month in months:
        df = pd.read_csv(f"Project_1/Sales_Data/Sales_{month}_2019.csv")
        dfs.append(df)
    Sales_Data_df = pd.concat(dfs, ignore_index=True)
    del dfs, df
    
    # 2: Xử lý các dòng lỗi định dạng, trống
    # Xóa dòng dữ liệu trống:
    Sales_Data_df.dropna(inplace=True)
    Sales_Data_df = Sales_Data_df[Sales_Data_df['Order Date'] != 'Order Date']

    #3: Chuyển đổi Order Date -> Date Time
    Sales_Data_df['Order Date'] = pd.to_datetime(Sales_Data_df['Order Date'].str.strip(), 
                                                 errors = 'coerce',
                                                 format = '%m/%d/%y %H:%M')

    #4: Tạo các cột mới: Month, Hour, và Sales = Quantity * Price.
    Sales_Data_df['Month'] = Sales_Data_df['Order Date'].dt.month
    Sales_Data_df['Hour']  = Sales_Data_df['Order Date'].dt.hour

    Sales_Data_df['Quantity Ordered'] = Sales_Data_df['Quantity Ordered'].astype('int16')
    Sales_Data_df['Price Each']       = Sales_Data_df['Price Each'].astype('float32')
    Sales_Data_df['Sales']            = Sales_Data_df['Quantity Ordered'] * Sales_Data_df['Price Each']

    #5: Trích xuất City từ Purchase Address.
    Sales_Data_df['City'] = Sales_Data_df['Purchase Address'].apply(lambda x: x.split(',')[1].strip())

    # Trả về Data Frame đã Clean.
    return Sales_Data_df
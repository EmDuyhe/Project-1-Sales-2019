from Data_Preprocessing import Load_and_preprocessing_data
import pandas as pd 

data_frame = Load_and_preprocessing_data()

# PHẦN 4: Phân tích hành vi mua hàng
# Câu 14: Tìm các đơn hàng có cùng Order ID ➜ mua nhiều sản phẩm.
# Tức là 1 lần mua hàng có thể có nhiều sản phẩm, nhưng sẽ cùng 1 Order Id? 
print("Câu 14: ")
Multi_Order = data_frame.groupby('Order ID').filter(lambda x: len(x)>1).reset_index()
print(Multi_Order)
print('\n')

# Câu 15: Tìm các cặp sản phẩm hay được mua chung.
# Tức trong nhóm Order ID sẽ có cặp sản phẩm mà trong những Order ID khác cũng thường xuất hiện?
print("Câu 15: ")
# Gọp những sản phẩm có cùng Order ID thành nhóm
Order_Product = Multi_Order.groupby('Order ID')['Product'].apply(list).reset_index()

# Tạo danh sách những cặp Product đi chung với nhau
pair_list = []
for products in Order_Product['Product']:
    products = sorted(products)
    for i in range(len(products)):
        for j in range(i+1, len(products)):
            pair = f"{products[i]} & {products[j]}"
            pair_list.append(pair)
            
# Đếm số lần xuất hiện của cặp sản phẩm
pair_counts = pd.Series(pair_list).value_counts().reset_index()
pair_counts.columns = ['Product Pair', 'Frequency']

print(pair_counts.head(10))
print('\n')

# Câu 16: Tính tổng số sản phẩm khác nhau đã bán.
print("Câu 16: ")
total_unique_products = data_frame['Product'].nunique()
print("Số sản phẩm khác nhau đã bán là: ", total_unique_products)
print('\n')

# Câu 17: Phân tích tỉ lệ sản phẩm bán ra của từng loại sản phẩm.
print("Câu 17: ")
Product_Data_df = data_frame.groupby('Product')['Quantity Ordered'].sum().reset_index()
total_product = Product_Data_df['Quantity Ordered'].sum()
Product_Data_df['Percent'] = Product_Data_df['Quantity Ordered'] / total_product * 100
print(Product_Data_df['Percent'])
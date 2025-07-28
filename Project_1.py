import numpy as np 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Phần 1: Tiền xử lý dữ liệu:
# Câu 1: Gộp tất cả DataFrame lại 
print("Câu 1: ")
months = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']
dfs = []
for month in months:
    df = pd.read_csv(f"Project_1/Sales_Data/Sales_{month}_2019.csv")
    dfs.append(df)
Sales_Data_df = pd.concat(dfs, ignore_index=True)
del dfs, df
print(Sales_Data_df.head(10))
print('\n')

# Câu 2: Xử lý các dòng lỗi định dạng, trống
print(r'Câu 2: ')
# Xóa dòng dữ liệu trống:
Sales_Data_df.dropna(inplace=True)
Sales_Data_df = Sales_Data_df[Sales_Data_df['Order Date'] != 'Order Date']
print('\n')

# Câu 3: Chuyển đổi Order Date -> Date Time
print(r'Câu 3: ')
Sales_Data_df['Order Date'] = pd.to_datetime(Sales_Data_df['Order Date'].str.strip(), 
                                             errors = 'coerce',
                                             format = '%m/%d/%y %H:%M')
print('\n')

# Câu 4: Tạo các cột mới: Month, Hour, và Sales = Quantity * Price.
print(r'Câu 4: ')
Sales_Data_df['Month'] = Sales_Data_df['Order Date'].dt.month
Sales_Data_df['Hour']  = Sales_Data_df['Order Date'].dt.hour

Sales_Data_df['Quantity'] = Sales_Data_df['Quantity Ordered'].astype('int16')
Sales_Data_df['Price']    = Sales_Data_df['Price Each'].astype('float32')
Sales_Data_df['Sales'] = Sales_Data_df['Quantity'] * Sales_Data_df['Price']
print('\n')

# Phần 2: Phân tích thống kê cơ bản
# Câu 5: Tính tổng doanh thu từng tháng.
print(r'Câu 5: ')
Sales_Month = Sales_Data_df.groupby('Month').agg({
    'Sales' : 'sum',
    'Price' : 'first'
}).reset_index()
print(Sales_Month)
print('\n')

# Câu 6: Tìm tháng có doanh thu cao nhất.
print(r'Câu 6: ')
Max_Sales = Sales_Month.max()
print('The Month have max Sales is: ', Max_Sales['Month'], ' with sales: ', Max_Sales['Sales'])
print('\n')

# Câu 7: Tính sản phẩm bán chạy nhất theo số lượng.
print(r'Câu 7: ')
Most_Productive = Sales_Data_df.groupby('Product').agg({
    'Quantity' : 'sum',
    'Price'    : 'first'
}).reset_index()
Result_Most_Productive = Most_Productive.sort_values(by = 'Quantity', ascending=False)
print(Result_Most_Productive.head(1))
print('\n')

# Câu 8: Tính doanh thu trung bình theo sản phẩm.
print(r'Câu 8: ')
Mean_Sales = Sales_Data_df.groupby('Product').agg({
    'Sales'    : 'sum',
    'Quantity' : 'sum',
    'Price'    : 'first'
}).reset_index()
Mean_Sales['Mean Sales per Unit'] = Mean_Sales['Sales']/Mean_Sales['Quantity']
print(Mean_Sales[['Product','Mean Sales per Unit']])
print('\n')

# Câu 9: Tìm 10 sản phẩm có giá trung bình cao nhất.
print(r'Câu 9: ')
Mean_Sales = Mean_Sales.sort_values(by = 'Mean Sales per Unit', ascending = False)
print(Mean_Sales.head(10))
print('\n')

# PHẦN 3: Phân tích theo địa lý và thời gian
# Câu 10: Trích xuất City từ Purchase Address.
print(r'Câu 10: ')
Sales_Data_df['City'] = Sales_Data_df['Purchase Address'].apply(lambda x: x.split(',')[1].strip())
print(Sales_Data_df)

# Câu 11: Phân tích doanh thu theo từng thành phố:
# Phân thành tựng cụm thành phố, mỗi thành phố sẽ xem xét mặt hàng, giá cả, số lượng ,...
print(r'Câu 11: ')
City_List = Sales_Data_df['City'].unique()
for City in City_List:
    print( f"\nCity: ----- {City} ----- ")
    City_df = Sales_Data_df[Sales_Data_df['City'] == City][['Product', 'Price', 'Quantity','Sales']]
    City_df = City_df.groupby('Product').agg({
        'Price' : 'mean',
        'Quantity': 'sum',
        'Sales' : 'sum'
    }).reset_index()
    
    print(City_df)
    
# Câu 12: Phân tích lượng đơn hàng theo giờ trong ngày.
# Phân cụm theo giờ, mỗi giờ có bao nhiêu đơn hàng, tiền trung bình khoảng bao nhiêu, của từng loại mặt hàng,... 
print(r'Câu 12: ')                                            
for Hour in sorted(Sales_Data_df['Hour'].unique()):
    print(f'\nTime: {Hour}')
    Hour_df = Sales_Data_df[Sales_Data_df['Hour']==Hour][['Product','Price','Quantity','Sales','Purchase Address']]
    Hour_df = Hour_df.groupby('Product').agg({
        'Price' : 'mean',
        'Quantity': 'sum',
        'Sales' : 'sum'
    }).reset_index
    
    print(Hour_df)
print('\n')

# Câu 13: Tính ngày có nhiều đơn hàng nhất
print(r'Câu 13: ')
Date_df = Sales_Data_df[['Order Date','Quantity']].copy()
Date_df['Date'] = Date_df['Order Date'].dt.date
Date_df = Date_df.groupby('Date').agg({
    'Quantity' : 'sum'        
}).reset_index()
Date_df = Date_df.sort_values(by='Quantity', ascending = 0).reset_index()
print(Date_df.head(1))
print('\n')

# PHẦN 4: Phân tích hành vi mua hàng
# Câu 14: Tìm các đơn hàng có cùng Order ID ➜ mua nhiều sản phẩm.
# Tức là 1 lần mua hàng có thể có nhiều sản phẩm, nhưng sẽ cùng 1 Order Id? 
print(r'Câu 14:')
Multi_Order = Sales_Data_df.groupby('Order ID').filter(lambda x: len(x)>1).reset_index()
print(Multi_Order)
print('\n')

# Câu 15: Tìm các cặp sản phẩm hay được mua chung.
# Tức trong nhóm Order ID sẽ có cặp sản phẩm mà trong những Order ID khác cũng thường xuất hiện?
print(r'Câu 15: ')
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
print(r'Câu 16: ')
total_unique_products = Sales_Data_df['Product'].nunique()
print(r'Số sản phẩm khác nhau đã bán là: ', total_unique_products)
print('\n')

# Câu 17: Phân tích tỉ lệ sản phẩm bán ra của từng loại sản phẩm.
print(r'Câu 17: ')
Product_Data_df = Sales_Data_df.groupby('Product')['Quantity'].sum().reset_index()
total_product = Product_Data_df['Quantity'].sum()
Product_Data_df['Percent'] = Product_Data_df['Quantity'] / total_product * 100
print(Product_Data_df['Percent'])

# PHẦN 5: Trực quan hóa dữ liệu
# Câu 18: Vẽ biểu đồ doanh thu theo tháng.
# Kiểm tra mỗi tháng từng loại hàng bán được bao nhiêu sản phẩm, doanh thu ( sales ) thu được.
# Dùng biểu đồ đường thể hiện cho các product, với tháng trọng số là Tiền thu được . 
# Một biểu đồ để kiểm tra các mặt hàng theo tháng tăng số lượng như nào ? 
print(r'Câu 18: ')
# Tách dữ liệu ra khỏi data frame gốc
Data_Month = Sales_Data_df[['Product','Month','Sales','Quantity']]

# Trực quan hóa bằng biểu đồ: 
# 1- Trực quan hóa doanh thu tổng của từng tháng

# Nhóm dữ liệu doanh thu theo từng tháng:
sales_month = Data_Month.groupby('Month')['Sales'].sum().sort_index()

# Lập biểu đồ thể hiện doanh thu theo từng tháng.
plt.figure(figsize=(10,6))
sns.lineplot(x=sales_month.index, y=sales_month.values,marker='o')
plt.grid(True)
plt.title(r'Tổng doanh thu theo tháng')
plt.xlabel(r'Tháng')
plt.ylabel(r'Doanh thu thu được')
plt.legend(r'Doanh thu của tháng')
plt.savefig("Project_1\Doanh thu từng tháng trong năm.png")
plt.show()

# 2 - Trực quan hóa dữ liệu của từng sản phẩm qua từng tháng trong năm.
# Group dữ liệu: tổng số lượng sản phẩm theo từng tháng
product_by_month = Data_Month.groupby(['Month', 'Product'])['Quantity'].sum().reset_index()

# Tạo bảng màu thủ công
unique_products = sorted(product_by_month['Product'].unique())
palette = sns.color_palette("tab20", n_colors=len(unique_products))
color_map = dict(zip(unique_products, palette))

# Vẽ FacetGrid: mỗi biểu đồ nhỏ cho 1 tháng
g = sns.catplot(
    data=product_by_month,
    x="Product", y="Quantity",
    col="Month",      # mỗi tháng là 1 biểu đồ nhỏ
    hue="Product",    # phân biệt màu theo Product
    kind="bar",       # dạng cột
    palette=color_map,# Dùng để tạo legend
    col_wrap=4,       # chia 4 cột mỗi hàng
    height=3,         # chiều cao mỗi biểu đồ
    sharey=False      # không chia trục y chung để dễ nhìn
)

# Legend thủ công
legend_patches = [mpatches.Patch(color=color_map[prod], label=prod) for prod in unique_products]
g.figure.legend(
    handles=legend_patches,
    title="Sản phẩm",
    loc="center right",
    bbox_to_anchor=(1.01, 0.5)
)

# Tùy chỉnh trục x cho đẹp
g.set_xticklabels(rotation=90)
g.set_titles("Tháng {col_name}")  # tiêu đề mỗi subplot
g.figure.subplots_adjust(top=0.9)
g.figure.suptitle("Số lượng sản phẩm bán ra theo từng tháng", fontsize=16)
plt.savefig("Project_1\Sản phẩm từng tháng.png")
plt.tight_layout()
plt.show()

# Nhận xét:
# 1) Doanh số theo từng tháng
# Trong 4 tháng đầu năm doanh thu các mặt hàng tăng rồi giảm dần tới tháng 9. Vào giai đoạn tháng 10 thì doanh số 
# tăng mạnh nhưng lại tuột khi tới tháng 11. Tháng 12 doanh số tăng và đạt doanh số cao nhất. Doanh số thấp nhất rơi vào tháng 1
# Tăng trưởng doanh số trong giai đoạn tháng 4- tháng 10 không ổn định. 
# Dự đoán trong tháng 1 mọi người không có xu hướng mua các mặt hàng do tiền không nhiều. 
# Giai đoạn cuối năm lại có xu hướng mua đồ cao , có thể là kết quả sau 1 năm làm việc dư giả tài sản.
# 4 Tháng đầu có xu hướng tăng có thể là do mua để sử dụng cơ bản. 
# Nhưng trong giai đoạn tháng 4-10 giảm do đã mua ở 4 tháng đầu đồng thời tập trung làm việc

# 2) Doanh số của từng sản phẩm qua từng tháng.
# 2 mặt hàng được mua nhiều nhất là AA Baterries (4-pack), và AAA Baterries (4-pack). 
# Khả năng cao là do nhu cầu sử dụng pin nhiều. Có thể đẩy mạnh sản xuất duy trì chất lượng. 
# Mở thêm chiến dịch tặng quà để giữ chân khách hàng. 
# 2 mặt hàng ít được quan tâm là LG Dryer và LG Wasshing Machine. 
# Khả năng cao là giá thành không hợp dẫn đến người mua ít.
# Có thể thấy nhu cầu sản phẩm qua mỗi tháng không có sự thay đổi đột ngột. 
# Các mặt hàng ưa chuộng duy trì được sự ổn định của bản thân.
# Các mặt hàng như lightning charging cable, usb-c charging cable, wirred headphones có tiềm năng phát triển cao. 
# Nên đầu tư vào mặt marketing nhầm đẩy mạnh sản phẩm. 

# Câu 19: Vẽ biểu đồ phân phối số đơn hàng theo giờ.
# Kiểm tra xem ứng với mỗi giờ thì sẽ có bao nhiêu sản phẩm được bán ra theo đơn hàng ? 
print("Câu 19: ")
# Gộp tất cả đơn hàng có cùng thời gian lại với nhau.
Product_by_Hour = Sales_Data_df.groupby(['Hour','Product'])['Quantity'].sum().reset_index()

# - 1: Xét tổng đơn hàng theo từng giờ
plt.figure(figsize=(12,6)) 
sns.barplot(data=Product_by_Hour,x='Hour',y='Quantity',hue='Hour',errorbar=None)
plt.title("Thời gian mua hàng theo giờ")
plt.xlabel("Giờ")
plt.ylabel("Số lượng")
plt.grid(True)
plt.legend()
plt.savefig("Project_1\Thời gian mua hàng.png")
plt.show()

# Nhận xét: Thời gian mua hàng thường rơi vào từ trưa tới tối ( 10h -> 23h)
# 2 khoản thời gian nhiều đơn đặt hàng nhất là từ 11h-13h và 18h-20h.
# Với mốc 11h-13h có thể là lúc nghỉ trưa, nên họ sẽ ra ngoài mua. Có thể đặt onl nên diễn ra nhiều.
# Mốc 18h-20h là sau ngày làm, tan làm nên sẽ mua những sản phẩm cần thiết.
# Khoảng thời gian từ 14h-17h vẫn có độ cao nhất định chứng tỏ thời gian buổi chiều là thời gian thường dành cho mua sắm vật tư
# Từ 0h-6h: Thời gian nghỉ , ngủ nên ít người mua. Chủ yếu sẽ là đặt onl. 
# Từ 7h-10h sẽ là lúc đi làm nên đôi khi sẽ có người mua. 

# Câu 20: Vẽ biểu đồ thể hiện top 5 sản phẩm bán chạy nhất trong từng tháng.
print("Câu 20: ")
# Xây dựng data của các sản phẩm bán chạy của từng tháng.
Most_Productive_A_Month = Sales_Data_df.groupby(['Month','Product'])['Quantity'].sum().reset_index()
Most_Productive_A_Month = Most_Productive_A_Month.sort_values(by=['Month','Quantity'],ascending = [1,0] )

dfs = []
for month in range(1,13):
    df = Most_Productive_A_Month[Most_Productive_A_Month['Month']==month].head(5)
    dfs.append(df)
df_most_productive = pd.concat(dfs, ignore_index=True)
del dfs, df

# Tạo màu cho từng mặt hàng:
unique_products = df_most_productive['Product'].unique()                # Tách các mặt hàng riêng biệt
colors = sns.color_palette("husl", len(unique_products))                # Tạo danh sách màu dựa trên mặt hàng
colors_map = dict(zip(unique_products, colors))                         # Đóng gọi lại 1 mặt hàng ứng với 1 màu
                                                                        # -> Chuyển Key value. Ví dụ như là Product: A -> Color: Red 
                                                                        # {'AA Batteries': 'red', 'USB-C Cable': 'blue'} 

# Trực quan hóa bằng đồ thị bằng FacetGrid
top_5 = sns.FacetGrid(df_most_productive, col='Month', col_wrap=4, height = 3, sharey= True)

def Bar_with_color(data, **kwargs):
    sns.barplot(
        data = data,
        x = 'Product',
        y = 'Quantity',
        hue = 'Product',                                        # Phân biệt màu theo sản phẩm
        palette=[colors_map[p] for p in data['Product']],       # Với mỗi p ( mặt hàng ) thì nó sẽ gọi vào map color để chọn ra màu tương ứng
        **kwargs
    )

# Định dạng
top_5.map_dataframe(Bar_with_color)                             
top_5.set_xticklabels(rotation = 90)
top_5.set_titles("Tháng {col_name}")
top_5.figure.subplots_adjust(top=0.9)
top_5.figure.suptitle("Top 5 sản phẩm bán chạy trong tháng", fontsize=16)

# Legend thủ công
handles = [mpatches.Patch(color=colors_map[prod], label=prod) for prod in unique_products]
plt.legend(handles=handles, title='Sản phẩm', bbox_to_anchor=(1.05, 1), loc='upper left')

# Xuất kết quả:
plt.tight_layout()
plt.savefig("Project_1\Top 5 sản phẩm bán chạy.png")
plt.show()

# Nhận xét: Các sản phẩm bán chạy luôn duy trì ổn định, không có sự thay đổi lớn.
# Nếu nhìn vào doanh thu sản phẩm theo từng tháng có thể thấy. Các sản phẩm gần như không có sự thay đổi.
# Có xu hướng tăng về số lượng và doanh thu vào những tháng cuối năm. 
# Cho thấy mức độ ưa chuộng của mặt hàng đối vơi tệp khách hàng quen.
# Nguyên nhân có thể do: Nhu cầu sử dụng baterries(Pin) của sản phẩm cao. Nhiều đồ công nghệ cần dùng tới.

# Câu 21: Vẽ biểu đồ heatmap thể hiện doanh thu theo giờ trong ngày và theo tháng.
print("Câu 21: ")
# Xây dựng dữ liệu doanh thu theo giờ trong ngày của month
Sales_by_Hour_Month = Sales_Data_df.groupby(['Hour','Month'])['Sales'].sum().unstack()

# Xây dựng heat map
plt.figure(figsize=(12,6))
sns.heatmap(Sales_by_Hour_Month, cmap="Oranges")
plt.title("Doanh thu theo giờ trong ngày và theo tháng")
plt.xlabel("Tháng")
plt.ylabel("Giờ")
plt.savefig("Project_1\Doanh thu theo giờ trong ngày và theo tháng.png")
plt.tight_layout()
plt.show()

# Nhận xét: Doanh thu tập trung vào quý 4 và quý 2,1 phần tập trung vào cuối quý 1
# Nguyên nhân tập trung doanh thu vào 2 khoảng này do quý 4 là 
# Trong ngày doanh thu dao chủ yếu từ 18h-20h và 10h-13h. Khoảng thời gian từ 0h-7h doanh thu thấp.
# Có thể là giờ nghỉ ngơi không mua hàng nên không có doanh thu

# Câu 22: Vẽ biểu đồ scatter thể hiện mối tương quan giữa giá trung bình và số lượng sản phẩm bán ra.
print("Câu 22: ")
# Tạo dữ liệu:
Mean_Quantity_Product = Sales_Data_df.groupby('Product').agg({
    'Quantity' : 'sum',
    'Sales' : 'sum'
}).reset_index()

Mean_Quantity_Product['Avg Price'] = Mean_Quantity_Product['Sales']/Mean_Quantity_Product['Quantity']

# Vẽ biểu đồ
plt.figure(figsize=(8, 6))

# Tạo màu cho điểm
products = Mean_Quantity_Product['Product'].unique()
palette = sns.color_palette("hsv", len(products))
col_map = dict(zip(products, palette))

# Vẽ từng điểm 
for _, row in Mean_Quantity_Product.iterrows():
    plt.scatter(
        row['Quantity'], row['Avg Price'],
        color=col_map[row['Product']],
        label=row['Product']
    )
    
# Vẽ đường hồi quy chung
sns.regplot(
    data=Mean_Quantity_Product,
    x='Quantity',
    y='Avg Price',
    scatter=False,
    line_kws={'color': 'black'}
)

#Vẽ legend:
handles = [mpatches.Patch(color=col_map[prod], label=prod) for prod in products]
plt.legend(handles=handles, bbox_to_anchor=(1.05, 1), loc='upper left', title='Sản phẩm')

plt.title("Tương quan giữa giá trung bình và số lượng sản phẩm bán ra")
plt.xlabel("Số lượng")
plt.ylabel("Giá trung bình")
plt.savefig("Project_1\Tương quan giá và số lượng.png")
plt.tight_layout()
plt.show()

# Câu 23: Vẽ biểu đồ boxplot để quan sát sự phân phối giá trị đơn hàng theo từng thành phố.
print("Câu 23: ")

# Lọc dữ liệu:
df_total_price_per_city = Sales_Data_df.groupby(['City','Order ID'])['Sales'].sum().reset_index()

# Vẽ đồ thị:
sns.boxplot(data = df_total_price_per_city, x='City', y='Sales', hue = 'City')
plt.title("Phân phối giá trị đơn hàng theo thành phố")
plt.xticks(rotation=45)
plt.xlabel("Thành phố")
plt.ylabel("Giá trị đơn hàng")
plt.savefig("Project_1\Phân phối giá trị đơn hàng theo thành phố.png")
plt.show()

# Câu 24: Vẽ biểu đồ đường thể hiện xu hướng tổng doanh thu của từng nhóm sản phẩm theo thời gian (theo tháng).
print("Câu 24: ")

# Phân nhóm sản phẩm
def map_product(product_name):
    if "Phone" in product_name:
        return "Phone"
    elif "Headphone" in product_name:
        return "Headphone"
    elif "Laptop" in product_name:
        return "Laptop"
    elif "Charging Cable" in product_name:
        return "Cable"
    elif "Monitor" in product_name or "TV" in product_name:
        return "Display"
    elif "Dryer" in product_name or "Washing Machine" in product_name:
        return "Appliance"
    else:
        return "Other"
Sales_Data_df['Product Group'] = Sales_Data_df['Product'].apply(map_product)

# Gọp Product theo nhóm và theo tháng
group_product_data = Sales_Data_df.groupby(['Product Group','Month'])['Sales'].sum().reset_index()

# Phân màu cho nhóm sản phẩm.
gr_products = group_product_data['Product Group'].unique()
palette_gp = sns.color_palette("hsv",len('Product Group'))
color_product_map = dict(zip(gr_products,palette_gp))

# Vẽ biểu đồ 
p = sns.catplot(
    data=group_product_data,
    x="Product Group", y="Sales",
    col="Month",                   # mỗi tháng là 1 biểu đồ nhỏ
    hue="Product Group",           # phân biệt màu theo nhóm Product
    kind="bar",                    # dạng cột
    palette = color_product_map,   # Phân màu để chia legend
    col_wrap=4,                    # chia 4 cột mỗi hàng
    height=3,                      # chiều cao mỗi biểu đồ
    sharey=False                   # không chia trục y chung để dễ nhìn
)

# Lập legend cho nhóm sản phẩm thủ công.
handles = [mpatches.Patch(color=color_product_map[prod], label=prod) for prod in gr_products]
plt.legend(handles=handles, title='Sản phẩm', bbox_to_anchor=(1.05, 1), loc='upper left')

# Tạo layout cho đồ thị.
p.set_xticklabels(rotation=45, ha='right')
p.set_axis_labels("Nhóm sản phẩm", "Doanh thu")

# Xuất kết quả
plt.tight_layout()
plt.savefig("Project_1\Doanh thu của nhóm sản phẩm theo tháng.png")
plt.show()

# Câu 25: Vẽ biểu đồ biểu diễn tỷ lệ sản phẩm bán ra của từng loại dưới dạng biểu đồ tròn (pie chart).
# Thiết lập dữ liệu:
print("Câu 25: ")
def label_top5(group):
    top5_products = group.sort_values(by='Quantity', ascending=False).head(5)['Product']
    group['Product Grouped'] = group['Product'].apply(lambda x: x if x in top5_products.values else 'Other')
    return group

Most_Productive_A_Month_Other = Most_Productive_A_Month.groupby('Month').apply(label_top5).reset_index(drop = True)
Result_Productive = Most_Productive_A_Month_Other.groupby(['Month','Product Grouped'])['Quantity'].sum().reset_index()

# Lập khung với 3 dòng 4 cột.
fig, axes = plt.subplots(nrows = 3, ncols = 4, figsize = (16,12))
axes = axes.flatten()

# Bắt đầu vẽ Piechart cho từng tháng
for month in range(1,13):
    ax = axes[month-1]
    data = Result_Productive[Result_Productive['Month'] == month]
    
    labels = data['Product Grouped']
    sizes = data['Quantity']
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.set_title(f"Tháng {month}")
    ax.get_legend()

# Xuất kết quả
plt.tight_layout()
plt.suptitle("Tỷ lệ sản phẩm bán ra theo từng tháng", fontsize=18, y=1.03)
plt.savefig("Project_1\Tỷ lệ sản phẩm bán ra từng tháng.png")
plt.show()


# ==================================== END PROJECT_1 ===================================== # 
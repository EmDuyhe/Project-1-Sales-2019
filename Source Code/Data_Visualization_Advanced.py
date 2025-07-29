from Data_Preprocessing import Load_and_preprocessing_data
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import os

data_frame = Load_and_preprocessing_data()
script_dir = os.path.dirname(os.path.abspath(__file__))  
project_dir = os.path.dirname(script_dir)                
save_dir = os.path.join(project_dir, "Visualization_Picture")

# Câu 20: Vẽ biểu đồ thể hiện top 5 sản phẩm bán chạy nhất trong từng tháng.
print("Câu 20: ")
# Xây dựng data của các sản phẩm bán chạy của từng tháng.
Most_Productive_A_Month = data_frame.groupby(['Month','Product'])['Quantity Ordered'].sum().reset_index()
Most_Productive_A_Month = Most_Productive_A_Month.sort_values(by=['Month','Quantity Ordered'],ascending = [1,0] )

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
        y = 'Quantity Ordered',
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
save_path = os.path.join(save_dir, "Top 5 sản phẩm bán chạy.png")
plt.savefig(save_path)
plt.show()

# Nhận xét: Các sản phẩm bán chạy luôn duy trì ổn định, không có sự thay đổi lớn.
# Nếu nhìn vào doanh thu sản phẩm theo từng tháng có thể thấy. Các sản phẩm gần như không có sự thay đổi.
# Có xu hướng tăng về số lượng và doanh thu vào những tháng cuối năm. 
# Cho thấy mức độ ưa chuộng của mặt hàng đối vơi tệp khách hàng quen.
# Nguyên nhân có thể do: Nhu cầu sử dụng baterries(Pin) của sản phẩm cao. Nhiều đồ công nghệ cần dùng tới.

# Câu 21: Vẽ biểu đồ heatmap thể hiện doanh thu theo giờ trong ngày và theo tháng.
print("Câu 21: ")
# Xây dựng dữ liệu doanh thu theo giờ trong ngày của month
Sales_by_Hour_Month = data_frame.groupby(['Hour','Month'])['Sales'].sum().unstack()

# Xây dựng heat map
plt.figure(figsize=(12,6))
sns.heatmap(Sales_by_Hour_Month, cmap="Oranges")
plt.title("Doanh thu theo giờ trong ngày và theo tháng")
plt.xlabel("Tháng")
plt.ylabel("Giờ")
save_path_1 = os.path.join(save_dir, "Doanh thu theo giờ trong ngày và theo tháng.png")
plt.savefig(save_path_1)
plt.tight_layout()
plt.show()

# Nhận xét: Doanh thu tập trung vào quý 4 và quý 2,1 phần tập trung vào cuối quý 1
# Nguyên nhân tập trung doanh thu vào 2 khoảng này do quý 4 là 
# Trong ngày doanh thu dao chủ yếu từ 18h-20h và 10h-13h. Khoảng thời gian từ 0h-7h doanh thu thấp.
# Có thể là giờ nghỉ ngơi không mua hàng nên không có doanh thu

# Câu 22: Vẽ biểu đồ scatter thể hiện mối tương quan giữa giá trung bình và số lượng sản phẩm bán ra.
print("Câu 22: ")
# Tạo dữ liệu:
Mean_Quantity_Product = data_frame.groupby('Product').agg({
    'Quantity Ordered' : 'sum',
    'Sales' : 'sum'
}).reset_index()

Mean_Quantity_Product['Avg Price'] = Mean_Quantity_Product['Sales']/Mean_Quantity_Product['Quantity Ordered']

# Vẽ biểu đồ
plt.figure(figsize=(8, 6))

# Tạo màu cho điểm
products = Mean_Quantity_Product['Product'].unique()
palette = sns.color_palette("hsv", len(products))
col_map = dict(zip(products, palette))

# Vẽ từng điểm 
for _, row in Mean_Quantity_Product.iterrows():
    plt.scatter(
        row['Quantity Ordered'], row['Avg Price'],
        color=col_map[row['Product']],
        label=row['Product']
    )
    
# Vẽ đường hồi quy chung
sns.regplot(
    data=Mean_Quantity_Product,
    x='Quantity Ordered',
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
save_path_2 = os.path.join(save_dir, "Tương quan giá và số lượng.png")
plt.savefig(save_path_2)
plt.tight_layout()
plt.show()

# Câu 23: Vẽ biểu đồ boxplot để quan sát sự phân phối giá trị đơn hàng theo từng thành phố.
print("Câu 23: ")

# Lọc dữ liệu:
df_total_price_per_city = data_frame.groupby(['City','Order ID'])['Sales'].sum().reset_index()

# Vẽ đồ thị:
sns.boxplot(data = df_total_price_per_city, x='City', y='Sales', hue = 'City')
plt.title("Phân phối giá trị đơn hàng theo thành phố")
plt.xticks(rotation=45)
plt.xlabel("Thành phố")
plt.ylabel("Giá trị đơn hàng")
save_path_3 = os.path.join(save_dir, "Phân phối giá trị đơn hàng theo thành phố.png")
plt.savefig(save_path_3)
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
data_frame['Product Group'] = data_frame['Product'].apply(map_product)

# Gọp Product theo nhóm và theo tháng
group_product_data = data_frame.groupby(['Product Group','Month'])['Sales'].sum().reset_index()

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
save_path_4 = os.path.join(save_dir, "Doanh thu của nhóm sản phẩm theo tháng.png")
plt.savefig(save_path_4)
plt.show()

# Câu 25: Vẽ biểu đồ biểu diễn tỷ lệ sản phẩm bán ra của từng loại dưới dạng biểu đồ tròn (pie chart).
# Thiết lập dữ liệu:
print("Câu 25: ")
def label_top5(group):
    top5_products = group.sort_values(by='Quantity Ordered', ascending=False).head(5)['Product']
    group['Product Grouped'] = group['Product'].apply(lambda x: x if x in top5_products.values else 'Other')
    return group

Most_Productive_A_Month_Other = Most_Productive_A_Month.groupby('Month').apply(label_top5).reset_index(drop = True)
Result_Productive = Most_Productive_A_Month_Other.groupby(['Month','Product Grouped'])['Quantity Ordered'].sum().reset_index()

# Lập khung với 3 dòng 4 cột.
fig, axes = plt.subplots(nrows = 3, ncols = 4, figsize = (16,12))
axes = axes.flatten()

# Bắt đầu vẽ Piechart cho từng tháng
for month in range(1,13):
    ax = axes[month-1]
    data = Result_Productive[Result_Productive['Month'] == month]
    
    labels = data['Product Grouped']
    sizes = data['Quantity Ordered']
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.set_title(f"Tháng {month}")
    ax.get_legend()

# Xuất kết quả
plt.tight_layout()
plt.suptitle("Tỷ lệ sản phẩm bán ra theo từng tháng", fontsize=18, y=1.03)
save_path_5 = os.path.join(save_dir, "Tỷ lệ sản phẩm bán ra từng tháng.png")
plt.savefig(save_path_5)
plt.show()


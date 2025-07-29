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

# PHẦN 5: Trực quan hóa dữ liệu
# Câu 18: Vẽ biểu đồ doanh thu theo tháng.
print("Câu 18: ")
# Tách dữ liệu ra khỏi data frame gốc
Data_Month = data_frame[['Product','Month','Sales','Quantity Ordered']]

# Trực quan hóa bằng biểu đồ: 
# 1- Trực quan hóa doanh thu tổng của từng tháng

# Nhóm dữ liệu doanh thu theo từng tháng:
sales_month = Data_Month.groupby('Month')['Sales'].sum().sort_index()

# Lập biểu đồ thể hiện doanh thu theo từng tháng.
plt.figure(figsize=(10,6))
sns.lineplot(x=sales_month.index, y=sales_month.values,marker='o')
plt.grid(True)
plt.title("Tổng doanh thu theo tháng")
plt.xlabel("Tháng")
plt.ylabel("Doanh thu thu được")
plt.legend("Doanh thu của tháng")
save_path = os.path.join(save_dir, "Doanh thu từng tháng trong năm.png")
plt.savefig(save_path)
plt.show()

# 2 - Trực quan hóa dữ liệu của từng sản phẩm qua từng tháng trong năm.
# Group dữ liệu: tổng số lượng sản phẩm theo từng tháng
product_by_month = Data_Month.groupby(['Month', 'Product'])['Quantity Ordered'].sum().reset_index()

# Tạo bảng màu thủ công
unique_products = sorted(product_by_month['Product'].unique())
palette = sns.color_palette("tab20", n_colors=len(unique_products))
color_map = dict(zip(unique_products, palette))

# Vẽ FacetGrid: mỗi biểu đồ nhỏ cho 1 tháng
g = sns.catplot(
    data=product_by_month,
    x="Product", y="Quantity Ordered",
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
save_path_1 = os.path.join(save_dir, "Sản phẩm từng tháng.png")
plt.savefig(save_path_1)
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
print("Câu 19: ")
# Gộp tất cả đơn hàng có cùng thời gian lại với nhau.
Product_by_Hour = data_frame.groupby(['Hour','Product'])['Quantity Ordered'].sum().reset_index()

# - 1: Xét tổng đơn hàng theo từng giờ
plt.figure(figsize=(12,6)) 
sns.barplot(data=Product_by_Hour,x='Hour',y='Quantity Ordered',hue='Hour',errorbar=None)
plt.title("Thời gian mua hàng theo giờ")
plt.xlabel("Giờ")
plt.ylabel("Số lượng")
plt.grid(True)
plt.legend()
save_path_2 = os.path.join(save_dir, "Thời gian mua hàng.png")
plt.savefig(save_path_2)
plt.show()

# Nhận xét: Thời gian mua hàng thường rơi vào từ trưa tới tối ( 10h -> 23h)
# 2 khoản thời gian nhiều đơn đặt hàng nhất là từ 11h-13h và 18h-20h.
# Với mốc 11h-13h có thể là lúc nghỉ trưa, nên họ sẽ ra ngoài mua. Có thể đặt onl nên diễn ra nhiều.
# Mốc 18h-20h là sau ngày làm, tan làm nên sẽ mua những sản phẩm cần thiết.
# Khoảng thời gian từ 14h-17h vẫn có độ cao nhất định chứng tỏ thời gian buổi chiều là thời gian thường dành cho mua sắm vật tư
# Từ 0h-6h: Thời gian nghỉ , ngủ nên ít người mua. Chủ yếu sẽ là đặt onl. 
# Từ 7h-10h sẽ là lúc đi làm nên đôi khi sẽ có người mua. 
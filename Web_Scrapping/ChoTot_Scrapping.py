from bs4 import BeautifulSoup
import requests
import csv

root = 'https://www.chotot.com/mua-ban-dien-thoai'
last_page = 150

# Mở file CSV để ghi dữ liệu
with open('dien_thoai.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Ghi tiêu đề cột
    writer.writerow(['Brand', 'Name', 'Status', 'Guarantee', 'Color', 'Capacity', 'Origin', 'Location' ,'Price'])

    for page in range(1, last_page + 1):
        website = f'{root}?page={page}'
        result = requests.get(website)
        content = result.text
        soup = BeautifulSoup(content, 'lxml')
        box = soup.find('div', class_=['ListAds_ListAds__rEu_9', 'col-xs-12 no-padding'])

        links = []
        for link in box.find_all('a', attrs={'itemprop': 'item'}, href=True):
            links.append(root + link['href'])

        for link in links:
            print(f"Đang truy cập {link}")
            link_response = requests.get(link)
            if link_response.status_code == 200:
                link_soup = BeautifulSoup(link_response.text, 'lxml')
                box = link_soup.find('div', class_='ctcdcee')
                box = box.find('div', attrs={'direction': 'column', 'class': 'r9vw5if'})

                # Lấy giá
                price = box.find('b', class_="p1mdjmwc").get_text().replace('đ', '').strip()

                # Lấy vị trí
                location_box = box.find_all('div', class_="r9vw5if")
                location = location_box[3].find('span', class_=["bwq0cbs", "flex-1"]).get_text()

                # Lấy thông tin khác
                information_box = link_soup.find_all('div', class_="c189eou8")
                infor_box = information_box[2].find('div', class_=["brl13u9", "r9vw5if"], attrs={'direction': 'column'})
                infor_row_box = infor_box.find_all('div', class_="p74axq8")

                # Khởi tạo các biến thông tin
                brand, name, status, guarantee, color, capacity, origin = [''] * 7

                for i in range(len(infor_row_box)):
                    info = infor_row_box[i].find('div', class_="p1vpox21").get_text()
                    if i == 0:
                        brand = info
                    elif i == 1:
                        name = info
                    elif i == 2:
                        status = info
                    elif i == 3:
                        guarantee = info
                    elif i == 4:
                        color = info
                    elif i == 5:
                        capacity = info
                    elif i == 6:
                        origin = info

                # Ghi dữ liệu vào file CSV
                writer.writerow([brand, name, status, guarantee, color, capacity, origin, location, price])
                print(f"Đã ghi: Giá: {price}, Vị trí: {location}, Thương hiệu: {brand}, Tên: {name}")

            else:
                print(f"Không thể truy cập {link}, mã lỗi: {link_response.status_code}")

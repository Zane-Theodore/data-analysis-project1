# Data Preprocessing

## 🏦 1. World Bank Macro Dataset

### 📌 Cấu trúc dữ liệu
Mỗi dòng tương ứng với 1 năm (2000–2025):

| Column | Meaning |
| :--- | :--- |
| `year` | Năm quan sát |
| `exports_percent_gdp` | Tỷ trọng xuất khẩu trên GDP (%) |
| `fdi_percent_gdp` | Dòng vốn FDI (% GDP) |
| `gdp_growth` | Tăng trưởng GDP (%) |
| `inflation_cpi` | Lạm phát CPI (%) |
| `labor_force` | Quy mô lực lượng lao động |
| `unemployment` | Tỷ lệ thất nghiệp (%) |

### 📈 Ý nghĩa kinh tế
* **🔹 Exports (% GDP):** Phản ánh mức độ mở cửa nền kinh tế. Việt Nam là nền kinh tế hướng xuất khẩu.
* **🔹 FDI (% GDP):** Đo mức độ phụ thuộc vào vốn đầu tư nước ngoài. Quan trọng cho tăng trưởng việc làm.
* **🔹 GDP Growth:** Biến trung tâm trong phân tích Okun’s Law.
* **🔹 Inflation (CPI):** Được dùng để kiểm định Phillips Curve.
* **🔹 Labor Force & Unemployment:** Phản ánh thị trường lao động. Biến phụ thuộc chính trong mô hình thất nghiệp.

---

## 🦠 2. COVID-19 Dataset

### 📌 Cấu trúc dữ liệu
Dữ liệu đã được:
* Lọc theo Việt Nam.
* Aggregate (tổng hợp) theo năm.
* Chuẩn hóa thành các chỉ số ở mức kinh tế vĩ mô (*macro-level indicators*).

### 📊 Các nhóm biến

#### 🔴 (1) Epidemic Scale
| Column | Meaning |
| :--- | :--- |
| `new_cases` | Tổng số ca mới trong năm |
| `new_deaths` | Tổng số tử vong trong năm |
| `total_cases` | Tổng ca tích lũy |
| `total_deaths` | Tổng tử vong tích lũy |
👉 *Phản ánh mức độ nghiêm trọng của dịch bệnh.*

#### 🟡 (2) Smoothed Trend
| Column | Meaning |
| :--- | :--- |
| `new_cases_smoothed` | Trung bình ca nhiễm |
| `new_deaths_smoothed` | Trung bình tử vong |
👉 *Giảm nhiễu dữ liệu theo ngày (daily).*

#### 💉 (3) Vaccination
| Column | Meaning |
| :--- | :--- |
| `total_vaccinations` | Tổng số liều vaccine |
| `people_vaccinated` | Số người đã tiêm |
| `people_fully_vaccinated` | Số người tiêm chủng đầy đủ |
👉 *Đo mức độ phục hồi kinh tế.*

#### 🧪 (4) Testing Capacity
| Column | Meaning |
| :--- | :--- |
| `total_tests` | Tổng số xét nghiệm |
| `positive_rate` | Tỷ lệ dương tính |

#### 🏛 (5) Policy Response
| Column | Meaning |
| :--- | :--- |
| `stringency_index` | Mức độ giãn cách xã hội |
👉 *Proxy cho lockdown / chính sách nhà nước.*

#### 🌍 (6) Macro Controls
| Column | Meaning |
| :--- | :--- |
| `population` | Dân số |
| `gdp_per_capita` | GDP bình quân đầu người |
| `life_expectancy` | Tuổi thọ trung bình |

---

## ⚙️ 3. Derived Features (Biến tạo thêm)

### 🔥 COVID Shock Indicators

* **📌 Normalized impact:** `cases_per_capita`, `deaths_per_capita`  
    👉 *Đo mức độ ảnh hưởng thực tế lên quy mô dân số.*
* **📌 Severity:** `fatality_rate`  
    👉 *Mức độ nguy hiểm của dịch.*
* **📌 Vaccination recovery:** `vaccination_rate`, `full_vaccination_rate`  
    👉 *Phản ánh khả năng phục hồi.*
* **📌 Composite Shock Index:** `covid_intensity_index = 0.6 * cases_per_capita + 0.4 * deaths_per_capita`  
    👉 *Đại diện tổng mức độ cú sốc COVID lên nền kinh tế.*
* **📌 Policy Shock:** `covid_policy_shock = stringency_index`  
    👉 *Mức độ can thiệp của chính phủ.*

---

## 📉 4. Ý nghĩa trong mô hình kinh tế

Dataset này được thiết kế để phục vụ:
1.  **Okun’s Law:** GDP growth ↔ Unemployment
2.  **Phillips Curve:** Inflation ↔ Unemployment
3.  **COVID Shock Analysis:** COVID intensity + policy → GDP & labor market
4.  **Structural macro model:** Exports + FDI + COVID → GDP → Unemployment

---
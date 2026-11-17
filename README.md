# Toolshop Automation Testing

Dự án kiểm thử giao diện tự động cho Toolshop, sử dụng Python 3.12, Playwright và pytest. Bộ smoke test kiểm tra bốn luồng chính trên Chromium. Các thao tác giao diện được tổ chức theo Page Object Model (POM).

## Phạm vi kiểm thử

| Luồng | Kết quả mong đợi |
| --- | --- |
| Tìm kiếm `pliers` | Có ít nhất một kết quả và mọi tên sản phẩm đều chứa `pliers`. |
| Thêm 3 `Claw Hammer` vào giỏ | Số lượng trên biểu tượng giỏ hàng là `3`. |
| Đăng nhập với email không tồn tại | Hiện `Invalid email or password` và URL vẫn kết thúc bằng `/auth/login`. |
| Gửi form liên hệ trống | Hiện `Subject is required` và `Message is required`. |

## Cài đặt

Cần Git, Python 3.12 và kết nối đến môi trường Toolshop được cấu hình trong `.env`.

### Windows PowerShell

```powershell
git clone https://github.com/thuantcn1802/automation-testing-project.git
cd automation-testing-project
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install chromium
if (-not (Test-Path -LiteralPath .env)) { Copy-Item .env.example .env }
```

Nếu đã có môi trường Conda `test` dùng Python 3.12, chạy `conda activate test` thay cho hai lệnh tạo và kích hoạt `.venv`.

### Cấu hình môi trường

[.env.example](.env.example) chứa cấu hình mặc định cho Toolshop. Biến đã đặt trong shell được ưu tiên hơn giá trị trong `.env`.

| Biến | Mục đích |
| --- | --- |
| `BASE_URL` | URL giao diện Toolshop mà smoke test sử dụng. |
| `API_URL` | URL API Toolshop cho fixture `api` và các fixture xác thực. |
| `ROUTE_PREFIX` | Tiền tố định tuyến, để trống với cấu hình mặc định. |
| `GITHUB_API_URL`, `GITHUB_TOKEN` | Cấu hình cho fixture `github`. Smoke test hiện tại không cần token. |

Lưu cấu hình riêng và token trong `.env`. Git bỏ qua tệp này theo [.gitignore](.gitignore).

## Chạy kiểm thử

Chạy bộ smoke test trong [tests/ui/test_smoke.py](tests/ui/test_smoke.py) từ thư mục gốc của repo. Kết quả mong đợi là `4 passed`.

```powershell
python -m pytest -m smoke -v
```

Mở Chromium để quan sát test hoặc giữ lại trace khi có lỗi.

```powershell
python -m pytest -m smoke --headed --slowmo 300
python -m pytest -m smoke --tracing retain-on-failure
```

## Cấu trúc thư mục

```text
.
├── pages/                  # Locator và thao tác theo từng trang
├── tests/
│   └── ui/
│       └── test_smoke.py    # Bốn kịch bản smoke
├── conftest.py             # Fixture dùng chung và cấu hình Playwright
├── pytest.ini              # Cấu hình pytest và danh sách marker
├── requirements.txt       # Phiên bản các thư viện Python
└── .env.example            # Mẫu cấu hình môi trường
```

## Đóng góp

1. Tạo nhánh từ `main` mới nhất và giữ thay đổi trong phạm vi của PR.
2. Đặt locator trong `pages/` và assertion trong `tests/`. Dùng cơ chế tự chờ của Playwright thay cho thời gian chờ cố định. Mỗi test có docstring ghi mục tiêu, điều kiện và kết quả mong đợi.
3. Chạy `python -m pytest -m smoke -v`, rồi đưa kết quả vào mô tả PR.
4. Mở PR vào `main` và chờ ít nhất một thành viên khác duyệt trước khi merge.

---

## Sprint 2

### Cấu trúc bộ kiểm thử cho mốc 18/11

| Loại kiểm thử | Số ca | Tệp và phạm vi |
| --- | ---: | --- |
| API sản phẩm | 7 | [test_products_api.py](tests/api/test_products_api.py) kiểm tra cấu trúc JSON, tìm kiếm theo từ khóa và phản hồi 401/404. |
| API người dùng | 2 | [test_users_api.py](tests/api/test_users_api.py) kiểm tra lỗi 422 khi đăng ký với dữ liệu trống và đọc hồ sơ của tài khoản test đã xác thực. |
| API giỏ hàng | 1 | [test_carts_api.py](tests/api/test_carts_api.py) dùng POST để thêm sản phẩm và GET để xác nhận số lượng đã lưu. |
| Route | 2 | [test_network.py](tests/ui/test_network.py) chặn ảnh để kiểm tra danh sách vẫn hiển thị và giả lập danh sách rỗng để kiểm tra thông báo. |
| UI C.5 | 12 | Bộ test tái sử dụng 4 ca [smoke](tests/ui/test_smoke.py) và bổ sung 8 ca trong [danh mục](tests/ui/test_catalog.py), [giỏ hàng](tests/ui/test_cart.py) và [tài khoản](tests/ui/test_account.py). |

### Phạm vi UI C.5

| Nhóm chức năng | Kịch bản |
| --- | --- |
| Danh sách và tìm kiếm | Tìm `pliers`, tìm từ khóa không có kết quả, sắp xếp theo giá tăng dần |
| Bộ lọc | Lọc danh mục `Hammer` |
| Chi tiết sản phẩm | Đối chiếu tên và giá với danh mục, kiểm tra số lượng giỏ sau khi thêm 3 `Claw Hammer` |
| Giỏ hàng | Kiểm tra thành tiền và tổng giỏ, quay lại danh mục bằng `Continue Shopping` |
| Xác thực | Đăng nhập sai thông tin, gửi form đăng nhập trống |
| Liên hệ và tài khoản | Gửi form liên hệ trống, mở trang tài khoản sau khi đăng nhập |

### Dữ liệu, fixture và marker

- Hai test dùng `pytest.mark.parametrize`. Test tìm kiếm đọc 4 từ khóa từ [data/search_keywords.json](data/search_keywords.json), còn test phản hồi lỗi chạy hai trường hợp 401 và 404.
- [conftest.py](conftest.py) cung cấp fixture theo `session` và `function`. Fixture `test_user` tạo tài khoản riêng cho phiên chạy. `auth_state` đăng nhập qua UI một lần và lưu `storage_state` để `logged_in_page` tái sử dụng.
- Marker `api` chọn 10 ca API, `ui` chọn 14 ca trình duyệt gồm cả 2 ca route, và `smoke` chọn 4 ca kiểm tra nhanh.

### Chạy nghiệm thu

Chạy từ thư mục gốc của repo sau khi kích hoạt môi trường Python theo phần cài đặt ở trên.

```powershell
pytest --collect-only -q
pytest -m api
```

Kết quả mốc 18/11 là `24 tests collected` và `10 passed, 14 deselected`. Pytest loại 14 ca UI và route khỏi lần chạy thứ hai khi lọc theo marker `api`.

| Mục đích | Lệnh | Kết quả đã kiểm chứng |
| --- | --- | --- |
| Chạy toàn bộ bộ kiểm thử | `python -m pytest -v` | `24 passed` |
| Kiểm tra nhanh các luồng chính | `python -m pytest -m smoke -q` | `4 passed, 20 deselected` |

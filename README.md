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

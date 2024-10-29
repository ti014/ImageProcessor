# Image Processor App

Ứng dụng cho phép người dùng cắt hoặc thay đổi kích thước ảnh. Ngoài ra còn có thể tự động phát hiện khuôn mặt để chỉ tập trung cắt vùng gần đó, tự động đổi tên các tệp sau khi xử lý.


## Tính Năng
- **Crop**: Cắt ảnh theo kích thước mục tiêu, tập trung vào khuôn mặt được phát hiện hoặc trung tâm của ảnh..
- **Resize**: Thay đổi kích thước ảnh theo kích thước đã chỉ định.
- **Auto-Rename**: Đổi tên các ảnh đã xử lý bằng UUID duy nhất.
- **Cancel Operation**: Hủy bỏ quá trình xử lý ảnh đang diễn ra bất cứ lúc nào.
- **Progress Tracking**: Theo dõi tiến trình xử lý ảnh thông qua thanh tiến trình.

## Cài Đặt
### Yêu Cầu
- Python > 3.8.x
- Pip (Python package installer)

### Cài Đặt Các Gói Phụ Thuộc:
Để cài đặt các gói cần thiết, chạy lệnh sau:
```bash
pip install -r requirements.txt
```

### Chạy Ứng Dụng
Chạy lệnh sau để khởi động ứng dụng:
```bash
python main.py
```
Ngoài ra, bạn có thể sử dụng tệp .exe có sẵn trong phần phát hành.
## Sử Dụng
1. **Input Folder**: Duyệt để chọn thư mục chứa các ảnh cần xử lý.
2. **Output Folder**: Duyệt để chọn thư mục nơi các ảnh đã xử lý sẽ được lưu.


## Hủy Bỏ Xử Lý
Bạn có thể hủy bỏ tác vụ xử lý ảnh bất cứ lúc nào bằng cách nhấn nút "Cancel".
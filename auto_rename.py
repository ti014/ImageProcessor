import os


def rename_files_recursively(directory):
    index = 0
    for root, _, files in os.walk(directory):
        for filename in files:
            # Lấy phần mở rộng của file
            file_extension = os.path.splitext(filename)[1]

            # Đặt tên mới cho file
            new_name = f"{index}{file_extension}"

            # Đường dẫn đầy đủ đến file cũ và file mới
            old_file = os.path.join(root, filename)
            new_file = os.path.join(root, new_name)

            # Đổi tên file
            os.rename(old_file, new_file)
            print(f"Đổi tên {filename} thành {new_name}")

            # Tăng chỉ số index cho file tiếp theo
            index += 1


# Ví dụ sử dụng
rename_files_recursively(input("Nhập đường dẫn thư mục cần đổi tên file: "))

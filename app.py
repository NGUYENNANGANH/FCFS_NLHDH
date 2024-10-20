
from flask import Flask, render_template, request

app = Flask(__name__)

# Hàm FCFS
def FCFS(dsTienTrinh):
    thoiGianHienTai = 0
    thoiGianChoTB = 0
    thoiGianLuuLaiHeThongTB = 0
    ket_qua = []

    # Sắp xếp tiến trình theo thời gian xuất hiện
    dsTienTrinh.sort(key=lambda x: x[0])  # Sắp xếp theo thời gian xuất hiện

    # Tính toán thời gian hoàn thành, thời gian chờ và thời gian quay vòng
    for tienTrinh in dsTienTrinh:
        id_tienTrinh = tienTrinh[2]  # Lấy chỉ số ID
        if thoiGianHienTai < tienTrinh[0]:
            thoiGianHienTai = tienTrinh[0]  # Nếu CPU rảnh, đợi đến khi tiến trình xuất hiện
        thoiGianHienTai += tienTrinh[1]  # Cập nhật thời gian hiện tại
        thoiDiemKetThuc = thoiGianHienTai
        ket_qua.append(f"Thời điểm kết thúc của tiến trình P{id_tienTrinh}: {thoiDiemKetThuc}")

        thoiGianLuuLaiHeThong = thoiDiemKetThuc - tienTrinh[0]  # Thời gian lưu lại hệ thống
        thoiGianCho = thoiGianLuuLaiHeThong - tienTrinh[1]  # Thời gian chờ

        # Cộng dồn thời gian chờ và thời gian quay vòng
        thoiGianChoTB += thoiGianCho
        thoiGianLuuLaiHeThongTB += thoiGianLuuLaiHeThong

    # Tính toán thời gian chờ và thời gian quay vòng trung bình
    thoiGianChoTB /= len(dsTienTrinh)
    thoiGianLuuLaiHeThongTB /= len(dsTienTrinh)

    # Thêm kết quả thời gian chờ và lưu lại hệ thống trung bình
    ket_qua.append(f"Thời gian chờ trung bình: {thoiGianChoTB}")
    ket_qua.append(f"Thời gian lưu lại hệ thống trung bình: {thoiGianLuuLaiHeThongTB}")

    return ket_qua


# Route cho trang chủ
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        soTienTrinh = int(request.form["soTienTrinh"])
        dsTienTrinh = []
        
        for i in range(soTienTrinh):
            xuatHien = int(request.form[f"xuatHien_{i}"])
            suDung = int(request.form[f"suDung_{i}"])
            dsTienTrinh.append((xuatHien, suDung, i + 1))  # Thêm chỉ số vào tuple

        # Gọi thuật toán FCFS
        ket_qua = FCFS(dsTienTrinh)
        return render_template("index.html", ket_qua=ket_qua, soTienTrinh=soTienTrinh)

    return render_template("index.html", ket_qua=None, soTienTrinh=0)


if __name__ == "__main__":
    app.run(debug=True)

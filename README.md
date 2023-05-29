
# Xác thực, thiết lập để sử dụng Youtube API.
Để có thể gọi được phương thức API từ Youtube, trước hết cần lấy được 3 thông số sau: client_id; client_secret và refresh_token.
Bài viết dưới đây sẽ hướng dẫn tạo và lấy được các thông số đọi
## 1. Lấy các thông số client_id và client_secret
Để sử dụng Youtube API, người dùng cần xác thực thông qua việc sử dụng API key. Việc này giúp cho Google có thể xác định được ai đang sử dụng API và đảm bảo rằng dữ liệu được truy xuất chỉ được sử dụng với mục đích hợp lý. Người dùng cần cung cấp API key trong các yêu cầu API của mình để xác thực.

Dưới đây, là quy trình thiết lập cũng như cấp quyền sử dụng trong Youtube API.

Trong phần này, mục tiêu của ta là sẽ lấy được 1 File có định dạng Json.
- Truy cập vào trang web: [Link](https://console.cloud.google.com/projectselector2/apis/dashboard?organizationId=802485071097&supportedpurview=project)
- Chọn Create Project. Điền một số thông tin cơ bản cho Project (như tên Project, tên Doanh nghiệp, lưu Folder ở đâu).
- Chọn Library ở cột bên trái. Tìm kiếm và kích hoạt: “Youtube data api v3”, “Youtube Analytics API” và “Youtube Reporting API ”. 

![Pic 1](https://github.com/QuangHD-Sconnect/Youtube-API-Web/blob/main/API%20doc%20image/Picture1.png?raw=true)
![Pic 2](https://github.com/QuangHD-Sconnect/Youtube-API-Web/blob/main/API%20doc%20image/Picture2.png?raw=true)
![Pic 3](https://github.com/QuangHD-Sconnect/Youtube-API-Web/blob/main/API%20doc%20image/Picture3.png?raw=true)

- Chọn mục “OAuth Consent Screen” bên trái. Chọn “Configure Consent Screen”. Sau đó chọn “Internal” (Những người được phép sử dụng ứng dụng do bạn tạo ra là những nhân viên nội bộ). Sau đó, điền thông tin cho Ứng dụng. “App name”: Đặt tên App; Địa chỉ Email. “Save and continue”
![Pic 4](https://github.com/QuangHD-Sconnect/Youtube-API-Web/blob/main/API%20doc%20image/Picture4.png?raw=true)
![Pic 5](https://github.com/QuangHD-Sconnect/Youtube-API-Web/blob/main/API%20doc%20image/Picture5.png?raw=true)
![Pic 6](https://github.com/QuangHD-Sconnect/Youtube-API-Web/blob/main/API%20doc%20image/Picture6.png?raw=true)

- Chọn mục “Credentials” bên trái. Sau đó Chọn “Create Credentials” → “OAuth client ID”.
- Sau đó, chọn loại ứng dụng mà bạn định tích hợp API vào. Trong trường hợp này, tôi muốn tạo ra một trang web sử dụng nên sẽ chọn “Web Application”.
- Đặt tên, và một phần quan trọng chúng ta phải thêm đó là link trang web, nhưng vì đây là web được thiết kế cho nội bộ sử dụng nên link của web sẽ có dạng http://localhost:8080 và ta thêm Link: https://developers.google.com/oauthplayground (sẽ có tác dụng ở phần sau)
<space><space> ![Pic 7](https://github.com/QuangHD-Sconnect/Youtube-API-Web/blob/main/API%20doc%20image/Picture7.png?raw=true)
![Pic 8](https://github.com/QuangHD-Sconnect/Youtube-API-Web/blob/main/API%20doc%20image/Picture8.png?raw=true)

- Sau khi nhấn “Save” ta sẽ được hiển thị thông báo như dưới, ta có thể copy 2 thông số client_id; client_secret hoặc nhấn “Download JSON” để tải về File JSON.

 ![Pic 9](https://github.com/QuangHD-Sconnect/Youtube-API-Web/blob/main/API%20doc%20image/Picture9.png?raw=true)

## 2. Lấy các thông số refresh_token
 
- Truy cập vào trang web [Link](https://developers.google.com/oauthplayground/)
- Click vào hình bánh răng cưa (Setting) ở góc trên bên tay phải. Tick vào ô "Use your own OAuth credentials". Paste các thông số client_id; client_secret đã copy phái trên.
![Pic 10](https://github.com/QuangHD-Sconnect/Youtube-API-Web/blob/main/API%20doc%20image/Picture10.png?raw=true)
- Trong phần "Select & authorize APIs", ta nhập dòng sau vào ô input: https://www.googleapis.com/auth/yt-analytics.readonly,https://www.googleapis.com/auth/youtubepartner,https://www.googleapis.com/auth/yt-analytics-monetary.readonly,https://www.googleapis.com/auth/youtube
 ![Pic 11](https://github.com/QuangHD-Sconnect/Youtube-API-Web/blob/main/API%20doc%20image/Picture11.png?raw=true)
- Sang Step 2 ta chỉ cần bấm vào nút "Exchange authorization code for tokens". refresh_token sẽ tự động hiện và ta copy lại.
 ![Pic 12](https://github.com/QuangHD-Sconnect/Youtube-API-Web/blob/main/API%20doc%20image/Picture12.png?raw=true)
 
## 3. Điền thông số
Sau khi đã lấy được 3 thông số ở trên. Ta điền các thông số đó vào File function.py
Trong phần khai báo function get_access_token()

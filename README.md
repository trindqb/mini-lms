
# Mini-LMS (Gradio + Hugging Face Spaces + Firebase)

Chức năng: Nghe (audio + MCQ), Nói (ghi âm), Đọc (trả lời ngắn), Viết (bài luận), Quản trị (xem/CSV).

## Triển khai nhanh
1. Tạo Firebase Project → Firestore, Storage, Service Account (JSON).
2. Tạo Hugging Face Space (Gradio), upload repo.
3. Đặt Secrets:
   - APP_PASSWORD = (ví dụ) 1234
   - FIREBASE_SA_JSON = (nội dung JSON)
   - FIREBASE_PROJECT_ID = your-project-id
   - FIREBASE_STORAGE_BUCKET = your-project.appspot.com
4. Upload file audio mẫu vào `samples/audio_l1.mp3`.
5. Run → Đăng nhập → Thử các tab.

## Ghi dữ liệu
- Firestore collection: `submissions` (fields: ts, ts_int, user, section, item_id, text/mcq_score/audio_path).
- Storage path: `audio/<user>/<file>`.

## Mở rộng
- Thêm nhiều câu MCQ (file JSON).
- Chấm nói: dùng Whisper → text → rubric đánh giá.
- Đăng nhập Firebase Auth (client + verify ID token).

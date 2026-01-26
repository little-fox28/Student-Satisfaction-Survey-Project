import pandas as pd
import re

from src.config import Config


class DataProcessor:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = None
        self.new_column_names = Config.COLUMN_MAPPING
        self.likert_scale_mapping = Config.LIKERT_MAPPING

    def load_data(self):
        print("Loading data...")
        self.data = pd.read_csv(self.file_path, encoding='utf-8')
        return self

    def _rename_columns(self):
        print("Renaming columns...")
        self.data.rename(columns=self.new_column_names, inplace=True)

    def _clean_data(self):
        print("Cleaning data...")
        # Drop PII and unnecessary columns
        self.data.drop(columns=['email', 'consent'], inplace=True)
        
        # Filter out rows that failed the attention check
        self.data = self.data[self.data['attention_check'] == 'Không đồng ý'].copy()
        self.data.drop(columns=['attention_check'], inplace=True)

        # Standardize 'semester'
        self.data['semester'] = self.data['semester'].apply(lambda x: int(re.search(r'\d+', str(x)).group()) if re.search(r'\d+', str(x)) else None)

        # Drop rows with no semester
        self.data.dropna(subset=['semester'], inplace=True)
        self.data['semester'] = self.data['semester'].astype(int)

    def _transform_data(self):
        print("🚀 Khởi động quy trình ETL...")

        # 1. Mapping Header (Chuyển câu hỏi thô sang mã biến tường minh)
        # Bước này phải thực hiện đầu tiên để các bước sau dùng đúng tên cột
        if hasattr(Config, 'COLUMN_MAPPING'):
            self.data.rename(columns=Config.COLUMN_MAPPING, inplace=True)

        # 2. Lọc phản hồi rác (Trap Question) - CỰC KỲ QUAN TRỌNG
        if 'qc_trap_answer' in self.data.columns:
            initial_count = len(self.data)
            # Chỉ giữ lại những người chọn đúng số 2
            self.data = self.data[self.data['qc_trap_answer'] == 2].copy()
            removed_count = initial_count - len(self.data)
            if removed_count > 0:
                print(f"🧹 Đã loại bỏ {removed_count} bản ghi vi phạm câu hỏi bẫy.")

        # 3. Chuyển đổi Timestamp
        if 'timestamp' in self.data.columns:
            self.data['timestamp'] = self.data['timestamp'].str.replace(r'\s[A-Z]{2}\sGMT\+\d+$', '', regex=True)
            self.data['timestamp'] = pd.to_datetime(self.data['timestamp'], errors='coerce')

        # 4. Chuyển đổi Likert Scale (Text -> Int)
        likert_columns = list(self.likert_scale_mapping.keys())
        for col in self.data.columns:
            if self.data[col].dtype == 'object':
                # Kiểm tra nếu 80% dữ liệu thuộc thang đo Likert thì mới map
                if self.data[col].isin(likert_columns).mean() > 0.8:
                    self.data[col] = self.data[col].map(self.likert_scale_mapping)

        # 5. Xử lý câu hỏi đảo ngược (Reverse Coding)
        # Chỉ thực hiện sau khi đã chuyển sang dạng số
        reverse_cols = ['aca_deadline_pressure', 'fin_living_cost_worry']
        for col in reverse_cols:
            if col in self.data.columns:
                self.data[col] = 6 - self.data[col]
                print(f"🔄 Đã đảo ngược điểm cho cột: {col}")

        # 6. Chuẩn hóa GPA (Mở lại để phục vụ phân tích DA)
        # if 'dem_gpa' in self.data.columns and hasattr(Config, 'GPA_MAPPING'):
        #     self.data['dem_gpa'] = self.data['dem_gpa'].map(Config.GPA_MAPPING)

        # 7. Loại bỏ trùng lặp
        self.data.drop_duplicates(inplace=True)

        print(f"✅ Hoàn tất ETL. Dữ liệu sạch sẵn sàng: {len(self.data)} dòng.")
        return self.data


    def save_data(self, output_path: str):
        from pathlib import Path
        print(f"📂 Đang chuẩn bị lưu dữ liệu vào: {output_path}...")

        # 1. Tự động tạo thư mục nếu chưa tồn tại
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        # 2. Lưu dữ liệu
        try:
            self.data.to_csv(output_path, index=False, encoding='utf-8-sig')
            print("✅ Lưu dữ liệu thành công.")
        except Exception as e:
            print(f"❌ Lỗi khi lưu dữ liệu: {e}")
        return self

    def process(self, output_path: str):
        self.load_data()
        self._rename_columns()
        self._clean_data()
        self._transform_data()
        self.save_data(output_path)
        return self.data.head()
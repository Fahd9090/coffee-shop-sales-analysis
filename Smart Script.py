import pandas as pd
import numpy as np

def smart_data_cleaner():
    try:
        file_name = input("الرجاء إدخال اسم الملف المراد تنظيفه (مثال: data.xlsx أو data.csv): ").strip()
        file_name = file_name.strip('"').strip("'")
        
        if file_name.endswith('.csv'):
            df = pd.read_csv(file_name)
        elif file_name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_name)
        else:
            print("عذراً، صيغة الملف غير مدعومة. يرجى استخدام CSV أو Excel.")
            return

        print("\n⏳ جاري تحليل وتطهير البيانات...")
        rows_before = len(df)
        
        df.columns = df.columns.str.strip()
        
        df = df.drop_duplicates(keep='first')
        duplicates_removed = rows_before - len(df)
        
        for col in df.columns:
            if df[col].isnull().sum() > 0:
                if pd.api.types.is_numeric_dtype(df[col]):
                    median_val = df[col].median()
                    df[col].fillna(median_val, inplace=True)
                else:
                    df[col].fillna('Unknown', inplace=True)

        if 'cash_type' in df.columns and 'card' in df.columns:
           df.loc[df['cash_type'].str.strip().str.lower() == 'cash', 'card'] = 'No Card'

        output_name = input("أدخل اسم الملف النظيف الجديد (مثال: Cleaned_Project_1): ").strip()
        if not output_name.endswith(('.xlsx', '.xls')):
            output_name += ".xlsx"

        df.to_excel(output_name, index=False)
        
        print("\n✅ تم تنظيف البيانات ومعالجتها بنجاح تامة!")
        print(f"📊 تقرير العمليات:")
        print(f"- إجمالي الصفوف الأصلية: {rows_before}")
        print(f"- التكرارات المحذوفة: {duplicates_removed}")
        print(f"- تم معالجة جميع الفراغات (NaN) دون خسارة أي صف.")
        print(f"- تم حفظ الملف الجديد باسم: {output_name}")

    except FileNotFoundError:
        print("عذراً، لم يتم العثور على الملف. تأكد من كتابة الاسم الصحيح ومكان وجوده في نفس المجلد.")
    except Exception as e:
        print(f"حدث خطأ غير متوقع: {e}")

smart_data_cleaner()

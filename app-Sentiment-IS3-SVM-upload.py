import streamlit as st
import joblib
import pandas as pd

# โหลดโมเดลที่บันทึกไว้
model = joblib.load('svm_sentiment_model.pkl')

# ฟังก์ชันสำหรับทำนาย Sentiment
def predict_sentiment(text):
    sentiment_map = {1: "😊 Positive", 0: "😐 Neutral", -1: "😡 Negative"}
    prediction = model.predict([text])[0]
    return sentiment_map[prediction]

# UI ของ Streamlit
st.title("📱 Samsung Galaxy S25 Sentiment Analysis")
st.subheader("🔍 วิเคราะห์ความรู้สึกจากรีวิว")

# เลือกโหมดการใช้งาน
option = st.radio("เลือกวิธีการป้อนข้อมูล:", ("📝 กรอกข้อความ", "📂 อัปโหลดไฟล์ Excel"))

# 📌 กรอกข้อความ
if option == "📝 กรอกข้อความ":
    user_input = st.text_area("พิมพ์รีวิวที่นี่", "")
    if st.button("🔍 วิเคราะห์"):
        if user_input:
            result = predict_sentiment(user_input)
            st.success(f"🔍 ผลลัพธ์: {result}")
        else:
            st.warning("⚠️ กรุณาใส่ข้อความก่อนกดปุ่มวิเคราะห์!")

# 📌 อัปโหลดไฟล์ Excel
elif option == "📂 อัปโหลดไฟล์ Excel":
    uploaded_file = st.file_uploader("อัปโหลดไฟล์ Excel (.xlsx)", type=["xlsx"])
    # if uploaded_file:
    #     df = pd.read_excel(uploaded_file)
        
    #     if 'Text' in df.columns:
    #         df['Sentiment'] = df['Text'].apply(predict_sentiment)
    #         st.write(df[['Text', 'Sentiment']])
            
    #         # ดาวน์โหลดผลลัพธ์
    #         output_filename = "sentiment_results.xlsx"
    #         df.to_excel(output_filename, index=False)
    #         st.download_button(
    #             label="📥 ดาวน์โหลดผลลัพธ์",
    #             data=open(output_filename, "rb"),

        if uploaded_file:
            df = pd.read_excel(uploaded_file)

        if 'Text' in df.columns:
            df['Sentiment'] = df['Text'].apply(predict_sentiment)
            st.write(df[['Text', 'Sentiment']])

            # บันทึก DataFrame เป็นไฟล์ Excel
            output_filename = "sentiment_results.xlsx"
            df.to_excel(output_filename, index=False)

            # โหลดไฟล์และแปลงเป็น binary เพื่อให้ Streamlit โหลดได้
            with open(output_filename, "rb") as file:
                file_data = file.read()

            # ปุ่มดาวน์โหลด
            st.download_button(
                label="📥 ดาวน์โหลดผลลัพธ์",
                data=file_data,
                file_name="sentiment_results.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.error("⚠️ ไฟล์ต้องมีคอลัมน์ชื่อ 'Text' เท่านั้น!")

import json
import datetime
import pytz
import cloudscraper

def generate_market_data():
    # 1. ตั้งค่าโซนเวลาพื้นฐานเป็น UTC
    utc_zone = pytz.utc
    today_date = datetime.datetime.now(utc_zone).strftime('%Y-%m-%d')
    
    # 2. โครงสร้าง JSON ที่ EA ของเราจะเข้ามารับไปใช้งาน
    market_data = {
        "valid_for_date": today_date,
        "symbol_keyword": ["XAU", "GOLD", "XAUUSD"],
        "status": "normal", 
        "close_time_utc": "",
        "sources": {
            "ftmo": {"status": "normal", "close_time_utc": ""},
            "cme": {"status": "normal", "close_time_utc": ""}
        }
    }

    # 3. เตรียม Cloudscraper ไว้เจาะระบบเว็บ
    scraper = cloudscraper.create_scraper()
    print("✅ System Ready: Cloudscraper is active.")

    # (เดี๋ยวเราจะมาเขียนโค้ดแกะ HTML ของเว็บ FTMO และ CME ใส่ตรงนี้ในสเต็ปถัดไป)
    # ตอนนี้ให้มันสร้างไฟล์รูปแบบมาตรฐานออกมาก่อน เพื่อทดสอบระบบอัตโนมัติบน GitHub

    # 4. บันทึกข้อมูลลงไฟล์ ftmo_time.json
    with open('ftmo_time.json', 'w') as json_file:
        json.dump(market_data, json_file, indent=4)
        print(f"✅ Data updated for {today_date}: {market_data['status']}")

if __name__ == "__main__":
    generate_market_data()
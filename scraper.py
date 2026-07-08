import json
import datetime
import pytz
import requests

def fetch_us_holidays(year):
    """ดึงข้อมูลวันหยุดสหรัฐฯ จาก Public API (Nager.Date) ซึ่งมีผลกับตลาดทองคำและดัชนีสหรัฐฯ"""
    url = f"https://date.nager.at/api/v3/PublicHolidays/{year}/US"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            holidays = response.json()
            return {item['date']: item['name'] for item in holidays}
    except Exception as e:
        print(f"❌ API Error: {e}")
    return {}

def generate_market_data():
    utc_zone = pytz.utc
    now = datetime.datetime.now(utc_zone)
    today_date = now.strftime('%Y-%m-%d')
    
    # 1. โครงสร้าง JSON มาตรฐานสำหรับ Boatswain EA
    market_data = {
        "valid_for_date": today_date,
        "symbol_keyword": ["XAU", "GOLD", "USD", "SPX", "US500"],
        "status": "normal", 
        "close_time_utc": "",
        "event_name": "None",
        "sources": {
            "cme_us": {"status": "normal", "event": "None"}
        }
    }

    print("✅ System Ready: Boatswain Scraper is active.")
    
    # 2. ดึงข้อมูลวันหยุดของปีนี้
    us_holidays = fetch_us_holidays(now.year)
    print(f"📅 Loaded {len(us_holidays)} US Holidays for {now.year}")

    # 3. ตรวจสอบว่าวันนี้ (หรือพรุ่งนี้) เป็นวันหยุดที่มีผลกระทบหรือไม่
    # XAUUSD และ SP500 มักจะปิดเวลา 18:00 หรือ 17:00 UTC (Early Close) ในวันหยุด
    if today_date in us_holidays:
        event_name = us_holidays[today_date]
        market_data["status"] = "early_close"
        # ปกติวันหยุด US ตลาดโลหะ/ดัชนี มักจะปิดช่วง 17:00 - 18:00 UTC
        # เพื่อความปลอดภัยขั้นสูงสุด เราตั้งเวลาบังคับปิดเป็น 17:00 UTC ของวันนั้น
        market_data["close_time_utc"] = f"{today_date} 17:00:00" 
        market_data["event_name"] = event_name
        market_data["sources"]["cme_us"] = {"status": "early_close", "event": event_name}
        print(f"⚠️ ALERT: US Holiday Detected today! ({event_name}) - Set to Early Close")

    # 4. บันทึกข้อมูลลงไฟล์ ftmo_time.json
    with open('ftmo_time.json', 'w', encoding='utf-8') as json_file:
        json.dump(market_data, json_file, indent=4, ensure_ascii=False)
        print(f"✅ Data updated for {today_date}: {market_data['status']}")

if __name__ == "__main__":
    generate_market_data()
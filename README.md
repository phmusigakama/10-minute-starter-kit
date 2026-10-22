# 10-Minute Starter Kit

ช่วยให้คนที่ "หัวว่าง" กลับมาได้จุดเริ่มต้นของไอเดีย ภายใน 10 นาที
— พิมพ์มั่ว 2 นาที (ห้ามลบ) → ตัดทางเลือก → ให้ AI ช่วยขึ้นต้น → ได้ไอเดียไปต่อยอด

🌐 **ใช้งานออนไลน์:** https://10-minute-starter-kit.vercel.app

## ทำไมต้อง "ห้ามลบ"

ตอนพิมพ์ ให้คนเขียนทำงานก่อน คนตัดสินค่อยมาทีหลัง
ถ้าลบทุกครั้งที่ไม่ถูกใจ คุณจะหยุดคิดแล้วเริ่มวิจารณ์ตัวเอง
ไอเดียแย่ ๆ มักพาไปถึงไอเดียที่ใช่ จึงเก็บไว้ก่อน แล้วค่อยตัดทิ้งในขั้น 2

## ความสามารถ

| ขั้น | ทำอะไร |
|---|---|
| 1 | พิมพ์มั่ว 2 นาที — นาฬิกานับถอยหลัง, ล็อกปุ่ม Backspace/Delete, พูดด้วยเสียง, เขียนภาษาไทยผ่าน IME ได้ปกติ |
| 2 | AI จัดระเบียบเป็นรายการ → ติ๊กเก็บ / กด ✕ ทิ้ง / เขียนคอมเมนต์, พูดเพิ่มความคิดได้ |
| 3 | ให้ AI ร่างไอเดีย 2-3 แบบ → แก้ต่อในช่องข้อความ |
| สรุป | สรุปเป็น Markdown → คัดลอกไปวางใน Notion / Google Docs ได้ทันที |

- ภาษาไทย + English (สลับได้มุมขวาบน)
- บันทึกงานอัตโนมัติลง localStorage (ปิดเท็บไปแล้วกลับมาได้)
- Responsive ทั้งมือถือและเดสก์ท็อป, เคารพ `prefers-reduced-motion`
- ปุ่มสถานะมุมขวาบนบอกว่า AI พร้อมใช้งานไหม

## โครงสร้าง

```
index.html        หน้าเว็บทั้งหมด (ไฟล์เดียว ไม่ต้อง build)
_core.py          โมดูลแชร์: prompt, ตัด JSON, เรียก OpenRouter
api/segment.py    POST /api/segment  → จัดระเบียบความคิด
api/draft.py      POST /api/draft    → ร่างไอเดีย
api/status.py     GET  /api/status   → เซิร์ฟเวอร์มี API key ไหม
server.py         เซิร์ฟเวอร์แบบ standalone (ใช้รันในเครื่อง)
vercel.json       ตั้งค่า Vercel
```

## AI ทำงานอย่างไร

- เรียก `https://openrouter.ai/api/v1/chat/completions` ผ่าน serverless function
- โมเดลไล่ลำดับ: `google/gemma-4-26b-a4b-it:free` → `google/gemma-4-26b-a4b-it` → `google/gemma-3-27b-it`
  ถ้าโมเดลแรกติด rate limit (429) ระบบข้ามไปตัวถัดไปให้อัตโนมัติ และข้ามตัวที่ติดลิมิตไป 10 นาที
- ถ้า AI ล่ม หน้าเว็บจะใช้ตัวสำรอง (ตัดข้อความ + ร่างจากแม่แบบ) โดยไม่พัง flow
- **คีย์อยู่ฝั่งเซิร์ฟเวอร์เท่านั้น** ผู้ใช้ไม่ต้องกรอกอะไรในหน้าเว็บ

## รันในเครื่อง

```bash
python server.py        # เปิด http://localhost:8000
```

ใส่คีย์ในไฟล์ `.env` ข้างๆ `server.py` (ดู `.env.example`) — ไม่ต้อง pip install อะไร

## ปล่อยขึ้น Vercel

1. สร้าง project (ชื่อ `10-minute-starter-kit`)
2. ใส่ environment variable: `OPENROUTER_API_KEY` → type **Sensitive** (secret)
   - Production / Preview / Development ทั้งหมด
3. Deploy — Vercel จะอ่าน `api/*.py` เป็น serverless functions และเสิร์ฟ `index.html` เป็นหน้าเว็บ
4. ผู้ใช้เรียก `/api/segment`, `/api/draft`, `/api/status` ได้เลย

> หมายเหตุ: rate limit ที่มีในโค้ดเป็นแบบ in-memory ซึ่งจะไม่คงอยู่ข้าม instance บน serverless
> ถ้าปล่อยจริงและกังวลเรื่องค่าใช้จ่าย ให้เพิ่ม rate limiting ที่ระดับ Vercel/WAF

## การพูดด้วยเสียง (Voice Input)

ใช้ Web Speech API ของเบราว์เซอร์

- รองรับ: Chrome, Edge, Safari (มือถือและคอมพิวเตอร์) — Firefox ยังไม่รองรับ
- ต้องเปิดผ่าน `https://` หรือ `localhost`
- ถ้าใช้ไม่ได้ ปุ่มจะถูกปิดใช้งานพร้อมข้อความอธิบาย

## ความเป็นส่วนตัว

ข้อความที่ผู้ใช้พิมพ์จะถูกส่งไปประมวลผลที่ OpenRouter เพื่อจัดระเบียบและร่างไอเดีย
ควรแจ้งผู้ใช้ให้ทราบ (หน้าเว็บมีข้อความแจ้งอยู่แล้ว) และควรมีนโยบายความเป็นส่วนตัวของคุณ

## หมายเหตุเรื่องคีย์

- อย่า commit ไฟล์ `.env` (มีใน `.gitignore` แล้ว)
- บน Vercel ให้ใส่คีย์เป็น Environment Variable แบบ Secret
- ถ้าคีย์หลุด ให้ revoke ที่ https://openrouter.ai/keys ทันที

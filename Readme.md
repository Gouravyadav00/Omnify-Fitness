# 🧘 Omnify-Fitness Booking API

A simple, modular Fitness Class Booking API built using **FastAPI** and **SQLite**, designed as part of the Omnify Developer Assignment. It enables users to view fitness classes, book them, and view bookings by email, with proper timezone management and input validation.

---

## 📌 Features

- 🔍 List upcoming classes (`GET /classes`)
- 🧾 Book a class (`POST /book`)
- 📬 Retrieve bookings by email (`GET /bookings`)
- ⏰ Timezone-aware (IST-based, supports conversions)
- ⚠️ Overbooking & input validation handled
- 🧪 Unit test-ready structure

---

## 🏗️ Tech Stack

- Python 3.10+
- FastAPI
- SQLite (in-memory or file-based)
- Pydantic
- Uvicorn (for running the server)
- pytz / zoneinfo for timezone handling

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/Gouravyadav00/Omnify-Fitness.git
cd Omnify-Fitness

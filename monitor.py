#!/usr/bin/env python3
import os, json, time, requests, smtplib, logging
from email.mime.text import MIMEText
from datetime import datetime

def send_email(price, url):
    sender = os.environ["EMAIL_USER"]
    password = os.environ["EMAIL_PASS"]
    recipient = os.environ["EMAIL_USER"]

    msg = MIMEText(f"Test Alert!\n\nShopee item price: {price}\nLink: {url}")
    msg["Subject"] = "Shopee Price Alert (TEST)"
    msg["From"] = sender
    msg["To"] = recipient

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)

# -----------------------------
# TEST MODE – force trigger
# -----------------------------
if __name__ == "__main__":
    test_price = 9999
    test_url = "https://shopee.ph/airpods-pro-2-test"
    send_email(test_price, test_url)
    print("✅ Test email sent!")

# # CONFIG from env (set in GitHub Secrets / workflow)
# GMAIL_USER = os.getenv("GMAIL_USER")
# GMAIL_PASS = os.getenv("GMAIL_PASS")
# TO_EMAIL   = os.getenv("TO_EMAIL", GMAIL_USER)
# CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL_SECONDS", "0"))  # not used in Actions run; kept for compatibility
# PRODUCTS_FILE = "products.json"
# STATE_FILE = "state.json"
# PRICE_DIVISOR = int(os.getenv("PRICE_DIVISOR", "100000"))

# logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

# def load_products():
#     with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
#         return json.load(f)

# def load_state():
#     if os.path.exists(STATE_FILE):
#         try:
#             return json.load(open(STATE_FILE, "r", encoding="utf-8"))
#         except Exception:
#             return {}
#     return {}

# def save_state(state):
#     with open(STATE_FILE, "w", encoding="utf-8") as f:
#         json.dump(state, f)

# def get_price(shopid, itemid):
#     url = f"https://shopee.ph/api/v4/item/get?itemid={itemid}&shopid={shopid}"
#     r = requests.get(url, timeout=12)
#     r.raise_for_status()
#     j = r.json()
#     data = j.get("data") or {}
#     # attempt several keys
#     price_raw = None
#     for key in ("price", "price_min", "price_max", "price_before_discount"):
#         if key in data and data[key] is not None:
#             price_raw = data[key]
#             break
#     if price_raw is None:
#         # nested fallback
#         if "item" in data and isinstance(data["item"], dict):
#             for key in ("price", "price_min", "price_max"):
#                 if key in data["item"]:
#                     price_raw = data["item"][key]
#                     break
#     if price_raw is None:
#         raise ValueError("price not found in Shopee response")
#     try:
#         price = float(price_raw) / PRICE_DIVISOR
#     except Exception:
#         price = float(price_raw)
#     return price

# def send_email(subject, body):
#     if not (GMAIL_USER and GMAIL_PASS and TO_EMAIL):
#         logging.error("Email config missing.")
#         return False
#     msg = MIMEText(body)
#     msg["Subject"] = subject
#     msg["From"] = GMAIL_USER
#     msg["To"] = TO_EMAIL
#     try:
#         with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
#             smtp.login(GMAIL_USER, GMAIL_PASS)
#             smtp.sendmail(GMAIL_USER, [TO_EMAIL], msg.as_string())
#         return True
#     except Exception as e:
#         logging.exception("Failed sending email")
#         return False

# def main():
#     products = load_products()
#     if not products:
#         logging.error("No products in products.json")
#         return
#     state = load_state()
#     for p in products:
#         shopid = p.get("shopid")
#         itemid = p.get("itemid")
#         name = p.get("name", f"{shopid}/{itemid}")
#         target = float(p.get("target", 0))
#         key = f"{shopid}_{itemid}"
#         try:
#             price = get_price(shopid, itemid)
#             logging.info(f"{name}: ₱{price:.2f} (target ₱{target:.2f})")
#             last_alert = state.get(key, {}).get("last_alert_price")
#             # Alert only if price <= target AND (no previous alert at same or lower price)
#             if price <= target and (last_alert is None or price < last_alert - 0.01):
#                 body = (f"{name} price alert!\n\nCurrent price: ₱{price:.2f}\nTarget: ₱{target:.2f}\n\n"
#                         f"Link: https://shopee.ph/product/{shopid}/{itemid}/\nTime (UTC): {datetime.utcnow().isoformat()}Z")
#                 ok = send_email(f"Price Alert: {name} ₱{price:.2f}", body)
#                 if ok:
#                     state.setdefault(key, {})["last_alert_price"] = price
#                     state[key]["last_alert_time"] = datetime.utcnow().isoformat()
#                     logging.info(f"Alert sent for {name}")
#             # always record last_seen_price
#             state.setdefault(key, {})["last_seen_price"] = price
#         except Exception as e:
#             logging.exception(f"Error checking {name}")
#         # small throttle to avoid hitting Shopee too fast
#         time.sleep(2)
#     save_state(state)

# if __name__ == "__main__":
#     main()


import streamlit as st
import json
import os
from datetime import datetime
import random

st.set_page_config(page_title="📧 Todo Gmail Pro", layout="wide")

USER_FILE = "users.json"
TASK_FILE = "tasks.json"

# ===== LOAD / SAVE =====
def load_json(file, default):
    if os.path.exists(file):
        try:
            with open(file, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return default
    return default

def save_json(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

users = load_json(USER_FILE, {})
tasks_db = load_json(TASK_FILE, {})

# FIX lỗi list cũ
if isinstance(tasks_db, list):
    tasks_db = {}

# ===== CAPTCHA =====
def generate_captcha():
    a = random.randint(1, 9)
    b = random.randint(1, 9)
    return (a, b, a + b)

if "captcha" not in st.session_state or st.session_state.captcha is None:
    st.session_state.captcha = generate_captcha()

# ===== SESSION =====
if "user" not in st.session_state:
    st.session_state.user = None
if "selected" not in st.session_state:
    st.session_state.selected = None

# ================= LOGIN =================
if not st.session_state.user:
    st.title("🔐 Todo Gmail Pro")

    tab1, tab2 = st.tabs(["Đăng nhập", "Đăng ký"])

    # ===== LOGIN =====
    with tab1:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")

        st.write(f"🤖 {st.session_state.captcha[0]} + {st.session_state.captcha[1]} = ?")
        cap = st.text_input("Nhập CAPTCHA")

        if st.button("Login"):
            if str(st.session_state.captcha[2]) != cap:
                st.error("Sai CAPTCHA 🤖")
                st.session_state.captcha = generate_captcha()
            elif u in users and users[u] == p:
                st.session_state.user = u
                st.session_state.captcha = None
                st.rerun()
            else:
                st.error("Sai tài khoản")

    # ===== REGISTER =====
    with tab2:
        u2 = st.text_input("Tạo username")
        p2 = st.text_input("Tạo password", type="password")

        st.write(f"🤖 {st.session_state.captcha[0]} + {st.session_state.captcha[1]} = ?")
        cap2 = st.text_input("Nhập CAPTCHA", key="cap2")

        if st.button("Register"):
            if str(st.session_state.captcha[2]) != cap2:
                st.error("Sai CAPTCHA 🤖")
                st.session_state.captcha = generate_captcha()
            elif u2 in users:
                st.error("Đã tồn tại")
            elif u2.strip() == "" or p2.strip() == "":
                st.warning("Không được để trống")
            else:
                users[u2] = p2
                tasks_db[u2] = []
                save_json(USER_FILE, users)
                save_json(TASK_FILE, tasks_db)
                st.success("Đăng ký thành công!")

    st.stop()

# ================= APP =================
user = st.session_state.user

if user not in tasks_db:
    tasks_db[user] = []

tasks = tasks_db[user]

# ===== SIDEBAR =====
st.sidebar.title(f"👤 {user}")

if st.sidebar.button("🚪 Logout"):
    st.session_state.user = None
    st.rerun()

menu = st.sidebar.radio("", ["📥 Inbox", "⭐ Star", "✅ Done"])
search = st.sidebar.text_input("🔍 Search")

st.sidebar.write("---")

# ===== COMPOSE (FORM SUBMIT) =====
with st.sidebar.form("compose", clear_on_submit=True):
    st.subheader("✏️ Add Task")
    title = st.text_input("Title")
    content = st.text_area("Content")
    submitted = st.form_submit_button("🚀 Submit")

    if submitted and title.strip():
        tasks.append({
            "id": len(tasks) + 1,
            "title": title,
            "content": content,
            "done": False,
            "star": False,
            "time": datetime.now().strftime("%d-%m %H:%M")
        })
        save_json(TASK_FILE, tasks_db)
        st.rerun()

# ===== FILTER =====
filtered = []
for t in tasks:
    if menu == "⭐ Star" and not t["star"]:
        continue
    if menu == "✅ Done" and not t["done"]:
        continue
    if search and search.lower() not in t["title"].lower():
        continue
    filtered.append(t)

# ===== LAYOUT =====
col1, col2 = st.columns([2, 3])

# ===== LIST =====
with col1:
    st.subheader("📩 Tasks")

    for t in filtered:
        c1, c2, c3 = st.columns([1, 6, 2])

        with c1:
            if st.button("⭐" if t["star"] else "☆", key=f"s{t['id']}"):
                t["star"] = not t["star"]
                save_json(TASK_FILE, tasks_db)
                st.rerun()

        with c2:
            title = f"~~{t['title']}~~" if t["done"] else t["title"]
            if st.button(title, key=f"open{t['id']}"):
                st.session_state.selected = t["id"]

        with c3:
            st.caption(t["time"])

# ===== DETAIL =====
with col2:
    if st.session_state.selected:
        task = next((x for x in tasks if x["id"] == st.session_state.selected), None)

        if task:
            st.markdown(f"## {task['title']}")
            st.write(task["content"])

            done = st.checkbox("Done", value=task["done"])
            task["done"] = done

            colA, colB = st.columns(2)

            with colA:
                if st.button("💾 Save"):
                    save_json(TASK_FILE, tasks_db)
                    st.success("Saved!")

            with colB:
                if st.button("🗑 Delete"):
                    tasks.remove(task)
                    save_json(TASK_FILE, tasks_db)
                    st.session_state.selected = None
                    st.rerun()
    else:
        st.info("Chọn task để xem")

# ===== AUTO SAVE =====
save_json(TASK_FILE, tasks_db)
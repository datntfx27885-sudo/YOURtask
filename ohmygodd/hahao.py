import streamlit as st
import sqlite3

DB_NAME = "tasks.db"

def get_conn():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            done INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def get_tasks():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT id, name, done FROM tasks ORDER BY id")
    rows = c.fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "done": bool(r[2])} for r in rows]

def add_task(name):
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO tasks (name, done) VALUES (?, ?)", (name, 0))
    conn.commit()
    conn.close()

def toggle_task(task_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("UPDATE tasks SET done = NOT done WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def remove_task(task_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

init_db()
with st.sidebar:
    image = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTXVMSfVuPxT62YPwRrqhxzjuy4W6SsZi4PeMcCuOTPqA&s"
    st.image(image, caption ='HÉ LÔ ANH BẠN')
    st.title('CHÀO MỪNG ĐẾN VỚI TO ĐÔ LÍT CỦA CHÚNG TÔI')
    st.write('ĐÂy là nơi đánh dấu nhiệm vụ của các bạn khi làm xong( bấm done để hoàn thành) ')
    st.write('còn nếu các bạn thấy nhiệm vụ này có vẻ không phù hợp thì các bạn cứ thẳng tay xóa cho đỡ nặng máy chủ sever :))')
    st.write('SUBMIT để xem hoàn thành đến đâu')
    st.write('chúc các bạn xài VUI VẺ :)')
st.set_page_config(page_title="Todo List", page_icon="📝")
st.title("Todo List📋")
if st.button("UPDATE có gì hay ho :))?"):
    st.write("Bản cập nhật v1.0")
    st.write("+ 1 tasks giao diện người dùng bình thường")
    st.write("+ 1 tung tung tung sahur")
    st.write("- 99999 auras")
    st.write("Cảm ơn bạn đã dùng và ủng hộ :))")
with st.form("Add Task➕"):
    new_task = st.text_input("New Task📑")
    submitted = st.form_submit_button("Submit📬")
    if submitted:
        st.balloons()
        if new_task.strip():
            add_task(new_task)
            st.rerun()

tasks = get_tasks()
for task in tasks:
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        if task['done']:
            st.write(f"~~{task['name']}~~ ✅")
        else:
            st.write(f"{task['name']}")
    with col2:
        if task['done']:
            update_btn_name = 'To Do'
        else:
            update_btn_name = 'Done'
        update_btn = st.button(update_btn_name, key=f"{task['id']}u")
        if update_btn:
            toggle_task(task["id"])
            st.rerun()
    with col3:
        delete_btn = st.button("Remove", key=f"{task['id']}d")
        if delete_btn:
            remove_task(task["id"])
            st.rerun()

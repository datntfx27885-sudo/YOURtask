import streamlit as st
with st.sidebar:
    st.title('CHÀO MỪNG ĐẾN VỚI TO ĐÔ LÍT CỦA CHÚNG TÔI')
    st.write('ĐÂy là nơi đánh dấu nhiệm vụ của các bạn khi làm xong( bấm done để hoàn thành) ')
    st.write('còn nếu các bạn thấy nhiệm vụ này có vẻ không phù hợp thì các bạn cứ thẳng tay xóa cho đỡ nặng máy chủ sever :))')
    st.write('SUBMIT để xem hoàn thành đến đâu')
    st.write('chúc các bạn xài VUI VẺ :)')
st.set_page_config(page_title="Todo List", page_icon="📝")
st.title("To do List👍")

with st.form("Add Task"):
    new_task = st.text_input("New Task")
    submitted = st.form_submit_button("Submit")

tasks = [
    {'id': 1, 'name': 'ăn cơm', 'done': True},
    {'id': 2, 'name': 'học bài', 'done': False}
]

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

    with col3:
        delete_btn = st.button("Remove", key=f"{task['id']}d")
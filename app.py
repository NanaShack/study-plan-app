import streamlit as st
from datetime import date
import json
DATA_FILE = "records.json"
STUDY_LOG_FILE = "study_logs.json"
try:
    with open(DATA_FILE, "r", encoding= "utf-8") as f:
        saved_records = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    saved_records = []
try:
    with open(STUDY_LOG_FILE, "r", encoding="utf-8") as f:
        saved_study_logs = json. load(f)
except(FileNotFoundError, json.JSONDecodeError):
    saved_study_logs = []
st.title("学習計画アプリ")
st.write("資格勉強の計画と進捗を管理するアプリです。")
qualification = st.text_input("資格名")
goal = st.number_input("目標勉強時間(時間)", min_value=1, value=100, step=1)
exam_date = st.date_input("試験日")
days_left = (exam_date - date.today()).days
progress = 0
total_minutes = 0
if "study_logs" in st.session_state:
    for log in st.session_state.study_logs:
        if log[1] == qualification:
            total_minutes += log[2]
progress = min(int(total_minutes / (goal* 60)* 100), 100)

st.subheader("現在の学習状況")

st.write("資格名", qualification)
st.write("学習目標" , goal)
st.write("試験日" , exam_date)
st.metric("進捗率" , f"{progress}%")
st.progress(progress)
if st.button("保存"):
    st.success("保存しました!")
st.write("試験日まであと：" , days_left , "日")
if "records" not in st.session_state:
    st.session_state.records = saved_records
if "study_logs" not in st. session_state:
    st.session_state. study_logs = saved_study_logs  
if st.button("一覧に追加"):
    st.session_state.records.append([qualification, goal, exam_date.isoformat(), progress])
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state.records, f, ensure_ascii=False)
st.divider()
st.subheader("資格一覧")
for i, record in enumerate (st.session_state.records):
    st.subheader(record[0])
    st.write("目標", record[1])
    st.write("試験日", record[2])
    total_minutes = 0
    if "study_logs" in st.session_state:
        for log in st.session_state.study_logs:
            if log[1] == record[0]:
                total_minutes += log[2]
    try:
        target_hours = float(record[1])
    except(ValueError, TypeError):
        target_hours = 0
    if target_hours >0:
        record_progress =min(int(total_minutes / (target_hours* 60)* 100), 100)
        st.write("進捗率", record_progress, "%")
    else:
        st.write("進捗率：目標勉強時間を設定しなおしてください")
    if st.button("削除", key = f"delete_{i}"):
        st.session_state.records.pop(i)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(st.session_state.records, f, ensure_ascii=False)
        st.rerun()
    st.divider()
st.subheader("毎日の勉強記録")
study_date = st.date_input("勉強日")
study_subject = st.text_input("勉強した資格")
study_minutes = st.number_input("勉強時間(分)", min_value=0, step=1)
if st.button("勉強時間を追加"):
    if "study_logs" not in st.session_state:
        st.session_state.study_logs = []
    st.session_state.study_logs.append([study_date.isoformat(), study_subject, study_minutes])
    with open(STUDY_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump (st.session_state.study_logs, f, ensure_ascii=False)
st.subheader("勉強履歴")
if "study_logs" in st.session_state:
    for log in st.session_state.study_logs:
        st.write(log[0], "|", log[1], "|", log[2], "分")

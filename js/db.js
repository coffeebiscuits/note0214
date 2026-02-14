import PouchDB from 'pouchdb';

// DB 인스턴스 생성
const focusDB = new PouchDB('focus_records');
const habitDB = new PouchDB('habit_records');
const moodDB = new PouchDB('mood_records');
const goalDB = new PouchDB('goal_records');

// 집중 기록 저장
export async function saveFocusRecord(start, end, duration, tags = []) {
  const record = {
    _id: new Date().toISOString(),
    start_time: start,
    end_time: end,
    duration,
    tags
  };
  return await focusDB.put(record);
}

// 습관 기록 저장
export async function saveHabitRecord(name, date, status, notes = '') {
  const record = {
    _id: `${name}-${date}`,
    habit_name: name,
    date,
    status,
    notes
  };
  return await habitDB.put(record);
}

// 감정 기록 저장
export async function saveMoodRecord(date, mood, intensity, notes = '') {
  const record = {
    _id: `${date}-${mood}`,
    date,
    mood,
    intensity,
    notes
  };
  return await moodDB.put(record);
}

// 목표 기록 저장
export async function saveGoalRecord(goal, deadline, progress = 0) {
  const record = {
    _id: new Date().toISOString(),
    goal,
    created_at: new Date().toISOString(),
    deadline,
    progress
  };
  return await goalDB.put(record);
}

// 모든 기록 조회
export async function getAllRecords(db) {
  const result = await db.allDocs({ include_docs: true });
  return result.rows.map(row => row.doc);
}

// 특정 기록 삭제
export async function deleteRecord(db, id) {
  const doc = await db.get(id);
  return await db.remove(doc);
}

// 전체 초기화 (모든 기록 삭제)
export async function resetDatabase(db) {
  await db.destroy(); // DB 자체를 삭제
  return new PouchDB(db.name); // 같은 이름으로 새 DB 생성
}

// 내보내기 (JSON)
export async function exportRecords(db) {
  const records = await getAllRecords(db);
  return JSON.stringify(records, null, 2);
}

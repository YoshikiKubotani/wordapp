-- dev スキーマが存在しない場合に作成
CREATE SCHEMA IF NOT EXISTS dev;
-- test スキーマが存在しない場合に作成
CREATE SCHEMA IF NOT EXISTS test;

-- item テーブルが存在しない場合に作成
CREATE TABLE IF NOT EXISTS dev.item (
    id INT PRIMARY KEY,
    english TEXT,
    japanese TEXT,
    grade INT
);

-- 既存のデータを削除
TRUNCATE TABLE dev.item;

-- 新しいデータを挿入
\COPY dev.item (id, english, japanese, grade) FROM '/docker-entrypoint-initdb.d/default_word_list.csv' WITH (FORMAT csv, DELIMITER ',', HEADER, ENCODING 'UTF8');

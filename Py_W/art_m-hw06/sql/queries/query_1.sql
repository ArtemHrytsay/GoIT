-- Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
SELECT  s.first_name || ' ' || s.last_name as "Student",
        ROUND(AVG(g.grade), 2) AS "Average grade"
FROM    students s
JOIN    grades g ON s.id = g.student_id
GROUP BY "Student"
ORDER BY "Average grade" DESC
LIMIT 5;
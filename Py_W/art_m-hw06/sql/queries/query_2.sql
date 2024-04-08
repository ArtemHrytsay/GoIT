-- Знайти студента із найвищим середнім балом з певного предмета.
SELECT  d.discipline_name as "Discipline",
        s.first_name || ' ' || s.last_name AS "Student",
        ROUND(AVG(g.grade), 2) AS "Average grade"
FROM    grades g
JOIN    students s ON g.student_id = s.id
JOIN    disciplines d ON g.discipline_id = d.id
WHERE   d.id = 1
GROUP BY "Student"
ORDER BY "Average grade" DESC
LIMIT 1;
-- Знайти які курси читає певний викладач.
SELECT  t.first_name || ' ' || t.last_name AS "Teacher",
        d.discipline_name as "Discipline"
FROM    teachers t
JOIN    disciplines d ON d.teacher_id = t.id
WHERE   t.id = 5;
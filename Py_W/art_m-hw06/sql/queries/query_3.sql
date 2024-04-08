-- Знайти середній бал у групах з певного предмета.
SELECT  d.discipline_name as "Discipline",
        gp.group_name as "Group",
        ROUND(AVG(gr.grade), 2) AS "Average grade"
FROM    grades gr
JOIN    students s ON gr.student_id = s.id
JOIN    disciplines d ON gr.discipline_id = d.id
JOIN    groups gp ON s.group_id = gp.id
WHERE   d.id = 5
GROUP BY "Group"
ORDER BY "Average grade" DESC;
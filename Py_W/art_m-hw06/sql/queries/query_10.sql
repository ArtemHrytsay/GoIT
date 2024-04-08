-- Список курсів, які певному студенту читає певний викладач.
SELECT DISTINCT s.first_name || ' ' || s.last_name AS "Student",
        t.first_name || ' ' || t.last_name AS "Teacher",
        d.discipline_name AS "Discipline"
FROM    grades g
JOIN    students s ON g.student_id = s.id
JOIN    disciplines d ON g.discipline_id = d.id
JOIN    teachers t ON d.teacher_id = t.id
WHERE   (
        s.id = 5
        AND t.id = 2
        );
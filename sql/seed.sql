set names utf8mb4;

insert into
    stroke_types (name) 
values
    ('recto_vertical'),
    ('recto_horizontal'),
    ('recto_diagonal'),
    ('curva'),
    ('onda'),
    ('circulo'),
    ('espiral'),
    ('arco'),
    ('letra'),
    ('libre');


INSERT INTO exercises (name, description, stroke_type_id, is_active)
SELECT 'Líneas verticales', 'Trazar líneas rectas de arriba hacia abajo', stroke_type_id, true
FROM stroke_types WHERE name = 'recto_vertical';

INSERT INTO exercises (name, description, stroke_type_id, is_active)
SELECT 'Líneas horizontales', 'Trazar líneas rectas de izquierda a derecha', stroke_type_id, true
FROM stroke_types WHERE name = 'recto_horizontal';

INSERT INTO exercises (name, description, stroke_type_id, is_active)
SELECT 'Curvas simples', 'Trazar curvas suaves en una dirección', stroke_type_id, true
FROM stroke_types WHERE name = 'curva';

INSERT INTO exercises (name, description, stroke_type_id, is_active)
SELECT 'Ondas', 'Trazar líneas onduladas de forma continua', stroke_type_id, true
FROM stroke_types WHERE name = 'onda';

INSERT INTO exercises (name, description, stroke_type_id, is_active)
SELECT 'Círculos', 'Trazar círculos completos cerrando el trazo', stroke_type_id, true
FROM stroke_types WHERE name = 'circulo';

INSERT INTO exercises (name, description, stroke_type_id, is_active)
SELECT 'Espirales', 'Trazar espirales desde el centro hacia afuera', stroke_type_id, true
FROM stroke_types WHERE name = 'espiral';

INSERT INTO exercises (name, description, stroke_type_id, is_active)
SELECT 'Arcos', 'Trazar arcos semicirculares de forma controlada', stroke_type_id, true
FROM stroke_types WHERE name = 'arco';

INSERT INTO exercises (name, description, stroke_type_id, is_active)
SELECT 'Letras individuales', 'Trazar letras simples siguiendo el patrón correcto', stroke_type_id, true
FROM stroke_types WHERE name = 'letra';

INSERT INTO exercises (name, description, stroke_type_id, is_active)
SELECT 'Trazo libre', 'Ejercicio de escritura libre', stroke_type_id, false
FROM stroke_types WHERE name = 'libre';
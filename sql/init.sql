create database if not exists GIIA_lapiz_inteligente;

use GIIA_lapiz_inteligente;

create table users (
    user_id int unsigned primary key auto_increment,
    name varchar(80) not null,
    lastname varchar(80) not null,
    email varchar(150) not null unique,
    password varchar(255) not null,
    phone varchar(9),
    is_active bool not null default true,
    created_at timestamp not null default current_timestamp,
    updated_at timestamp default current_timestamp on update current_timestamp
);

create table children (
    child_id int unsigned primary key auto_increment,
    user_id int unsigned not null,
    name varchar(80) not null,
    birth_date date,
    dominant_hand enum('derecha', 'izquierda', 'ambidiestro') not null default 'derecha',
    school_grade varchar(30),
    notes text,
    created_at timestamp not null default current_timestamp,
    updated_at timestamp not null default current_timestamp on update current_timestamp,
    foreign key (user_id) references users(user_id)
);

create table stroke_types (
    stroke_type_id int unsigned primary key auto_increment,
    name varchar(50) not null unique,
    created_at timestamp not null default current_timestamp
);

create table exercises (
    exercise_id int unsigned primary key auto_increment,
    name varchar(50) not null,
    description text null,
    -- difficulty_level tinyint not null check (difficulty_level between 1 and 5),
    stroke_type_id int unsigned not null,
    is_active boolean not null default true,
    created_at timestamp not null default current_timestamp,
    updated_at timestamp not null default current_timestamp on update current_timestamp,
    foreign key (stroke_type_id) references stroke_types(stroke_type_id)
);

create table sessions (
    session_id int unsigned primary key auto_increment,
    child_id int unsigned not null,
    exercise_id int unsigned not null,
    started_at timestamp not null default current_timestamp,
    ended_at timestamp,
    avg_pressure float,
    max_pressure float,
    pressure_stability float,
    movement_stability float,
    tremor_level float,
    posture_score float,
    total_errors smallint unsigned default 0,
    feedback_count smallint unsigned default 0,
    ai_score float,
    result_summary text,
    created_at timestamp not null default current_timestamp,
    foreign key (child_id) references children(child_id),
    foreign key (exercise_id) references exercises(exercise_id)
);

/*
CREATE TABLE session_readings (
    reading_id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,

    session_id INT UNSIGNED NOT NULL,

    recorded_at DATETIME NOT NULL,

    -- aceler�metro
    accel_x FLOAT,
    accel_y FLOAT,
    accel_z FLOAT,

    -- giroscopio
    gyro_x FLOAT,
    gyro_y FLOAT,
    gyro_z FLOAT,

    -- presi�n
    pressure FLOAT,

    CONSTRAINT fk_readings_session
        FOREIGN KEY (session_id)
        REFERENCES sessions(session_id)
        ON DELETE CASCADE
);
*/

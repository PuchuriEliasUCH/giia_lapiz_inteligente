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
    created_at datetime not null default current_timestamp,
    updated_at datetime default current_timestamp on update current_timestamp
);

create table children (
    child_id int unsigned primary key auto_increment,
    user_id int unsigned not null,
    name varchar(80) not null,
    birth_date date,
    dominant_hand enum('derecha', 'izquierda', 'ambidiestro') not null default 'derecha',
    school_grade varchar(30),
    notes text,
    is_active bool not null default true,
    created_at datetime not null default current_timestamp,
    updated_at datetime not null default current_timestamp on update current_timestamp,
    foreign key (user_id) references users(user_id)
);

create table stroke_types (
    stroke_type_id int unsigned primary key auto_increment,
    name varchar(50) not null unique,
    created_at datetime not null default current_timestamp
);

create table exercises (
    exercise_id int unsigned primary key auto_increment,
    name varchar(50) not null,
    description text,
    stroke_type_id int unsigned not null,
    is_active bool not null default true,
    created_at datetime not null default current_timestamp,
    updated_at datetime not null default current_timestamp on update current_timestamp,
    foreign key (stroke_type_id) references stroke_types(stroke_type_id)
);

create table sessions (
    session_id int unsigned primary key auto_increment,
    child_id int unsigned not null,
    exercise_id int unsigned not null,
    started_at datetime not null default current_timestamp,
    ended_at datetime,
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
    created_at datetime not null default current_timestamp,
    foreign key (child_id) references children(child_id),
    foreign key (exercise_id) references exercises(exercise_id)
);

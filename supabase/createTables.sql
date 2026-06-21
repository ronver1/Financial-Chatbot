-- Author: Ronit Verma
-- Created on: 6.21.26

-- This file is a creates the tables used in the database

create table users (
  id uuid primary key default gen_random_uuid(),
  username text not null, 
  token_hash text not null, 
  created_at timestamp default now()
);

create table sessions  (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references users(id),
  started_at timestamp default now(),
  ended_at timestamp,
  status text default 'active'
);

create table recommendations (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references users(id),
  session_id uuid references sessions(id),
  created_at timestamp default now()
);
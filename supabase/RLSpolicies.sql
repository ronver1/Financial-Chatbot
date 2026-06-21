-- Author: Ronit Verma
-- Created on: 6.21.26

-- This file includes RLS policies

create policy "no public access"
on users
for all
to anon, authenticated
using (false);

create policy "no public access"
on sessions
for all
to anon, authenticated
using (false);

create policy "no public access"
on recommendations
for all
to anon, authenticated
using (false);
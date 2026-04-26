-- Mini X schema for Supabase.
-- Run this in: Supabase Dashboard > SQL Editor.

create table if not exists public.posts (
  id           uuid        primary key default gen_random_uuid(),
  user_id      uuid        not null references auth.users(id) on delete cascade,
  author_email text,
  content      text        not null check (char_length(content) between 1 and 280),
  created_at   timestamptz not null default now()
);

create index if not exists posts_created_at_idx
  on public.posts (created_at desc);

alter table public.posts enable row level security;

drop policy if exists "posts are readable by anyone" on public.posts;
create policy "posts are readable by anyone"
  on public.posts
  for select
  using (true);

drop policy if exists "users can insert their own posts" on public.posts;
create policy "users can insert their own posts"
  on public.posts
  for insert
  with check (auth.uid() = user_id);

drop policy if exists "users can delete their own posts" on public.posts;
create policy "users can delete their own posts"
  on public.posts
  for delete
  using (auth.uid() = user_id);

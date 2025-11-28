-- WARNING: This schema is for context only and is not meant to be run.
-- Table order and constraints may not be valid for execution.

CREATE TABLE public.chunks (
  id uuid NOT NULL DEFAULT uuid_generate_v4(),
  document_id uuid NOT NULL,
  chunk_index integer NOT NULL,
  chunk_text text NOT NULL,
  created_at timestamp without time zone DEFAULT now(),
  CONSTRAINT chunks_pkey PRIMARY KEY (id),
  CONSTRAINT chunks_document_id_fkey FOREIGN KEY (document_id) REFERENCES public.documents(id)
);
CREATE TABLE public.documents (
  id uuid NOT NULL DEFAULT uuid_generate_v4(),
  entity_id uuid NOT NULL,
  title text,
  content text NOT NULL,
  created_at timestamp without time zone DEFAULT now(),
  CONSTRAINT documents_pkey PRIMARY KEY (id),
  CONSTRAINT documents_entity_id_fkey FOREIGN KEY (entity_id) REFERENCES public.entities(id)
);
CREATE TABLE public.embeddings (
  id uuid NOT NULL DEFAULT uuid_generate_v4(),
  chunk_id uuid NOT NULL,
  embedding USER-DEFINED NOT NULL,
  created_at timestamp without time zone DEFAULT now(),
  CONSTRAINT embeddings_pkey PRIMARY KEY (id),
  CONSTRAINT embeddings_chunk_id_fkey FOREIGN KEY (chunk_id) REFERENCES public.chunks(id)
);
CREATE TABLE public.entities (
  id uuid NOT NULL DEFAULT uuid_generate_v4(),
  user_id uuid NOT NULL,
  project_id uuid,
  type text NOT NULL,
  raw_data jsonb NOT NULL,
  created_at timestamp without time zone DEFAULT now(),
  summary text,
  CONSTRAINT entities_pkey PRIMARY KEY (id),
  CONSTRAINT entities_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id),
  CONSTRAINT entities_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id)
);
CREATE TABLE public.languages_stats (
  id uuid NOT NULL DEFAULT uuid_generate_v4(),
  language text NOT NULL UNIQUE,
  total_bytes bigint DEFAULT 0,
  projects_count integer DEFAULT 0,
  users_count integer DEFAULT 0,
  usage_percentage real DEFAULT 0,
  created_at timestamp without time zone DEFAULT now(),
  updated_at timestamp without time zone DEFAULT now(),
  user_id uuid,
  CONSTRAINT languages_stats_pkey PRIMARY KEY (id),
  CONSTRAINT languages_stats_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id)
);
CREATE TABLE public.project_languages (
  id uuid NOT NULL DEFAULT uuid_generate_v4(),
  project_id uuid NOT NULL,
  language text NOT NULL,
  bytes bigint,
  created_at timestamp without time zone DEFAULT now(),
  CONSTRAINT project_languages_pkey PRIMARY KEY (id),
  CONSTRAINT project_languages_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id)
);
CREATE TABLE public.projects (
  id uuid NOT NULL DEFAULT uuid_generate_v4(),
  user_id uuid NOT NULL,
  repo_name text NOT NULL,
  description text,
  stars integer,
  forks integer,
  last_commit timestamp without time zone,
  created_at timestamp without time zone DEFAULT now(),
  project_type text NOT NULL DEFAULT 'github'::text,
  source_url text,
  CONSTRAINT projects_pkey PRIMARY KEY (id),
  CONSTRAINT projects_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id)
);
CREATE TABLE public.user_languages (
  id uuid NOT NULL DEFAULT uuid_generate_v4(),
  user_id uuid NOT NULL,
  language text NOT NULL,
  bytes bigint,
  repos_count integer,
  created_at timestamp without time zone DEFAULT now(),
  CONSTRAINT user_languages_pkey PRIMARY KEY (id),
  CONSTRAINT user_languages_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id)
);
CREATE TABLE public.users (
  id uuid NOT NULL DEFAULT uuid_generate_v4(),
  username text NOT NULL UNIQUE,
  name text,
  bio text,
  avatar_url text,
  created_at timestamp without time zone DEFAULT now(),
  github_username text UNIQUE,
  CONSTRAINT users_pkey PRIMARY KEY (id)
);
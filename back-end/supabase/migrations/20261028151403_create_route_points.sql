create table route_points (
    id uuid primary key default gen_random_uuid(),

    route_id uuid not null references routes(id) on delete cascade,
    point_name text not null,

    latitude double precision not null,
    longitude double precision not null,
    
    created_at timestamp default now(),
    updated_at timestamp default now()
);

create index idx_route_points_route_id on route_points(route_id);
create index idx_route_points_point_name on route_points(point_name);

create rls policy "Allow all" on route_points for all using (true);
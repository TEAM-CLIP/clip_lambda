

create_table_query = """
    create table if not exists recommend_request(
        id bigint primary key auto_increment,
        phone_number varchar(50) not null,
        prefer_style text not null,
        snap_types json,
        created_at datetime default current_timestamp
    );
    """


insert_query = """
    insert into recommend_request(phone_number, prefer_style, snap_types) values (%s, %s, %s)
    """
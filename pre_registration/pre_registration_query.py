

create_table_query = """
    create table if not exists pre_registration_request(
        id bigint primary key auto_increment,
        phone_number varchar(50) not null,
        service_name text not null,
        created_at datetime default current_timestamp
    );
    """


insert_query = """
    insert into pre_registration_request(phone_number, service_name) values (%s, %s)
    """

check_exist_query = """
    select id from pre_registration_request where phone_number = %s LIMIT 1;
"""
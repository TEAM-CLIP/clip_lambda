

create_table_query = """
    create table if not exists pre_registration_request(
        id bigint primary key auto_increment,
        phone_number varchar(50) not null,
        hangout text not null,
        created_at datetime default current_timestamp
    );
    """


insert_query = """
    insert into pre_registration_request(phone_number, hangout) values (%s, %s)
    """
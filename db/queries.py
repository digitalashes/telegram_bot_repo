from contextlib import closing
from sqlite3 import Connection as SqliteConnection
from typing import Dict


def add_user(conn: SqliteConnection,
             user_data: Dict) -> None:
    external_id = user_data.pop('id')
    user_data['external_id'] = external_id

    with closing(conn.cursor()) as cursor:
        cursor.execute("""
            insert into users(external_id, first_name, last_name, username, is_bot)
            select :external_id, :first_name, :last_name, :username, :is_bot
            where not exists(select 1 from users where external_id = :external_id)
        """, user_data)
        conn.commit()


def delete_user(conn: SqliteConnection,
                user_id: int) -> None:
    with closing(conn.cursor()) as cursor:
        cursor.execute("""
            delete from users where external_id = :external_id
        """, {'external_id': user_id})
        conn.commit()

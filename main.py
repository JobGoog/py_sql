

import psycopg2
from pprint import pprint



#  создания таблиц
def create_db(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients(
        id SERIAL PRIMARY KEY,
        name VARCHAR(20) NOT NULL,
        lastname VARCHAR(30),
        email VARCHAR(254)
        );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS phonenumbers(
        number VARCHAR(11) PRIMARY KEY,
        client_id INTEGER REFERENCES clients(id)
        );
    """)
    
    return

# Заполнение телефона
def add_tel(cur, tel, client_id):
    cur.execute("""
        INSERT INTO phonenumbers (number, client_id)
        VALUES (%s, %s)
        """, (client_id, tel))
    return client_id

# Заполнение данных клиента
def add_client(cur, name=None, surname=None, email=None, tel=None):
    cur.execute("""
        INSERT INTO clients(name, lastname, email)
        VALUES (%s, %s, %s)
        """, (name, surname, email))
    cur.execute("""
        SELECT id from clients
        ORDER BY id DESC
        LIMIT 1
        """)
    id = cur.fetchone()[0]
    if tel is None:
        return id
    else:
        add_tel(cur, id, tel)
        return id
    
# Удаление телефона
def delete_phone(cur, number):
    cur.execute("""
        DELETE 
        FROM phonenumbers 
        WHERE number = %s
        """, (number, ))
    return number


# Удаление клиента
def delete_client(cur, id):
    cur.execute("""
        DELETE 
        FROM phonenumbers
        WHERE client_id = %s
        """, (id, ))
    cur.execute("""
        DELETE 
        FROM clients 
        WHERE id = %s
       """, (id,))
    return id

def update_client(cur, id, name=None, surname=None, email=None):
    cur.execute("""
        SELECT * 
        FROM clients
        WHERE id = %s
        """, (id, ))
    info = cur.fetchone()
    if name is None:
        name = info[1]
    if surname is None:
        surname = info[2]
    if email is None:
        email = info[3]
    cur.execute("""
        UPDATE clients
        SET name = %s, lastname = %s, email =%s 
        WHERE id = %s
        """, (name, surname, email, id))
    return id

# Поиск 
def find_client(cur, name=None, surname=None, email=None, tel=None):
    if name is None:
        name = '%'
    else:
        name = '%' + name + '%'
    if surname is None:
        surname = '%'
    else:
        surname = '%' + surname + '%'
    if email is None:
        email = '%'
    else:
        email = '%' + email + '%'
    if tel is None:
        cur.execute("""
            SELECT c.id, c.name, c.lastname, c.email, p.number 
            FROM clients c
            LEFT JOIN phonenumbers p ON c.id = p.client_id
            WHERE c.name LIKE %s AND c.lastname LIKE %s
            AND c.email LIKE %s
            """, (name, surname, email))
    else:
        cur.execute("""
            SELECT c.id, c.name, c.lastname, c.email, p.number 
            FROM clients c
            LEFT JOIN phonenumbers p ON c.id = p.client_id
            WHERE c.name LIKE %s AND c.lastname LIKE %s
            AND c.email LIKE %s AND p.number like %s
            """, (name, surname, email, tel))
    return cur.fetchall()


def delet_db(cur):
    cur.execute("""
    DROP TABLE clients, phonenumbers CASCADE;
    """)
    return


if __name__ == '__main__':
    with psycopg2.connect(database = 'py_sql', user = 'postgres', password = 'ipad4ilove') as conn:
        with conn.cursor() as curs:
            delet_db(curs)
            create_db(curs)
            print('Database Create')
            print('Add client: ', 
                   add_client(curs, "Евгений", "Фомин", "roro4250522@gmail.com"))
            print('Add client: ', 
                   add_client(curs, "Роман", "Ефремов", "crepp@gmail.com", '89607304949'))
            print('Add client: ', 
                   add_client(curs, "Кирилл", "Сорокин", "asdasdasd@gmail.com", '83245655196'))
            print('Add client: ', 
                   add_client(curs, "Дмитрий", "Попов", "psdokmjf@gmail.com", '83245675288'))
            print('Add client: ', 
                   add_client(curs, "Арам", "Соколов", "lolo123123@gmail.com"))
            print('Add client: ', 
                   add_client(curs, "Илья", "Круглов", "sdfsdf23@gmail.com"))
            print('Add client: ', 
                   add_client(curs, "Егор", "Иванов", "kokklol2@gmail.com"))
            
            print('Data add to DB')

            curs.execute("""
                SELECT c.id, c.name, c.lastname, c.email, p.number 
                FROM clients c
                LEFT JOIN phonenumbers p ON c.id = p.client_id
                ORDER by c.id
                """)
            
            pprint(curs.fetchall())

            print("Phone add to client id: ",
                  add_tel(curs, 1, '89877453278'))
            print("Phone add to client id: ",
                  add_tel(curs, 3, '89625424545'))
            print("Phone add to client id: ",
                  add_tel(curs, 6, '86305204000'))
            
            print('Data add to DB')

            curs.execute("""
                SELECT c.id, c.name, c.lastname, c.email, p.number 
                FROM clients c
                LEFT JOIN phonenumbers p ON c.id = p.client_id
                ORDER by c.id
                """)
            
            pprint(curs.fetchall())
            
            print("Change client data id: ",
                  update_client(curs, 7, "Иван", None, 'ivan_2050@list.ru'))
            
            print("Delet numder: ",
                  delete_phone(curs, '89607304949'))
            
            print("Data Save")

            curs.execute("""
                SELECT c.id, c.name, c.lastname, c.email, p.number 
                FROM clients c
                LEFT JOIN phonenumbers p ON c.id = p.client_id
                ORDER by c.id
                """)
            
            pprint(curs.fetchall())

            print("Delet client id: ",
                  delete_client(curs, 5))
            
            curs.execute("""
                SELECT c.id, c.name, c.lastname, c.email, p.number 
                FROM clients c
                LEFT JOIN phonenumbers p ON c.id = p.client_id
                ORDER by c.id
                """)
            
            pprint(curs.fetchall())

            print('Find client by Name:')
            print(find_client(curs, 'Евгений'))

            print('Find client by email:')
            print(find_client(curs, None, None, 'ivan_2050@list.ru'))

            print('Find client by Name, SurName, email:')
            print(find_client(curs, 'Дмитрий', 'Попов',   'psdokmjf@gmail.com'))

            print('Find client by Name, SurName, Phonenumber, email:')
            print(find_client(curs, 'Илья', 'Круглов','sdfsdf23@gmail.com', '86305204000'))

            print('Find client by Name, SurName, Phonenumber:') 
            print(find_client(curs, None, None, None, '89877453278'))


conn.close()

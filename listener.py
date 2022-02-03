import socket
import sqlite3
import time

TCP_IP = socket.gethostname()
TCP_PORT = 5115
BUFFER_SIZE = 1024

t0 = 1600000000
DBFNAME = 'data.sqlite'

def init_db():
    db = sqlite3.connect('data.sqlite')
    db.execute('create table if not exists devices (uuid text, name text, created_at integer)')
    db.commit()
    db.close()

init_db()

def now():
    return int(time.time()) - t0

def add_device(uuid, name):
    print(f'adding device', uuid, name)
    if has_device(uuid):
        print(f'device with uuid {uuid} already exists')
        return False

    db = sqlite3.connect('data.sqlite')
    db.execute('insert into devices values (?,?,?)', (uuid, name, now()))
    db.commit()

    print('inserted into devices table')
    print()
    datatablename = 'd_' + uuid.split('-')[0]
    db.execute(f'create table if not exists {datatablename} (dt integer primary key autoincrement, value number)')
    db.commit()

    print('created data table', datatablename)
    db.close()

    return True

def has_device(uuid):
    db = sqlite3.connect('data.sqlite')
    res = [row for row in db.execute(f'select * from devices where uuid = "{uuid}"')]
    db.close()
    return len(res)

def insert_value(uuid, value):
    if not has_device(uuid):
        add_device(uuid, "Peter's Walkolution")
    
    db = sqlite3.connect('data.sqlite')
    datatablename = 'd_' + uuid.split('-')[0]
    db.execute(f"INSERT INTO {datatablename}(dt, value) VALUES (MAX(?, (SELECT seq FROM sqlite_sequence) + 1), ?);", (now() ,value ))
    db.commit()
    db.close()




def launchListener():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    while 1:
        conn, addr = s.accept()
        # print('Connection address:', addr)
        data = b''
        while 1:
            rcv = conn.recv(BUFFER_SIZE)
            data += rcv
            if not rcv: break
        
        try:
            uuid, value = data.decode('ascii').strip().split()
            value = float(value)
        except:
            print('error parsing data', data)
            break


        insert_value(uuid, value)

        print(uuid, value)
        # conn.send(b'OK\n')
        # time.sleep(1)
        conn.close()


if __name__ == '__main__':
    launchListener()
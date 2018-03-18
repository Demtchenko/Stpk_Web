#!/usr/bin/env python3
import asyncio
import functools
import socket
from concurrent.futures import ThreadPoolExecutor


def clnt(s, n):
    try:
        conn, addr = s.accept()
    except OSError:
        return
    print('Клиент', n, addr)
    data = b''
    while data.decode('utf-8').strip() != 'close':
        data = conn.recv(1024)
        conn.send(data)
        print('Клнт', n, data.decode('utf-8').strip())
    conn.shutdown(socket.SHUT_RDWR)
    conn.close
    print(n, 'Закрыли соединение')


def main(cnt, ipa, prt, tmot):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(tmot)
        s.bind((ipa, prt))
        s.listen(cnt)

        xctr = ThreadPoolExecutor(cnt)
        fclnts = list()
        loop = asyncio.get_event_loop()
        loop.set_debug(True)
        for i in range(cnt):
            # fclnts.append(asyncio.ensure_future(loop.run_in_executor(xctr, functools.partial(clnt, s, i))))
        # для совместимости с версией 3.4.3 на Степике заменим
            fclnts.append(asyncio.async(loop.run_in_executor(xctr, functools.partial(clnt, s, i))))
        loop.run_until_complete(asyncio.gather(*fclnts))
        loop.close()
        s.shutdown(socket.SHUT_RDWR)
        s.close()


if __name__ == '__main__':
    main(10, '0.0.0.0', 2222, 15)

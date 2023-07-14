# -*- coding: utf-8 -*-

import sys
import signal
import threading

from twisted.internet import reactor, endpoints, task, protocol
from twisted.logger import Logger, globalLogPublisher, FilteringLogObserver, LogLevel, LogLevelFilterPredicate, textFileLogObserver

import click

from network.factory import GameServerFactory, RingggoClientFactory

import game

WORKER_FRQ = 0.1

MANU_HOST = '192.168.40.254'
MANU_PORT = 9996


from network import ringggo_packet


class RingggoProtocol(protocol.Protocol):
    __logger = Logger(__name__)
    
    def connectionMade(self):
        self.__logger.info('New Connection')

    def connectionLost(self, reason):
        self.__logger.info('Lost Connection: (reason: {})'.format(reason.getErrorMessage()))

    def dataReceived(self, data):
        header = ringggo_packet.Header.from_bytes(data[0:8])
        print(header)
        packet = ringggo_packet.Packet.from_bytes(data[8:])
        print(packet)
        if header.code not in []:
            if header.code == ringggo_packet.Header.PK_POSITION_OBJECTS:
                print(f'{header.car_number} - {packet.body}')
            elif header.code == ringggo_packet.Header.PK_BUMP_NOTI:
                print(f'car no {header.car_number} - bumped {packet.body.bump_point}')
            elif header.code == ringggo_packet.Header.PK_GAME_STEP_CHANGE_NOTI:
                print(f'{packet.body.step} step')
            elif header.code == ringggo_packet.Header.PK_GAME_EVENT_NOTI:
                print(f'{packet.body.event} event')
            else:
                print('invalid code')


class RingggoFactory(protocol.ClientFactory):
    __logger = Logger(__name__)

    def __init__(self):
        self.protocol = None

    def buildProtocol(self, addr):
        self.__logger.info('addr: {}'.format(addr))
        self.protocol = RingggoProtocol() 
        return self.protocol


@click.command()
@click.option('--port', default=1234, type=click.INT, required=True, help='set server port(default: 1234)')
def main(port):
    predicate = LogLevelFilterPredicate(defaultLogLevel=LogLevel.debug)
    observer = FilteringLogObserver(textFileLogObserver(outFile=sys.stdout), [predicate])
    observer._encoding = 'utf-8'
    globalLogPublisher.addObserver(observer)

    logger = Logger('MainThread')
    logger.info('let\'s go spicy')
    logger.info('I\'m too spicy, too, too, I\'m too spicy')

    tcp_server_endpoint = endpoints.TCP4ServerEndpoint(reactor, port)
    game_server_factory = GameServerFactory()
    tcp_server_endpoint.listen(game_server_factory)

    tcp_client_endpoint = endpoints.TCP4ClientEndpoint(reactor, MANU_HOST, MANU_PORT, timeout=5)
    ringggo_client_factory = RingggoFactory()
    # ringggo_client_factory = RingggoClientFactory()
    tcp_client_endpoint.connect(ringggo_client_factory)

    worker = task.LoopingCall(game_server_factory.worker)
    worker_deferred = worker.start(WORKER_FRQ, False)
    worker_deferred.addCallback(game_server_factory.cbWorkerDone)
    worker_deferred.addErrback(game_server_factory.ebWorkerFailed)

    def shutdown_handler(_=None, __=None):
        game.app.exit_arcade()
        reactor.callFromThread(reactor.stop)

    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    threading.Thread(target=reactor.run, args=(False,)).start()

    game.app.start_arcade(game_server_factory)


if __name__ == '__main__':
    main()

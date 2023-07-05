# -*- coding: utf-8 -*-

import sys
import signal
import threading

from twisted.internet import reactor, endpoints, task
from twisted.logger import Logger, globalLogPublisher, FilteringLogObserver, LogLevel, LogLevelFilterPredicate, textFileLogObserver

import click

from network.factory import GameServerFactory

import game

WORKER_FRQ = 0.1

MANU_HOST = '192.168.40.254'
MANU_PORT = 9998

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

    # tcp_client_endpoint = endpoints.TCP4ClientEndpoint(reactor, MANU_HOST, MANU_PORT)
    # game_server_factory = GameServerFactory()
    # tcp_client_endpoint.connect(game_server_factory)

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

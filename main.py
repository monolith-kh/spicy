# -*- coding: utf-8 -*-

import sys
import signal
import threading

from twisted.internet import reactor, endpoints, task
from twisted.logger import Logger, globalLogPublisher, FilteringLogObserver, LogLevel, LogLevelFilterPredicate, textFileLogObserver

from network.factory import GameServerFactory

import game

PORT = 1234
WORKER_FRQ = 0.1


def main():
    predicate = LogLevelFilterPredicate(defaultLogLevel=LogLevel.debug)
    observer = FilteringLogObserver(textFileLogObserver(outFile=sys.stdout), [predicate])
    observer._encoding = 'utf-8'
    globalLogPublisher.addObserver(observer)

    logger = Logger('MainThread')
    logger.info('let\'s go spicy')
    logger.info('I\'m too spicy, too, too, I\'m too spicy')

    tcp_server_endpoint = endpoints.TCP4ServerEndpoint(reactor, PORT)
    game_server_factory = GameServerFactory()
    tcp_server_endpoint.listen(game_server_factory)

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

# Module:   node
# Date:     ...
# Author:   ...

"""Node

...
"""

from .client import Client
from .server import Server

from circuits import handler, BaseComponent


class Node(BaseComponent):
    """Node

    ...
    """

    channel = "node"

    def __init__(self, bind=None, channel=channel, **kwargs):
        super(Node, self).__init__(channel=channel, **kwargs)

        self.bind = bind
        self.nodes = {}

        if self.bind is not None:
            self.server = Server(
                self.bind,
                channel=channel,
                **kwargs
            ).register(self)
        else:
            self.server = None

    def add(self, name, host, port, **kwargs):
        channel = kwargs.pop('channel', '%s_client_%s' % (self.channel, name))
        node = Client(host, port, channel=channel, **kwargs)
        node.register(self)

        self.nodes[name] = node
        return channel

    @handler("remote")
    def _on_remote(self, event, e, client_name, channel=None):
        node = self.nodes[client_name]
        if channel is not None:
            e.channels = (channel,)
        return node.send(event, e)

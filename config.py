import logging

# This is a minimal configuration to get you started with the Text mode.
# If you want to connect Errbot to chat services, checkout
# the options in the more complete config-template.py from here:
# https://raw.githubusercontent.com/errbotio/errbot/master/errbot/config-template.py

BACKEND = 'IRC'  # Errbot will start in text mode (console only mode) and will answer commands from there.
BOT_IDENTITY = {
    'nickname' : 'cibott',
    'username' : 'cibott',    # optional, defaults to nickname if omitted
    'password' : 'rdo-ci-6a547',             # optional
    'server' : 'irc.freenode.net',
    # 'port': 6667,                  # optional
    # 'ssl': True,                  # optional
    # 'ipv6': False,                 # optional
    #'nickserv_password': 'rdo-ci-6a547',     # optional

    ## Optional: Specify an IP address or hostname (vhost), and a
    ## port, to use when making the connection. Leave port at 0
    ## if you have no source port preference.
    ##    example: 'bind_address': ('my-errbot.io', 0)
    # 'bind_address': ('localhost', 0),
}

BOT_ADMINS = ('sshnaidm!*sshnaidm@*', )
CHATROOM_PRESENCE = ('#talcotest', '#talcotest2')

IRC_CHANNEL_RATE = 1
IRC_PRIVATE_RATE = 1
IRC_RECONNECT_ON_KICK = 5
IRC_RECONNECT_ON_DISCONNECT = 5

AUTOINSTALL_DEPS = True

BOT_DATA_DIR = r'/home/sshnaidm/errbot-root/data'
BOT_EXTRA_PLUGIN_DIR = r'/home/sshnaidm/errbot-root/plugins'

BOT_LOG_FILE = r'/home/sshnaidm/errbot-root/errbot.log'
BOT_LOG_LEVEL = logging.DEBUG

DIVERT_TO_PRIVATE = ('help', 'about', 'status')
MESSAGE_SIZE_LIMIT = 500
BOT_ASYNC = True
BOT_ASYNC_POOLSIZE = 20
BOT_ADMINS_NOTIFICATIONS = ("sshnaidm")
BOT_PREFIX = '@'
BOT_PREFIX_OPTIONAL_ON_CHAT = True
BOT_ALT_PREFIXES = ('Err', "bot", "cibot", "cibotik", "errbot")
BOT_ALT_PREFIX_SEPARATORS = (':', ',', ';')
BOT_ALT_PREFIX_CASEINSENSITIVE = True
GROUPCHAT_NICK_PREFIXED = True

# Security
HIDE_RESTRICTED_COMMANDS = True
#HIDE_RESTRICTED_ACCESS = True
SUPPRESS_CMD_NOT_FOUND = True
ACCESS_CONTROLS = {
    'status': {'allowrooms': ('talcotest@*',)},
    'uptime': {'allowusers': BOT_ADMINS},
    'about': {'allowusers': BOT_ADMINS},
    'help': {'allowmuc': False},
    'PatchStatusOnCi:*': {'allowrooms': ('#talcotest',)},
}
CORE_PLUGINS = ('ACLs', 'Help', 'ChatRoom', 'CommandNotFoundFilter', 'Plugins')


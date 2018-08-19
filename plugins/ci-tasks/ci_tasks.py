from errbot import BotPlugin, arg_botcmd
from plugins.utils import get_patch_status
from plugins.utils import get_promotion_status
from plugins.utils import gerrit_status
from plugins.utils import validate_patch
from plugins.utils import BRANCHES


class CiTasks(BotPlugin):
    """
    CI related tasks and scripts
    """

    @arg_botcmd('patch_number', type=str,
                help="Patch number or link to gerrit",
                unpack_args=False)
    def patch_status(self, message, args):
        """A command which returns patch status """
        stat, patch = validate_patch(args.patch_number)
        if stat:
            return get_patch_status(patch)
        return "`%s`{:color='red'}" % patch

    @arg_botcmd('patch_number', type=str,
                help="Patch number or link to gerrit",
                unpack_args=False)
    def patch_result(self, message, args):
        """A command which returns patch status """
        stat, patch = validate_patch(args.patch_number)
        if stat:
            return gerrit_status(patch)
        return "`%s`{:color='red'}" % patch

    @arg_botcmd('branch', type=str, choices=BRANCHES + ['all'], default='all',
                help="Specific branch or all",
                unpack_args=False)
    def promotion_status(self, message, args):
        """A command which returns promotion status for branches """
        return get_promotion_status(args.branch)

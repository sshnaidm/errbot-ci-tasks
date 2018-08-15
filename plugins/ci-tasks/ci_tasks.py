from errbot import BotPlugin, botcmd, arg_botcmd, webhook
from plugins.utils import get_patch_status


class CiTasks(BotPlugin):
    """
    CI related tasks and scripts
    """

    @arg_botcmd('patch_number', type=str,
                help="Patch number or link to gerrit",
                unpack_args=False)
    def patch_status(self, message, args):
        """A command which returns patch status """
        if "http" not in args.patch_number and not args.patch_number.isdigit():
            return "Patch should be either gerrit link or number"
        elif "http" in args.patch_number:
            patch = args.patch_number.strip("/").split("/")[-1]
            if not patch.isdigit():
                return "Patch number contains non-digits"
        else:
            patch = args.patch_number
        if len(patch) > 20:
            return "Patch length should be less than 20"
        status = get_patch_status(patch)
        return status


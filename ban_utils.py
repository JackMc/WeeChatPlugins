# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import_ok = True

try:
    import weechat as w
except:
    print('This script must be run under WeeChat.')
    print('Get WeeChat now at: http://www.weechat.org')
    import_ok = False

import os

SCRIPT_NAME = "BanUtils"
SCRIPT_AUTHOR = "JackMc"
SCRIPT_VERSION = "0.01"
SCRIPT_LICENSE = "MIT"
SCRIPT_DESC = "A set of utilities for easier administration."

BANTXT_CMD = 'bantxt'
AUX_MARK_RANGE_CMD = 'mark_range'


def bantxt_cmd(data, buffer, args):
    split = args.split()
    channel = split[0]
    filename = ' '.join(split[1:])
    server = w.buffer_get_string(buffer, "localvar_server")

    if not os.path.exists(filename):
        filename = os.path.expanduser(filename)
        print(filename)
        with open(filename) as f:
            for line in f:
                w.hook_signal_send('irc_input_send',
                                   w.WEECHAT_HOOK_SIGNAL_STRING,
                                   ("%s;;2;;/mode %s +b *!*@%s" %
                                    (server, channel, line)))
        return w.WEECHAT_RC_OK
    else:
        return w.WEECHAT_RC_ERROR


def aux_mark_range_cmd(data, buffer, args):
    split = args.split()
    server = w.buffer_get_string(buffer, "localvar_server")

    # Get/convert args or error
    try:
        first_num = int(split[0])
        second_num = int(split[1])
        reason = ' '.join(split[2:])
    except:
        return w.WEECHAT_RC_ERROR

    for i in range(first_num, second_num+1):
        w.hook_signal_send('irc_input_send',
                           w.WEECHAT_HOOK_SIGNAL_STRING,
                           # TODO: Make this a configuration option
                           ("%s;;2;;/msg ##wp-aux !mark %d %s" %
                            (server, i, reason)))
    return w.WEECHAT_RC_OK


# For some reason, Weechat thinks every command needs a post-hook...
# So we define this to add to commands which don't need one.
def general_finish():
    pass


def main():
    w.hook_command(BANTXT_CMD, SCRIPT_DESC,
                   "<channel> <filename>",
                   '''
                   channel: The channel to perform the ban-from-text on.
                   filename: Name of the file to ban from (separated by newlines).
                   ''',
                   '%(filename)',
                   'bantxt_cmd', 'general_finish')

    w.hook_command(AUX_MARK_RANGE_CMD, SCRIPT_DESC,
                   "<first_to_mark> <last_to_mark> <reason>",
                   '''
                   first_to_mark: First ban # to mark
                   last_to_mark: last ban # to mark
                   reason: Reason to mark the bans with
                   ''',
                   '',
                   'aux_mark_range_cmd', 'general_finish')

if __name__ == '__main__' and import_ok:
    if w.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION,
                  SCRIPT_LICENSE, SCRIPT_DESC, "", ""):
        main()

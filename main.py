import api
import sm
import extra_
import uos
class shell_re:
    def __init__(self):
        self.nowstr = ''
        self.echo = True
    def addstr(self,toaddstr,end = '\n'):
        self.nowstr += toaddstr
        if self.echo:
            api.system.api_print(toaddstr,end = end)
    def reset(self):
        self.nowstr = ''
    def echo_on(self):
        self.echo = True
    def echo_off(self):
        self.echo = False
print_ = shell_re()
def cmd_cd(args):
    if not args:
        print_.addstr('usage:cd <dir>')
        return 1
    try:
        uos.chdir(args[0])
    except Exception as e:
        print_.addstr(f'cd failed,log:{e}')
        return 1
    return 0
def cmd_ls(args):
    print_.addstr(get_state())
    return 0
def get_state():
    output = ''
    for i in api.system.listdir():
        if (api.system.stat(i)[0] & 0x8000) != 0:
            output += f'{i}   file   {round(uos.stat(i)[6] / 1024,2)}KiB\n'
        else:
            output += f'{i}   dir\n'
    return output
def cmd_pwd(args):
    print_.addstr(str(uos.getcwd()))
    return 0
def cmd_touch(args):
    if not args:
        print_.addstr('usage:touch <file>')
        return 1
    try:
        api.system.append_file(args[0],'')
    except Exception as e:
        print_.addstr(f'[ERROR]touch failed,log:{e}')
        return 1
    return 0
def cmd_mkdir(args):
    if not args:
        print_.addstr('usage:mkdir <name>')
        return 1
    try:
        api.system.mkdir(args[0])
    except Exception as e:
        print_.addstr(f'[ERROR]mkdir failed,log:{e}')
        return 1
    return 0
def cmd_rm(args):
    if not args:
        print_.addstr('usage:rm <file>')
        return 1
    try:
        api.system.remove_file(args[0])
    except Exception as e:
        print_.addstr(f'[ERROR]rm failed,log:{e}')
        return 1
    return 0
def cmd_rmdir(args):
    if not args:
        print_.addstr('usage:rmdir <dir>')
        return 1
    try:
        api.system.rmdir(args[0])
    except Exception as e:
        print_.addstr(f'[ERROR]rmdir failed,log:{e}')
        return 1
    return 0
def cmd_echo(args):
    if not args:
        print_.addstr('usage:echo <data>')
        return 1
    for i in args:
        print_.addstr(f'{i} ',end = '')
    return 0
def cmd_cat(args):
    if not args:
        print_.addstr('usage:cat <file>')
        return 1
    try:
        for i in range(api.system.get_line(args[0])):
            print_.addstr(api.system.read_file(args[0],i+1),end = '')
    except Exception as e:
        print_.addstr(f'cat failed,log:{e}') 
        return 1
    return 0
def cmd_unknown(zhanwei):
    print_.addstr('unknown command')
    return 1
def parse_line(line):
    if line is None:
        return None

    line = line.strip()
    if not line:
        return None

    result = []
    current = []
    buf = ""
    quote = None
    i = 0

    def push_token():
        nonlocal buf, current
        if buf != "":
            current.append(buf)
            buf = ""

    def push_command():
        nonlocal current, result
        if not current:
            return True

        cmd = current[0]
        args = current[1:]
        result.append([cmd, args])
        current = []
        return True

    try:
        while i < len(line):
            c = line[i]

            if quote is not None:
                if c == quote:
                    quote = None
                else:
                    buf += c
                i += 1
                continue

            if c == '"' or c == "'":
                quote = c
                i += 1
                continue

            if c == " " or c == "\t":
                push_token()
                i += 1
                continue

            if c == "|":
                push_token()
                if not push_command():
                    return []
                i += 1
                continue

            if c == ">":
                push_token()
                push_command()

                if i + 1 < len(line) and line[i + 1] == ">":
                    redir = ">>"
                    i += 2
                else:
                    redir = ">"
                    i += 1

                filename = line[i:].strip()
                if not filename:
                    return []

                result.append([redir, [filename]])
                return result

            buf += c
            i += 1

        if quote is not None:
            return []

        push_token()
        push_command()

        if not result:
            return None

        return result

    except Exception:
        return []
def deep_in(seq, target):
    for item in seq:
        if item == target:
            return True

        if isinstance(item, (list, tuple)):
            if deep_contains(item, target):
                return True

    return False
def cmd_exit(args):
    api.system.exit = True
    return 255
def cmd_write(args):
    if len(args) != 2:
        print_.addstr("'>' is a command :)")
        return 1
    try:
        api.system.write_file(args[0],args[1])
    except Exception as e:
        print_.addstr(f'> failed,log:{e}')
    return 0
def cmd_append(args):
    if len(args) != 2:
        print_.addstr("'>>' is a command :)")
        return 1
    try:
        api.system.append_file(args[0],f'{args[1]}\n')
    except Exception as e:
        print_.addstr(f'>> failed,log:{e}')
    return 0
def cmd_sc(args):
    try:
        if len(args) < 1:
            print_.addstr('usage:sc <op(status/disable/unable)> <service>')
            return 1
        if args[0] == 'status':
            print_.addstr(str(api.system.read_sersta()))
        elif args[0] == 'disable':
            api.system.change_ser(args[1],0)
        elif args[0] == 'unable':
            api.system.change_ser(args[1],1)
        elif args[0] == 'log':
            print_.addstr(api.system.read_log())
        else:
            print_.addstr('usage:sc <op(status/disable/unable)> <service>')
            return 1
        return 0
    except Exception as e:
        print_.addstr(f'sc failed,log:{e}')
        return 1
support_command = {
    'cd':cmd_cd,
    'ls':cmd_ls,
    'pwd':cmd_pwd,
    'touch':cmd_touch,
    'mkdir':cmd_mkdir,
    'rm':cmd_rm,
    'rmdir':cmd_rmdir,
    'echo':cmd_echo,
    'cat':cmd_cat,
    'exit':cmd_exit,
    '>':cmd_write,
    '>>':cmd_append,
    'sc':cmd_sc
    }
builtin_ = {}
class command:
    def __init__(self):
        self.typecmd = None
        api.system.api_print('[INFO]command object load successfully')
    def batch(self,nowcm,args):
        return_val = support_command.get(nowcm,cmd_unknown)(args)
        if return_val:
            api.system.api_print(f'failed with {return_val}')
        if return_val == 255:
            return 1
command_ = command()
while 1:
    try:
        not_write = True
        tmp = False
        print_.echo_off()
        command_.typecmd = parse_line(input(f'[{uos.getcwd()}]>'))
        if not command_.typecmd:
            if command_.typecmd is None:
                continue
            else:
                api.system.api_print('[ERROR]SyntaxError')
        print_.reset()
        tmp1 = 1
        if deep_in('>',command_.typecmd) or deep_in('>>',command_.typecmd):
            not_write = False
        for i in command_.typecmd:
            if len(command_.typecmd) == tmp1 and not_write:
                print_.echo_on()
            if print_.nowstr:
                #print(print_.nowstr)
                i[1].append(print_.nowstr)
                print_.reset()
            if command_.batch(i[0],i[1]):
                tmp = True
                break
            tmp1 += 1
            #print(command_.typecmd)
        if tmp:
            break
    except KeyboardInterrupt:
        api.system.api_print('Abort by user')
api.system.api_print('[WARNING]shell exit')
while 1:
    sm.utime.sleep(3)
    print('Press Ctrl+C to exit')

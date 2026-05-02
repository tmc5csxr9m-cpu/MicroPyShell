import uos
import utime
import gc
import extra_
class shell_re:
    def __init__(self):
        self.nowstr = ''
        self.echo = True
    def addstr(self,toaddstr,end = '\n'):
        self.nowstr += toaddstr
        if self.echo:
            print(toaddstr,end = end)
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
    for i in uos.listdir():
        if (uos.stat(i)[0] & 0x8000) != 0:
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
        f = open(args[0],'a')
        f.close()
    except Exception as e:
        print_.addstr(f'[ERROR]touch failed,log:{e}')
        return 1
    return 0
def cmd_mkdir(args):
    if not args:
        print_.addstr('usage:mkdir <name>')
        return 1
    try:
        uos.mkdir(args[0])
    except Exception as e:
        print_.addstr(f'[ERROR]mkdir failed,log:{e}')
        return 1
    return 0
def cmd_rm(args):
    if not args:
        print_.addstr('usage:rm <file>')
        return 1
    try:
        uos.remove(args[0])
    except Exception as e:
        print_.addstr(f'[ERROR]rm failed,log:{e}')
        return 1
    return 0
def cmd_rmdir(args):
    if not args:
        print_.addstr('usage:rmdir <dir>')
        return 1
    try:
        uos.rmdir(args[0])
    except Exception as e:
        print_.addstr(f'[ERROR]rmdir failed,log:{e}')
        return 1
    return 0
def cmd_echo(args):
    if not args:
        print_.addstr('usage:echo <data>')
        return 1
    for i in args:
        print_.addstr(i,end=' ')
    return 0
def cmd_cat(args):
    if not args:
        print_.addstr('usage:cat <file>')
        return 1
    try:
        with open(args[0],'r') as f:
            for line in f:
                print_.addstr(line,end = '')
    except Exception as e:
        print_.addstr('cat failed,log:',e)
        return 1
    return 0
def cmd_unknow(zhanwei):
    print_.addstr('unkown command')
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
    return 255
def cmd_write(args):
    if len(args) != 2:
        print("'>' is a command :)")
        return 1
    try:
        with open(args[0],'w') as f:
            f.write(args[1])
    except Exception as e:
        print('> failed,log:',e)
    return 0
def cmd_append(args):
    if len(args) != 2:
        print("'>>' is a command :)")
        return 1
    try:
        with open(args[0],'a') as f:
            f.write(f'{args[1]}\n')
    except Exception as e:
        print('>> failed,log:',e)
    return 0
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
    '>>':cmd_append
    }
builtin_ = {}
class command:
    def __init__(self):
        self.typecmd = None
        print('[INFO]command object load successfully')
    def batch(self,nowcm,args):
        return_val = support_command.get(nowcm,cmd_unknow)(args)
        if return_val:
            print(f'failed with {return_val}')
        if return_val == 255:
            return 1
command_ = command()
while 1:
    not_write = True
    tmp = False
    print_.echo_off()
    command_.typecmd = parse_line(input(f'[{uos.getcwd()}]>'))
    if not command_.typecmd:
        if command_.typecmd is None:
            continue
        else:
            print('[ERROR]SyntaxError')
    print_.reset()
    tmp1 = 1
    if deep_in('>',command_.typecmd) or deep_in('>>',command_.typecmd):
        not_write = False
    for i in command_.typecmd:
        if len(command_.typecmd) == tmp1 and not_write:
            print_.echo_on()
        if print_.nowstr:
            i[1].append(print_.nowstr)
            print_.reset()
        if command_.batch(i[0],i[1]):
            tmp = True
            break
        tmp1 += 1
        #print(command_.typecmd)
    if tmp:
        break
        

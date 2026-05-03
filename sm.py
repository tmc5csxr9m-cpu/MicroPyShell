import utime
import api
import _thread
import ujson
def startup():
    f = ujson.loads(api.system.read_file('sm.json',1))
    for i in f:
        try:
            exec(f[i])
        except Exception as e:
            api.system.api_print(f'[ERROR]Failed at startup {e}')
def services_manager(ser_list,ser_time):
    timer = 0
    api.system.write_sersta({k: 1 for k in ser_list})
    while 1:
        for i in ser_list:
            try:
                if not (timer % ser_time[i]) and api.system.read_sersta()[i]:
                    exec(ser_list[i])
                    api.system.write_log(f'[INFO]{ser_list[i]} active')
            except Exception as e:
                api.system.write_log(f'[ERROR]Failed at {ser_list[i]},log:{e}')
        if api.system.exit:
            api.system.api_print('[WARNING]Services Manager exit')
            break
        utime.sleep(1)
        timer += 1
startup()
_thread.start_new_thread(services_manager,(ujson.loads(api.system.read_file('sm.json',2)),ujson.loads(api.system.read_file('sm.json',3))))
api.system.api_print('[INFO]Services Manager load successfully')
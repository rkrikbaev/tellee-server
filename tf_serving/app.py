from adapter import Nats_to_TF
import _thread
from interface import *
import argparse
import os, time, datetime
import yaml


def utc_time(timeshift):
    unix_time = time.time()
    unix_with_tz = float(unix_time+3600*timeshift)
    dt = datetime.datetime.utcfromtimestamp(unix_with_tz).strftime('%Y-%m-%d %H:%M:%S')
    return dt


def get_yaml_info(file):
    data =[]
    with open(file, 'r') as fp:
        config_list = yaml.load(fp)
    for item in config_list:
        pipe_enabled = config_list[str(item)]['enabled']
        if pipe_enabled == True:
            dic = config_list[str(item)]
            data.append(dic.copy())
    return data


def worker(config, model_number, delay, dt):
    print("{timestamp}: start job#{model_number}".format(timestamp=dt, model_number=model_number))

    nats_address = config['nats_address']
    tf_address = config['tf_address']
    thing_id = config['thing_id']
    thing_ext_id = config['thing_ext_id']
    thing_key = config['thing_key']
    channel_id = config['channel_id']

    while 1:

        time.sleep(delay)
        cli_nats = Nats_to_TF(nats_address, thing_id, thing_key, channel_id, thing_ext_id, dt)
        cli_nats.tf_worker(tf_address)


def parse_args():
    path = os.getcwd()+''
    parser = argparse.ArgumentParser(description='Main program to run flow-server')
    parser.add_argument('-f', type=str, required=True,
                        default=path,
                        help='path to the configuration file')
    return parser.parse_args()


def main(work_flow_config):

    for model in range(len(work_flow_config)):
        print(len(work_flow_config))

        delay = work_flow_config[model]['delay']
        config = work_flow_config[model]['worker']

        _thread.start_new_thread(worker, (config, model, delay, dt))

        print('{timestamp}: Thread started for model: {model}...'.format(timestamp=dt, model=model))


if __name__ == '__main__':

    dt = utc_time(6)

    print("{timestamp}: Start...".format(timestamp=dt))
    print('{timestamp}: Read configuration file...'.format(timestamp=dt))

    #args = parse_args()
    #main(file=args.f)

    main(get_yaml_info(file='./work_flow.yml'))
    tf.app.run()

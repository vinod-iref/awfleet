import json
from lib import Spot
from db import db
import boto3
from lib import Demand
import configparser
import code

PERCENT = 0.1

def start_spot(ids):
    demand = Demand()
    bid_price = demand.get_price()
    dbase = db.DB('db/fleet.db')

    config = configparser.ConfigParser()
    config.read('.aws/config')
    client = boto3.client('ec2')
    for _id in ids:
        with open(configfile, 'r') as config:
            body = json.load(config)
            body['ClientToken'] = '{}_{:d}'.format(_id[2], int(time.time()))
            body['SpotPrice'] = bid_price

            data = {
                "SpotFleetRequestConfig": body
            }

            res = client.request_spot_fleet(**data)
            with open('config/{}.json'.format(_id[2]), 'w') as newconfig:
                newconfig.write(json.dumps(body, indent=4))
            dbase.instance_up('spotinstance', res['SpotFleetRequestId'], bid_price, _id[2])
            print res

def stop_spot(ids):
    if len(ids) == 0: return
    client = boto3.client('ec2')
    client.cancel_spot_instance_requests(SpotInstanceRequestIds=[_id[0] for _id in ids])
    dbase = db.DB('db/fleet.db')
    for _id in ids:
        dbase.instance_down('spotinstance', _id[0])

def start_on_demand(ids):
    client = boto3.resource('ec2')
    dbase = db.DB('db/fleet.db')
    for _id in ids:
        with open('config/{}.json'.format(_id[2]), 'r') as config:
            body = json.load(config)
            instance = client.create_instances(
                        ImageId=body['LaunchSpecifications'][0]['ImageId'],
                        MinCount=1,
                        MaxCount=1,
                        InstanceType=body['LaunchSpecifications'][0]['InstanceType'],
                        SecurityGroupIds=body['LaunchSpecifications'][0]['NetworkInterfaces'][0]['Groups'])

            demand = Demand()
            price = demand.get_price()
            dbase.instance_up('ondemand', instance[0]._id, price, _id[2])

def stop_on_demand(ids):
    if len(ids) == 0: return
    client = boto3.resource('ec2')
    client.stop_instances(InstanceIds=[_id[0] for _id in ids])
    dbase = db.DB('db/fleet.db')
    for _id in ids:
        dbase.instance_down('ondemand', _id[0])

def monitor():
    spot = Spot()
    prices = spot.get_price()
    linux_price = [d for d in prices if d['name']=='linux'][0]
    spot_price = float(linux_price['prices']['USD'])

    dbase = db.DB('db/fleet.db')
    spots = dbase.get_instances('spotinstance')
    ids = [value for value in spots if spot_price >= PERCENT*value[1]]
    print "Starting on-demands and stoping spots for these:"
    print ids
    start_on_demand(ids)
    stop_spot(ids)

    demands = dbase.get_instances('ondemand')
    ids = [value for value in demands if spot_price < PERCENT*value[1]]
    print "Starting spots and stoping on-demands for these:"
    print ids
    start_spot(ids)
    stop_on_demand(ids)

if __name__ == '__main__':
    monitor()
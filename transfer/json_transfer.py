import logging

from shadowsocks import common

from transfer.db_transfer import TransferBase
from utils.configloader import load_config, get_config


class MuJsonTransfer(TransferBase):
    def __init__(self):
        super(MuJsonTransfer, self).__init__()

    def update_all_user(self, dt_transfer):
        import json
        rows = None

        config_path = get_config().MUDB_FILE
        with open(config_path, 'rb+') as f:
            rows = json.loads(f.read().decode('utf8'))
            for row in rows:
                if "port" in row:
                    port = row["port"]
                    if port in dt_transfer:
                        row["u"] += dt_transfer[port][0]
                        row["d"] += dt_transfer[port][1]

        if rows:
            output = json.dumps(rows, sort_keys=True,
                                indent=4, separators=(',', ': '))
            with open(config_path, 'r+') as f:
                f.write(output)
                f.truncate()

        return dt_transfer

    def pull_db_all_user(self):
        import json
        rows = None

        config_path = get_config().MUDB_FILE
        with open(config_path, 'rb+') as f:
            rows = json.loads(f.read().decode('utf8'))
            for row in rows:
                try:
                    if 'forbidden_ip' in row:
                        row['forbidden_ip'] = common.IPNetwork(
                            row['forbidden_ip'])
                except Exception as e:
                    logging.error(e)
                try:
                    if 'forbidden_port' in row:
                        row['forbidden_port'] = common.PortRange(
                            row['forbidden_port'])
                except Exception as e:
                    logging.error(e)

        if not rows:
            logging.warn('no user in json file')
        return rows

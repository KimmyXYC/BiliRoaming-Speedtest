import paramiko
from loguru import logger
from utils.Parameter import get_parameter


def upload():
    logger.info('开始上传')
    try:
        sftp_config = get_parameter('sftp')
        tran = paramiko.Transport((sftp_config['host'], sftp_config['port']))
        tran.connect(username=sftp_config['user'], password=sftp_config['passwd'])
        sftp = paramiko.SFTPClient.from_transport(tran)
        sftp.put(sftp_config['local_path'], sftp_config['remote_path'])
        tran.close()
        logger.success('上传成功')
    except Exception as e:
        logger.error(f'上传失败: {e}')

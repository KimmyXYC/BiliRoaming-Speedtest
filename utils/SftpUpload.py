from utils.Parameter import get_parameter
import paramiko


def upload():
    if get_parameter('upload'):
        print('开始上传')
        try:
            SftpConfig = get_parameter('sftp')
            tran = paramiko.Transport((SftpConfig['host'], SftpConfig['port']))
            tran.connect(username=SftpConfig['user'], password=SftpConfig['passwd'])
            sftp = paramiko.SFTPClient.from_transport(tran)
            sftp.put(SftpConfig['localpath'], SftpConfig['remotepath'])
            tran.close()
            print('上传成功')
        except Exception as e:
            print(f'上传失败: {e}')

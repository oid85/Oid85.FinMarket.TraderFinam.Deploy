import time
import os
import shutil
import config
import json


def deploy():
    # остановка и удаление службы
    cmd = f'sc stop {config.trade_finam_service_name}'
    print(cmd)
    res = os.system(cmd)
    print(res)

    cmd = f'sc delete {config.trade_finam_service_name}'
    print(cmd)
    res = os.system(cmd)
    print(res)

    # формируем директории
    if not os.path.exists(config.deploy_path):
        os.makedirs(config.deploy_path)

    if not os.path.exists(os.path.join(config.deploy_path, config.trade_finam_deploy_directory)):
        os.makedirs(os.path.join(config.deploy_path, config.trade_finam_deploy_directory))

    current_time = time.time()
    current_deploy_version = f"{current_time}"

    dest_path = os.path.join(config.deploy_path, config.trade_finam_deploy_directory, current_deploy_version)

    if not os.path.exists(dest_path):
        os.makedirs(dest_path)

    # build
    cmd = f'cd {config.trade_finam_source_path} && dotnet build --configuration Release --output {dest_path}'
    print(cmd)
    res = os.system(cmd)
    print(res)

    # редактируем appsettings.json
    appsettings_file_path = os.path.join(dest_path, config.trade_finam_appsettings_file)
    with open(appsettings_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    data['DeployPort'] = config.trade_finam_deploy_port

    data['Hangfire']['CheckOutbox']['Enable'] = False

    with open(appsettings_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    # установка и запуск службы
    exe_file_path = os.path.join(dest_path, config.trade_finam_exe_file_name)
    cmd = f'sc create {config.trade_finam_service_name} binPath={exe_file_path}'
    print(cmd)
    res = os.system(cmd)
    print(res)

    cmd = f'sc config {config.trade_finam_service_name} start=auto'
    print(cmd)
    res = os.system(cmd)

    cmd = f'sc start {config.trade_finam_service_name}'
    print(cmd)
    res = os.system(cmd)
    print(res)

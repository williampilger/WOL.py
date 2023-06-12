try:
    import socket
    import struct
    import os
    import sys
    import multiplat as mp
    import backend as be
except:
    print("Biblioteca necessária não disponível.\n\nEstamos finalizando.")
    quit()


def WakeupOnLan(broadcast_ip, host_mac):
    mac_adrs = host_mac.replace(host_mac[2], '')#remover separadores
    data = ''.join(['FFFFFFFFFFFF', mac_adrs * 20])
    send_data = b''
    for j in range(0, len(data), 2):
        send_data = b''.join([
            send_data,
            struct.pack('B', int(data[j: j + 2], 16))
        ])
    # Broadcast it to the LAN.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(send_data, (broadcast_ip, 7))
    print(f'Magic Packet enviado para {host_mac} ({broadcast_ip})')
    return True

# Função para ler dados de arquivo
# PARAMS: filename(String) -> Nome do arquivo que possui as configurações
# RETURN: data(dictionary) -> Ex. {'hostName' : ['192.168.2.255','a4:5e:81:f8:a9:9a']}
def ler_config(fileName):
    if not os.path.exists(fileName):
        os.system("echo https://sample.youdomine.com/path/to/service.php\t30 > wol_config.ini")
        return False
    data = {}
    with open(fileName, "r") as arquivo:
        for linha in arquivo:
            linha = linha.replace('\n', '')#tirar fim de linha
            host = linha.split('\t')
            if(len(host) == 1):
                data = host[0]
                break
    return data

def print_list(config):
    print('\n\n Hosts configurados:')
    for host in config:
        print(f"     {host} -> [ {config[host][0]} | {config[host][1]} ]")

def print_help():
    print(" Desenvolvido por William Pilger | AuthentyAE | Bom Princípio - RS - Brasil")
    print("      wol.py [ARG]")
    print("           ARG:")
    print("              -all - Envia o Magic Packet para todos os Hosts configurados.")
    print("              -list - Lista todos os Hosts configurados.")
    print("              -help - Envia o Magic Packet para todos os Hosts configurados.")
    print("              seuHost - Envia o Magic Packet para o host informado, se ele existir")
    print("\n      wol_config.ini")
    print("              Este arquivo DEVE conter a configuração dos hosts, e deve estar neste diretório.")
    print("              A correta disposição dos dados é:")
    print("                     hostname    broadcast_ip    mac_adrs")
    print("                     exemplo     192.168.2.255   a4:5e:81:f8:a9:9a")
    print("              A separação dos dados é feita por TAB.")
    print("              Caso o arquivo não exista, um exemplo será criado ao executar o WOL.")

def main(arg):
    config = ler_config('wol_config.ini')
    if(config):
        wol = False#seta se precisa ser feito o wake-on-lan

        if( not arg ):
            print_list(config)
            arg = input('\nInforme o host que deseja iniciar: ')
        
        if (arg == '-all'):
            for host in config:
                WakeupOnLan(config[host][0],config[host][1])
        elif(arg == '-list'):
            print_list(config)
        elif(arg == '-help'):
            print_help()
        else:
            if(arg in config):
                WakeupOnLan(config[arg][0], config[arg][1])
                input("\nPressione ENTER para sair")
            else:
                print("Host não existe.")
                print("use 'wol.py -help' para obter ajuda.")
    else:
        be.sair(2)
    
if __name__ == '__main__':
    prompt = ("-p" in sys.argv) #Obtém parametros informados
    if(len(sys.argv) == 1):#Nenhum argumento foi informado
        arg = False
    else:
        arg = sys.argv[-1]
    main(arg)

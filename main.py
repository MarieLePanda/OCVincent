# Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)

import paramiko
import time
import logging


def send(shell, command):
    """
    Function to send specific commands
    """

    shell.send("\n")
    shell.send(str(command) + "\n")

    time.sleep(.5)

    output = shell.recv(65000)
    print(output.decode('ascii'))


def main():
    """
    Main function that initializes the ssh connection by asking for the targeted ip address,
    user and password
    """

    logging.info('Connexion SSH')

    router_ip = input("Entrez l'adresse IP cible : ")
    router_username = input("Entrez le username : ")
    router_password = input("Entrez le mot de passe : ")

    try:
        ssh_pre = paramiko.SSHClient()
        ssh_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh_pre.load_system_host_keys()

        try:

            # Connect to router using username/password authentication.
            ssh_pre.connect(router_ip,
                            username=router_username,
                            password=router_password,
                            look_for_keys=False)
            print("Connexion réussie")
            shell = ssh_pre.invoke_shell()
            output = shell.recv(65000)
            print(output.decode('ascii'))

            send(shell, "enable")
            send(shell, "vdcvdc\n")

        except paramiko.AuthenticationException:
            print("Mot de passe incorrect : ")
            logging.error("Mauvais identifiant !")
    except:
        print("Quelque chose ne vas pas")
        logging.error("Problème de connexion")
    mainMenu(shell)


def mainMenu(shell):
    """
    Main menu to access several sub-menus
    """

    logging.info('Menu principal')

    menu_choice = -1
    while 0 > menu_choice or 4 < menu_choice:
        try:
            print("\n MENU PRINCIPAL\n")
            print("--------------------\n")

            print("Choisissez parmi les propositions suivantes : ")
            print(
                """\n\n\n
                1 - APERCU CONFIGURATION
                -----------------------------
                2 - CONFIGURATION MATERIEL
                -----------------------------
                3 - TEST DE CONNEXION
                -----------------------------
                4 - SAUVEGARDER / CHARGER
                -----------------------------
                0 - Quitter               
                -----------------------------
                \n\n\n"""
            )
            menu_choice = int(input())
        except ValueError:
            print("Choisissez un chiffre entre 1 et 3")

    if menu_choice == 1:
        showConf(shell)
    elif menu_choice == 2:
        confMain(shell)
    elif menu_choice == 3:
        connTest(shell)
    elif menu_choice == 4:
        saveLoad(shell)
    elif menu_choice == 0:
        exit(shell)


def showConf(shell):
    """
    Multiple choice configuration overview menu
    """

    logging.info('Menu aperçu de configuration')


    menu_choice = -1
    while 0 > menu_choice < 4:
        try:
            print("\n MENU APERCU CONFIGURATION\n")
            print("------------------------------\n")

            print("Choisissez parmi les propositions suivantes : ")
            print(
                """\n\n\n
                1 - SHOW RUNNING CONFIGURATION
                -----------------------------
                2 - SHOW IP INTERFACE BRIEF
                -----------------------------
                3 - SHOW ACCESS LIST
                -----------------------------
                4 - SHOW IP ROUTE                
                -----------------------------
                0 - Quitter               
                -----------------------------
                \n\n\n"""
            )
            menu_choice = int(input())
        except ValueError:
            print("Choisissez un chiffre entre 1 et 4")

        if menu_choice == 1:
            time.sleep(2)
            send(shell, "sh run")
            time.sleep(2)
        elif menu_choice == 2:
            send(shell, "sh ip int brief")
        elif menu_choice == 3:
            send(shell, "sh ip access-list")
        elif menu_choice == 4:
            send(shell, "show ip route")
        elif menu_choice == 0:
            mainMenu(shell)
        showConf(shell)


def confMain(shell):
    """
    Multiple choice setup menu
    """

    logging.info('Menu de configuration')

    menu_choice = -1
    while 0 > menu_choice or 3 < menu_choice:
        try:
            print("\n MENU DE CONFIGURATION\n")
            print("--------------------\n")

            print("Choisissez parmi les propositions suivantes : ")
            print(
                """\n\n\n
                1 - CONFIGURER INTERFACE
                -----------------------------
                2 - CONFIGURER ROUTE
                -----------------------------
                3 - CONFIGURER HOSTNAME
                -----------------------------
                0 - Quitter               
                -----------------------------
                \n\n\n"""
            )
            menu_choice = int(input())
        except ValueError:
            print("Choisissez un chiffre entre 1 et 3")

    if menu_choice == 1:
        intConf(shell)
    elif menu_choice == 2:
        routeConf(shell)
    elif menu_choice == 3:
        setHostname(shell)
    elif menu_choice == 0:
        mainMenu(shell)


def intConf(shell):
    """
    Configuration menu for the various interfaces
    """

    logging.info('Menu de configuration des interfaces')

    print("\n CONFIUGRATION DES INTERFACES\n")
    print("------------------------------------\n")

    send(shell, 'sh ip int brief')
    interface = input("Choisissez une interface à configurer [q pour quitter] : \n")
    if interface == 'q':
        confMain(shell)
    else:
        ip_address = input("Addresse IP ? : ")
        mask = input("Masque de sous-réseau : ")
        send(shell, 'conf terminal')
        send(shell, 'int ' + interface)
        send(shell, 'ip add ' + ip_address + " " + mask)
        send(shell, 'no shut')
        send(shell, 'end')

    intConf(shell)


def routeConf(shell):
    """
    Route configuration menu
    """

    logging.info('Menu de configuration des routes')

    print("\n CONFIUGRATION DES ROUTES\n")
    print("------------------------------------\n")

    send(shell, 'sh ip route')
    route = input("Adresse à atteindre [q pour quitter] :  ")
    if route == "q":
        confMain(shell)
    else:
        wildcard = input("Masque inversé : ")
        next = input("Interface ou adresse de prochain saut : ")
        send(shell, "conf t")
        send(shell, "ip route " + route + " " + wildcard + " " + next)
        send(shell, 'end')
    routeConf(shell)


def setHostname(shell):
    """
    Hostname configuration menu
    """

    logging.info('Menu de configuration du hostname')

    print("\n CONFIUGRATION HOSTNAME \n")
    print("-----------------------------\n")

    hostname = input("Entrez un Hostname : ")
    send(shell, 'conf t')
    send(shell, 'hostname ' + hostname)
    send(shell, 'end')
    confMain(shell)


def connTest(shell):
    """
    Menu for testing connectivity
    """

    logging.info('Menu test de connectivité')

    menu_choice = -1
    while 0 > menu_choice or 2 < menu_choice:
        try:
            print("\n MENU TEST DE CONNEXION\n")
            print("--------------------\n")

            print("Choisissez parmi les propositions suivantes : ")
            print(
                """\n\n\n
                1 - TRACEROUTE
                -----------------------------
                2 - PING
                -----------------------------
                0 - Quitter               
                -----------------------------
                \n\n\n"""
            )

            menu_choice = int(input())

        except ValueError:
            print("Choisissez un chiffre entre 1 et 2")

    if menu_choice == 1:
        traceTest(shell)
    elif menu_choice == 2:
        pingTest(shell)
    elif menu_choice == 0:
        mainMenu(shell)


def traceTest(shell):
    """
    Menu allowing to follow the paths that a data packet
    """

    logging.info('Menu traceroute')


    print("\nTRACEROUTE\n")
    print("--------------")

    trace = input("Entrez une addresse que vous souhaitez tracer : ")
    send(shell, "traceroute " + trace)

    connTest(shell)


def pingTest(shell):
    """
    Menu used to test the accessibility of another machine
    """

    logging.info('Menu test de ping')


    print("\nTEST DE PING\n")
    print("----------------------")

    ping = input("Entrez une adresse que vous souhaitez pinguer : [q pour quitter")
    if ping == 'q':
        connTest(shell)
    else:
        send(shell, "ping " + ping)

        connTest(shell)


def saveLoad(shell):
    """
    Menu used to save or load a configuration
    """

    logging.info('Menu sauvegarde / charger configuration')

    print("\nSAUVEGARDER / CHARGER\n")
    print("----------------------")

    menu_choice = -1

    while 0 > menu_choice or 4 < menu_choice:
        try:

            print("Choisissez parmi les propositions suivantes : ")
            print(
                """\n\n\n
                1 - SAUVEGARDER DANS STARTUP CONFIG
                -----------------------------------
                2 - SAUVEGARDER SUR TFTP
                -----------------------------------
                3 - CHARGER SUR STARTUP CONFIG
                -----------------------------------
                4 - CHARGER DEPUIS TFTP
                -----------------------------------
                0 - Quitter               
                -----------------------------------
                \n\n\n"""
            )

            menu_choice = int(input())

        except ValueError:
            print("Choisissez un chiffre entre 1 et 4")

    if menu_choice == 1:
        send(shell, "wr")
        time.sleep(2)
        saveLoad(shell)
    elif menu_choice == 2:
        tftp = input("Entrez l'adresse de votre serveur TFTP :")
        # file_name = input("Entrez un nom pour votre sauvegarde :")
        send(shell, "copy running-config tftp" + tftp)
        time.sleep(2)
        saveLoad(shell)
    elif menu_choice == 3:
        send(shell, "copy start run")
    elif menu_choice == 4:
        file = input("Entre le chemin tftp du fichier specifié :")
        send(shell, "copy running-config tftp:" + file)
    elif menu_choice == 0:
        mainMenu(shell)


if __name__ == '__main__':
    main()
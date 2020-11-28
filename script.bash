DEFAULT="\033[0m"
GREEN="\033[32m"
RED="\033[31m"

USER=""
WORKING_DIR=""
LIB_DIR=""
SERVICE=nubeio-bacnet-server.service
SERVICE_DIR=/lib/systemd/system
SERVICE_DIR_SOFT_LINK=/etc/systemd/system/multi-user.target.wants
DATA_DIR=/data/bacnet-flask
CONFIG_EXAMPLE=settings/config.example.ini
CONFIG=config.ini
COMMAND=""

help() {
    echo "Service commands:"
    echo -e "   ${GREEN}start -u=<user> -dir=<working_dir> -lib_dir=<lib_dir>${DEFAULT}   Start the service (-u=pi -dir=/home/pi/backend-${version}-${sha})"
    echo -e "   ${GREEN}disable${DEFAULT}                                                 Disable the service"
    echo -e "   ${GREEN}enable${DEFAULT}                                                  Enable the stopped service"
    echo -e "   ${GREEN}delete${DEFAULT}                                                  Delete the service"
    echo -e "   ${GREEN}restart${DEFAULT}                                                 Restart the service"
    echo
    echo "Service parameters:"
    echo -e "   ${GREEN}-h --help${DEFAULT}                                               Show this help"
    echo -e "   ${GREEN}-u --user=<user>${DEFAULT}                                        Which <user> is starting the service"
    echo -e "   ${GREEN}-dir --working-dir=<working_dir>${DEFAULT}                        From where wires is starting"
    echo -e "   ${GREEN}-dir --lib_dir-dir=<lib_dir>${DEFAULT}                            From where lib should load"
}

start() {
    if [[ ${USER} != "" && ${WORKING_DIR} != "" && ${LIB_DIR} != "" ]]
    then
        echo -e "${GREEN}Creating Linux Service${DEFAULT}"
        sudo cp systemd/${SERVICE} ${SERVICE_DIR}/${SERVICE}
        sed -i -e 's/<user>/'"${USER}"'/' ${SERVICE_DIR}/${SERVICE}
        sed -i -e 's,<working_dir>,'"${WORKING_DIR}"',' ${SERVICE_DIR}/${SERVICE}
        sed -i -e 's,<lib_dir>,'"${LIB_DIR}"',' ${SERVICE_DIR}/${SERVICE}

        # Create data_dir and config.ini if not exist
        mkdir -p ${DATA_DIR}
        if [ ! -s ${DATA_DIR}/${CONFIG} ] ; then
            echo "config.ini file doesn't exist (or it is empty)"
            cp ${WORKING_DIR}/${CONFIG_EXAMPLE} ${DATA_DIR}/${CONFIG}
            sudo chmod -R +755 ${DATA_DIR}/${CONFIG}
        fi
        sudo chown -R ${USER}:${USER} ${DATA_DIR}

        echo -e "${GREEN}Soft Un-linking Linux Service${DEFAULT}"
        sudo unlink ${SERVICE_DIR_SOFT_LINK}/${SERVICE}

        echo -e "${GREEN}Soft Linking Linux Service${DEFAULT}"
        sudo ln -s ${SERVICE_DIR}/${SERVICE} ${SERVICE_DIR_SOFT_LINK}/${SERVICE}

        echo -e "${GREEN}Enabling Linux Service${DEFAULT}"
        sudo systemctl daemon-reload
        sudo systemctl enable ${SERVICE}

        echo -e "${GREEN}Starting Linux Service${DEFAULT}"
        sudo systemctl restart ${SERVICE}

        echo -e "${GREEN}Service is created and started, please reboot to confirm...${DEFAULT}"
    else
        echo -e ${RED}"-u=<user> -dir=<working_dir> -lib_dir=<lib_dir> these parameters should be on you input (-h, --help for help)${DEFAULT}"
    fi
}

disable() {
    echo -e "${GREEN}Stopping Linux Service${DEFAULT}"
    sudo systemctl stop ${SERVICE}
    echo -e "${GREEN}Disabling Linux Service${DEFAULT}"
    sudo systemctl disable ${SERVICE}
    echo -e "${GREEN}Service is disabled...${DEFAULT}"
}

enable() {
    echo -e "${GREEN}Enabling Linux Service${DEFAULT}"
    sudo systemctl enable ${SERVICE}
    echo -e "${GREEN}Starting Linux Service${DEFAULT}"
    sudo systemctl start ${SERVICE}
    echo -e "${GREEN}Service is enabled...${DEFAULT}"
}

delete() {
    echo -e "${GREEN}Stopping Linux Service${DEFAULT}"
    sudo systemctl stop ${SERVICE}
    echo -e "${GREEN}Un-linking Linux Service${DEFAULT}"
    sudo unlink ${SERVICE_DIR_SOFT_LINK}/${SERVICE}
    echo -e "${GREEN}Removing Linux Service${DEFAULT}"
    sudo rm -r ${SERVICE_DIR}/${SERVICE}
    echo -e "${GREEN}Service is deleted...${DEFAULT}"
}

restart() {
    echo -e "${GREEN}Restarting Linux Service${DEFAULT}"
    sudo systemctl restart ${SERVICE}
    echo -e "${GREEN}Service is restarted...${DEFAULT}"
}

parseCommand() {
    for i in "$@"
    do
    case ${i} in
    -h|--help)
        help
        exit 0
        ;;
    -u=*|--user=*)
        USER="${i#*=}"
        ;;
    -dir=*|--working-dir=*)
        WORKING_DIR="${i#*=}"
        ;;
    -lib_dir=*)
        LIB_DIR="${i#*=}"
        ;;
    start|disable|enable|delete|restart)
        COMMAND=${i}
        ;;
    *)
        echo -e "${RED}Unknown option (-h, --help for help)${DEFAULT}"
        exit 1
        ;;
    esac
    done
}


runCommand() {
    case ${COMMAND} in
    start)
        start
        ;;
    disable)
        disable
        ;;
    enable)
        enable
        ;;
    delete)
        delete
        ;;
    restart)
        restart
        ;;
    esac
}

parseCommand "$@"
runCommand
exit 0
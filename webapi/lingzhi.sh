#/bin/bash
PID=''
URL='http://192.168.0.137:9080'
TOKEN='7f7a648f-fbd1-406e-8b80-612dbdea1cff'

banner(){
    echo "
		LingZhi IAST

"
}

mkpath(){
    rm -rf ~/.iast
    mkdir ~/.iast
}

# download lingzhi agent.jar
download(){
    curl -X GET $1/iast/download/agent -H "X-IAST-TOKEN:$2" -o ~/.iast/agent.jar -k
}

# init
init(){
    java -jar ~/.iast/agent.jar -k $2 -m properties -p $1
}

# repleace host
replece(){
    sed -i -e "s#iast\.server\.url=https:\/\/www\.huoxian\.cn#iast\.server\.url=$1#g" ~/.iast/config/iast.properties
    sed -i -e "s/iast\.server\.token=.*?/iast\.server\.token=$2/g" ~/.iast/config/iast.properties
}

# attach agent.jar to pid
run(){
    java -jar ~/.iast/agent.jar -k $2 -m install -p $1
}

choice_pid(){
    ajps=($(jps -l|grep -v Jps|grep "[a-zA-Z]$"))
    len=${#ajps[@]}

    if [ 0 -ne $len ]; then
        
        echo "请在30秒内选择需要attach的Java进程:
  编号，进程ID, 目标进程"
        for ((i=0; i<${len};i+=2));
        do
            let j=$i/2
            echo "  "$j"    "${ajps[i]}"    "${ajps[i+1]}
        done

        read -t 30 index
        if [ ! -n "$index" ]; then
            echo "attach的进程不存在，即将退出"
            exit
        else
            let index=$index*2
            PID=${ajps[index]}
            echo "attach进程："$PID
        fi
    else
        echo '未发现任何Java进程，终止安装进程'
        exit
    fi
}

while getopts "u:" arg #选项后面的冒号表示该选项需要参数
do
    case $arg in
        u)
			URL=$OPTARG
            ;;
        ?)  #当有不认识的选项的时候arg为?
            echo "unkonw argument"
            exit 1
        ;;
    esac
done

if [ ! $URL ]; then
	echo "Usage: lingzhi.sh -u <url>
	-u <url>, iast server url, eg: http://127.0.0.1:8000"
else
    # 检查并选择需要attach的进程
    banner
    choice_pid
    # 检查pid是否存在
    mkpath
    download $URL $TOKEN
    init $PID $TOKEN
    replece $URL $TOKEN
    run $PID $TOKEN
fi

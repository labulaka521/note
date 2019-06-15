export LANG=en_US.UTF-8
pidfile=/tmp/autopush.pid
cd /Users/wanglitao/Dropbox/note
case $1 in 
    start)
    if [[ -f $pidfile ]];then
      pid=`cat $pidfile`
      echo "authpush.sh is running $pid"
      exit 0
    fi
    echo $$ > $pidfile
    while true
      do
        git status|grep 'nothing to commit' >/dev/null 2>&1
        if [[ $? -eq 0 ]];then
            continue
        fi
        git add --all
        git commit -m 'update notes'
        git push -u origin master
        sleep 60
      done
    ;;
    stop)
      if [[ ! -f $pidfile ]];then
         echo "authpush.sh is not running"
         exit 0
      fi
      kill -9 `cat $pidfile`
      rm -rf $pidfile
    ;;
    status)
      if [[ -f $pidfile ]];then
        pid=`cat $pidfile`
        echo "authpush.sh is running " $pid
        exit 0
      else
        echo "authpush.sh is not running"
        exit 0
      fi
      ;;
    *)
    echo 'USAGE:bash autopush.sh [start,stop,status]'
    ;;
esac


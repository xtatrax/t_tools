# いらんの消すやつ
cd `dirname $0`
#xattr -dr com.apple.quarantine ./
find ./ -name "._*"\
 -or -name "~\$*"\
 -or -name "desktop.ini"\
 -or -name ".DS_Store"\
 -not -path "*/portable_bin/*"\
 | sed -e 's/ /\\ /g'\
 | tee log._.txt\
 | xargs -t rm
#find ./ -name "~\$*" -not -path "*/portable_bin/*" | sed -e 's/ /\\ /g' | tee log_d.txt | xargs -t rm

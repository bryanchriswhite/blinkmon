set -e

dir=$(dirname "$(realpath $0)")
files=$(ls $dir/systemd)
unit_dir=$HOME/.config/systemd/user
blinkmon_dest=/usr/local/bin/blinkmon

if [[ ! -d ./venv ]]; then
  venv ./venv
fi
. ./venv/bin/activate
pip install -r ./requirements.txt

if [[ ! -d $unit_dir ]]; then
  mkdir -p $unit_dir
fi

for f in $files; do
  dest=$unit_dir/$f
  if [[ ! -e $dest ]]; then
    ln -s $(pwd)/systemd/$f $dest
  fi
done

if [[ ! -e $blinkmon_dest ]]; then
  sudo ln -s $dir/blinkmon.sh $blinkmon_dest
fi

chmod +x $blinkmon_dest

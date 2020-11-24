set -e

dir=$(dirname "$(realpath $0)")
files=$(ls $dir/systemd)
unit_dir=$HOME/.config/systemd/user
blinkmon_dest=/usr/local/bin/blinkmon
udev_rules=/etc/udev/rules.d/51-blink1.rules

#TODO: ensure asdf python?
#TODO: use pipenv instead
if [[ ! -d ./venv ]]; then
  venv ./venv
fi
. ./venv/bin/activate
pip install -r ./requirements.txt

if [[ ! -f $udev_rules ]]; then
  echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="27b8", ATTRS{idProduct}=="01ed", MODE:="666", GROUP="plugdev"' | $udev_rules
  udevadm control --reload
  udevadm trigger
fi

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

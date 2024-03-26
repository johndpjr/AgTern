# Exit if any of the commands below fail
set -e

if [ -z "$1" ] || ! [[ $1 =~ ^[0-9]*\.?[0-9]+$ ]]; then
  echo "Please specify the desired size of the swapfile in GB!"
  exit 1
fi

swapfile_size_bytes=$(wc -c < /swapfile)
desired_size_bytes=$(printf "%.0f" $(($1 * 1024 * 1024 * 1024)))

if [ "$swapfile_size_bytes" -ne "$desired_size_bytes" ]; then
  # Turn off all swapfiles
  swapoff -a
  # Allocate a new swapfile
  fallocate -l "$desired_size_bytes" /swapfile
  # Set the proper permissions
  chmod 600 /swapfile
  # Declare the file as swap space
  mkswap /swapfile
  # Enable the swapfile
  swapon /swapfile
  # Enable the swapfile when the Node restarts
  if ! grep -q "^/swapfile none swap sw 0 0$" /etc/fstab; then
    echo "/swapfile none swap sw 0 0" | tee -a /etc/fstab
  fi
fi
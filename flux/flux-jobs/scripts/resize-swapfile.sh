# Run the script on the host Node:
export SWAPFILE_SIZE_GB=$1
chroot /host /bin/bash <<"EOF"

if [ -z "$SWAPFILE_SIZE_GB" ] || ! [[ $1 =~ ^[0-9]*\.?[0-9]+$ ]]; then
  echo "Please specify the desired size of the swapfile in GB!"
  exit 1
fi

swapfile_size_bytes=$( [ -f /swapfile ] && wc -c < /swapfile || echo 0 )
desired_size_bytes=$( printf "%.0f" $(($SWAPFILE_SIZE_GB * 1024 * 1024 * 1024)) )

if [ "$swapfile_size_bytes" -ne "$desired_size_bytes" ]; then
  # Turn off all swapfiles
  swapoff -a || { echo "Failed to disable current swapfile!"; exit 1; }
  # Allocate a new swapfile
  fallocate -l "$desired_size_bytes" /swapfile || { echo "Failed to allocate new swapfile!"; exit 1; }
  # Set the proper permissions
  chmod 600 /swapfile || { echo "Failed to set swapfile permissions!"; exit 1; }
  # Declare the file as swap space
  mkswap /swapfile || { echo "Failed to define swap space!"; exit 1; }
  # Enable the swapfile
  swapon /swapfile || { echo "Failed to enable swapfile!"; exit 1; }
  # Enable the swapfile when the Node restarts
  if ! grep -q "^/swapfile swap swap defaults 0 0$" /etc/fstab; then
    echo "/swapfile swap swap defaults 0 0" | tee -a /etc/fstab
  fi
fi

EOF
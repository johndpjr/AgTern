# Run the script on the host Node:
export SWAPFILE_SIZE_GB=$1
chroot /host /bin/bash <<"EOF"

if [ -z "$SWAPFILE_SIZE_GB" ] || ! [[ $SWAPFILE_SIZE_GB =~ ^[0-9]*\.?[0-9]+$ ]]; then
  echo "Please specify the desired size of the swapfile in GB!"
  exit 1
fi

swapfile_size_bytes=$( [ -f /swapfile ] && wc -c < /swapfile || echo 0 )
desired_size_bytes=$( printf "%.0f" $(( $SWAPFILE_SIZE_GB * 1024 * 1024 * 1024 )) )
difference_bytes=$( printf "%.0f" $( echo $swapfile_size_bytes $desired_size_bytes | awk '{ print ( $1 > $2 ) ? $1-$2 : $2-$1 }' ) )

if [ "$difference_bytes" -le 1024 ]; then
  echo "Swapfile size: $SWAPFILE_SIZE_GB GB (unmodified)"
else
  echo "Resizing swapfile from $swapfile_size_bytes bytes to $desired_size_bytes bytes."
  # Turn off all swapfiles
  swapoff -a || { echo "Failed to disable current swapfile(s)!"; exit 1; }
  # Delete the swapfile if it exists
  [ -f /swapfile ] && ( rm /swapfile || { echo "Failed to delete current swapfile!"; exit 1; } )
  # Allocate a new swapfile
  fallocate -l "$desired_size_bytes" /swapfile || { echo "Failed to allocate new swapfile!"; exit 1; }
  # Set the proper permissions
  chmod 600 /swapfile || { echo "Failed to set swapfile permissions!"; exit 1; }
  # Declare the file as swap space
  mkswap /swapfile || { echo "Failed to define swap space!"; exit 1; }
  # Enable the swapfile
  swapon /swapfile || { echo "Failed to enable swapfile!"; exit 1; }
  # Enable the swapfile when the Node restarts
  if ! grep -q "^/swapfile" /etc/fstab; then
    echo "/swapfile swap swap defaults 0 0" | tee -a /etc/fstab
  fi
  # Modify the Kubernetes command-line arguments to allow using swap
  awk '{
    if(/^ExecStart=/) {
      line = $0;
      gsub(/\r/, "", line);
      while(line ~ /\\[[:space:]]*$/) {
        if(line ~ /--fail-swap-on=false/) {
          found = 1;
        }
        if(line !~ /--fail-swap-on=true/) {
          print line;
        }
        getline line;
        gsub(/\r/, "", line);
      }
      if(!found) {
        if(line !~ /^[[:space:]]*$/)
          print line " \\";
        print "  --fail-swap-on=false";
        if(line ~ /^[[:space:]]*$/)
          print "";
      } else {
        print line;
      }
    } else {
      print $0;
    }
  }' /etc/systemd/system/kubelet.service > /etc/systemd/system/kubelet.service.new || { echo "Failed to modify kubelet service! Swapfile may not be used."; exit 1; }
  mv /etc/systemd/system/kubelet.service.new /etc/systemd/system/kubelet.service || { echo "Failed to write to kubelet service file! Swapfile may not be used."; rm /etc/systemd/system/kubelet.service.new; exit 1; }
  echo "Swapfile modified! Scheduling restart in 1 minute..."
  # Restart the Node in 1 minute
  shutdown -r +1 || { echo "Failed to restart the Node!"; exit 1; }
fi

EOF
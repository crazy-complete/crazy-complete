function _alsamixer_list_devices
  set -l card

  for card in (aplay -l | string match -r '^card [0-9]+: [^,]+')
    set card (string replace 'card ' '' $card)
    set -l split (string split ': ' $card)

    if set -q split[2]
      printf "%s\t%s\n" $split[1] $split[2]
    end
  end
end

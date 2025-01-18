_alsamixer_list_devices() {
  local card
  aplay -l | grep -Eo '^card [0-9]+: [^,]+' | uniq | while read card; do
    card="${card#card }"
    local id="${card%%: *}"
    local name="${card#*: }"
    printf '%s\t%s' "$id" "$name"
  done
}

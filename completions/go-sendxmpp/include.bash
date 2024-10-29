_go-sendxmpp_jid_from_history() {
  command grep go-sendxmpp "$HISTFILE" | command grep -E -o '[^ ]+@[^ ]+(/[^ ]+)?' | command sort | command uniq
}

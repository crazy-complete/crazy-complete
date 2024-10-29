function _go-sendxmpp_jid_from_history
  builtin history | command grep go-sendxmpp | command grep -E -o '[^ ]+@[^ ]+(/[^ ]+)?' | command sort | command uniq
end

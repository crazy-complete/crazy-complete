function _complete_table
  switch $CAPTURED_DB
    case mysql
      printf '%s\n' users orders products
    case postgres
      printf '%s\n' customers invoices transactions
    case sqlite
      printf '%s\n' local_cache config sessions
  end
end

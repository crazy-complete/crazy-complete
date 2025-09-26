_complete_table() {
  case "${CAPTURED_DB[-1]}" in
    mysql)    printf '%s\n' users orders products;;
    postgres) printf '%s\n' customers invoices transactions;;
    sqlite)   printf '%s\n' local_cache config sessions;;
  esac
}

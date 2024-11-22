Here is the comparison of popular shell completion generators:

| Feature            | [crazy-complete](https://github.com/crazy-complete/crazy-complete) | [argcomplete](https://github.com/kislyuk/argcomplete) | [auto-auto-complete](https://codeberg.org/maandree/auto-auto-complete)[^1] | [complete-shell](https://github.com/complete-shell/complete-shell) | [completely](https://github.com/DannyBen/completely) | [complgen](https://github.com/adaszko/complgen)[^2] |
| ------------------ | -------- | -------- | -------- | ---- | ---- | ---- |
| Standalone scripts | yes      | no       | yes      | no   | yes  | yes  |
| Robust scripts     | yes      | yes      | no       | n/a  | no   | yes  |
| Extensible scripts | yes      | yes      | yes      | no   | no   | yes  |
| Bash support       | yes      | yes      | yes      | yes  | yes  | yes  |
| Fish support       | yes      | no       | yes      | no   | no   | yes  |
| Zsh support        | yes      | yes      | yes      | no   | no   | yes  |
| Dependencies       | Python 3 | Python 3 | Python 3 | Bash | Ruby | Rust |

[^1]: The domain specific language for this project is insane, have a look
at the [example](https://codeberg.org/maandree/auto-auto-complete/src/branch/master/doc/example).
[^2]: The grammar of this project is quite complicated, have a look at the [examples](https://github.com/adaszko/complgen/tree/master/examples)

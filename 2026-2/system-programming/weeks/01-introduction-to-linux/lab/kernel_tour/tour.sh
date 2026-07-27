#!/bin/sh
# W1 lab: tour of what the kernel exposes about itself in /proc and /sys.
# Read-only — safe to run anywhere (Linux only; /proc, /sys do not exist on macOS).
# Run inside the Lima VM:  sh tour.sh   (some items show more with sudo)

hr() { printf '\n=== %s ===\n' "$1"; }
show() {  # show <path> — print a file with its path, tolerate absence
	if [ -r "$1" ]; then
		printf -- '--- %s\n' "$1"
		cat "$1"
	else
		printf -- '--- %s (not readable here — try sudo, or it does not exist)\n' "$1"
	fi
}

hr "1. Which kernel am I running?"
show /proc/version
uname -r   # release string: <version>-<abi>-<flavour> on Ubuntu

hr "2. How was this kernel booted? (bootloader -> kernel command line)"
# These parameters were passed by the bootloader; init/main.c parses them
# (early_param / __setup / parse_args) before PID 1 exists.
show /proc/cmdline

hr "3. Which init became PID 1?"
ps -p 1 -o pid,comm,args 2>/dev/null || true
# comm=systemd on Ubuntu; the kernel only tried a list of paths and exec'ed it.

hr "4. Loaded modules (/proc/modules is the raw source; lsmod pretty-prints it)"
# columns: name size refcount dependents state load_address
head -5 /proc/modules 2>/dev/null || echo "(no /proc/modules?)"
echo "..."
echo "total modules loaded: $(wc -l < /proc/modules 2>/dev/null || echo '?')"

hr "5. Taint state (0 = pristine)"
show /proc/sys/kernel/tainted
t=$(cat /proc/sys/kernel/tainted 2>/dev/null || echo 0)
[ $((t & 1)) -ne 0 ]     && echo "  bit 0  (P): proprietary module was loaded"
[ $((t & 4096)) -ne 0 ]  && echo "  bit 12 (O): out-of-tree module was loaded"
[ $((t & 8192)) -ne 0 ]  && echo "  bit 13 (E): unsigned module was loaded"
[ "$t" = "0" ]           && echo "  (kernel is not tainted — no out-of-tree/proprietary/unsigned module yet)"

hr "6. printk console log levels: console_loglevel default_msg_level min_console default_console"
show /proc/sys/kernel/printk

hr "7. Per-module view under /sys/module (works for built-ins with params too)"
for m in hello_param loop; do
	d=/sys/module/$m
	if [ -d "$d" ]; then
		echo "$d:"
		ls "$d"
		[ -d "$d/parameters" ] && for p in "$d"/parameters/*; do
			printf '  %s = %s\n' "$(basename "$p")" "$(cat "$p" 2>/dev/null || echo '?')"
		done
		[ -r "$d/refcnt" ] && echo "  refcnt = $(cat "$d/refcnt")"
		[ -r "$d/taint" ] && echo "  taint  = '$(cat "$d/taint")'  (O = out-of-tree)"
	else
		echo "$d: not present (load the module first, or pick another name)"
	fi
done

hr "8. The build config this kernel was compiled with (.config snapshot)"
if [ -r "/boot/config-$(uname -r)" ]; then
	grep -E '^CONFIG_(MODULES|MODULE_SIG|PREEMPT|HZ|LOCALVERSION)[=_ ]?' \
		"/boot/config-$(uname -r)" | head -12
elif [ -r /proc/config.gz ]; then   # only if CONFIG_IKCONFIG_PROC=y
	zcat /proc/config.gz | grep -E '^CONFIG_(MODULES|PREEMPT|HZ)=' | head -12
else
	echo "(no /boot/config-* and no /proc/config.gz on this system)"
fi

hr "9. Kernel symbol table teaser (/proc/kallsyms — addresses are 0 without sudo)"
grep -w -m1 'start_kernel' /proc/kallsyms 2>/dev/null || echo "(need /proc/kallsyms)"
grep -c ' [Tt] ' /proc/kallsyms 2>/dev/null | sed 's/^/text symbols visible: /'

hr "done"
echo "Cross-reference: README sections on boot flow (/proc/cmdline, PID 1),"
echo "modules (/proc/modules, taint), and Kconfig (/boot/config-*)."

# Week 01 — Exercises (Exam Style)

All questions in English, as in the real exam. Total: 100 points. Kernel version references are Linux v6.12 unless stated otherwise.

---

**Q1. (8 pts, short answer)**
A process calls `read(fd, buf, 4096)` and the data is already in memory, so the call returns without blocking.
(a) How many mode switches occurred because of this call?
(b) How many context switches necessarily occurred?
(c) In what context (process context / interrupt context) did the kernel-side code of `read` execute, and on which stack?

<details><summary>Model answer</summary>

(a) Exactly **2** — one user→kernel transition at syscall entry, one kernel→user at return.
(b) **Zero** are necessary. A mode switch does not change the running task; the scheduler was not required to run. (A context switch *could* happen if preemption triggers, but nothing in the scenario requires one.)
(c) In **process context**, on behalf of the calling task, executing on that task's own **kernel stack** (16 KiB on x86-64). The kernel is not a separate process that "receives" the request.
</details>

---

**Q2. (8 pts, essay)**
Define the three ways control enters the kernel from outside kernel code. For each: name it, state whether it is synchronous or asynchronous with respect to the currently executing instruction stream, and give one concrete example.

<details><summary>Model answer</summary>

1. **System call** — synchronous and *voluntary*: the process deliberately executes the `syscall` instruction to request a service. Example: `write(2)`.
2. **Interrupt** — **asynchronous**: raised by hardware (a device via an IRQ line) at an arbitrary time, unrelated to the current instruction. Example: NIC signaling packet arrival, timer tick.
3. **Exception** — synchronous and *involuntary*: caused by the currently executing instruction itself. Example: page fault on access to an unmapped address, divide-by-zero.

Syscalls and exceptions run in process context (they have a "current" task to blame/serve); interrupt handlers run in interrupt context, which belongs to no task.
</details>

---

**Q3. (12 pts, calculation)**
Consider a file-read request that must traverse an FS service and a disk-driver service.
On a microkernel, each service is a separate user-space server, and sending one IPC message between address spaces costs $t_{IPC}$ **one-way**. On the monolithic kernel, the same traversal is: one syscall round trip (cost $t_{mode}$ each way) plus ordinary function calls (negligible).

(a) Write cost formulas $T_{micro}$ and $T_{mono}$ for a request that crosses app→FS→driver and back.
(b) Using Liedtke's SOSP'93 measurements on an i486-DX50 (Mach IPC ≈ 115 µs **one-way** for an 8-byte message — the paper's ping-pong methodology divides total elapsed time by 20,000, i.e. per one-way IPC; assume $2\,t_{mode} \approx 5\ \mu s$ total for the monolithic syscall round trip), compute the ratio $T_{micro}/T_{mono}$ for this request on Mach.
(c) Liedtke's own L3 kernel achieved ≈ 5.2 µs per one-way IPC. Recompute the ratio and state, in one sentence, the historical conclusion he drew from this.

<details><summary>Model answer</summary>

(a) The request needs 2 IPC round trips = **4 one-way messages** (app→FS, FS→driver, driver→FS, FS→app): $T_{micro} = 4 \cdot t_{IPC}$. Monolithic: $T_{mono} = 2\,t_{mode} + \sum t_{func} \approx 2\,t_{mode}$.
(b) $T_{micro} = 4 \times 115 = 460\ \mu s$; $T_{mono} \approx 5\ \mu s$ ⇒ ratio ≈ **92×** in favor of the monolithic design.
(c) $T_{micro} = 4 \times 5.2 = 20.8\ \mu s$ ⇒ ratio ≈ **4×**. Conclusion: the microkernel penalty was not inherent to the *architecture* but to Mach's *implementation* — IPC designed as the kernel's first-class primitive (L3/L4) recovers most of the gap, though a residual boundary-crossing cost remains.
</details>

---

**Q4. (6 pts, short answer)**
Place each system on the monolithic ↔ microkernel spectrum and justify each placement in one sentence: (a) Linux, (b) Mach 3.0, (c) macOS/XNU.

<details><summary>Model answer</summary>

(a) **Linux — modular monolithic**: all services run in one kernel address space (internal calls are function calls), but loadable modules give runtime extensibility — *without* isolation.
(b) **Mach 3.0 — true microkernel**: kernel keeps IPC/scheduling/minimal VM; OS personalities (e.g., BSD) run as user-space servers reached by message passing.
(c) **XNU — hybrid**: Mach's task/thread/port abstractions survive, but the BSD layer and IOKit drivers are co-located *inside* the kernel address space, avoiding per-service IPC cost; structurally Mach-derived, deployment-wise monolithic.
</details>

---

**Q5. (6 pts, short answer)**
For each item, name the v6.12 top-level directory where you would look first:
(a) the EEVDF scheduler; (b) `task_struct` definition; (c) the ext4 on-disk extent code; (d) the x86-64 syscall entry assembly; (e) the buddy page allocator; (f) the `checkpatch.pl` style checker.

<details><summary>Model answer</summary>

(a) `kernel/` (specifically `kernel/sched/`); (b) `include/` (`include/linux/sched.h`); (c) `fs/` (`fs/ext4/`); (d) `arch/` (`arch/x86/entry/`); (e) `mm/` (`mm/page_alloc.c`); (f) `scripts/`.
</details>

---

**Q6. (10 pts, essay)**
Explain the division of labor between **Kconfig** and **Kbuild**. Include: what a `tristate` option's three values mean; where the chosen configuration is stored; and how the single line `obj-$(CONFIG_FOO) += foo.o` implements the y/m/n decision at build time. Finally, give one technical reason (not preference) to choose `y` over `m` for a driver, and one to choose `m` over `y`.

<details><summary>Model answer</summary>

**Kconfig** decides *what goes in*: per-directory `Kconfig` files declare options (with `depends on`/`select` constraints); the user's choices are stored in the tree-root **`.config`** file (`CONFIG_FOO=y`, `=m`, or absent/`# ... is not set`). **Kbuild** decides *how it is compiled*: per-directory Makefiles list objects.

`tristate`: `y` = linked into the kernel image (built-in), `m` = built as a loadable module (`.ko`), `n` = not built at all.

`obj-$(CONFIG_FOO) += foo.o` expands to `obj-y += foo.o` (goes into the vmlinux link), `obj-m += foo.o` (built as a module), or `obj- += foo.o` (an ignored list) — the make-variable expansion itself routes the object.

Reason for `y`: the code is needed before any filesystem is available — e.g., the root-filesystem driver when booting without an initramfs; built-ins exist from boot. Reason for `m`: the code can be loaded/unloaded at runtime (development iteration without reboot, smaller boot image, hardware present on only some machines).
</details>

---

**Q7. (8 pts, essay)**
`vmlinux` and `bzImage` are both produced by an x86 kernel build. Explain what each file is, what each is used for, and why booting cannot simply use `vmlinux`. Where does the name `bzImage` come from (and what does the `bz` *not* mean)?

<details><summary>Model answer</summary>

**`vmlinux`** — the uncompressed, fully linked **ELF executable** of the kernel at the build-tree root, with symbol information; the object of debugging, `objdump`, and symbol resolution. **`bzImage`** (`arch/x86/boot/bzImage`) — the bootable artifact: real-mode setup code + a self-extracting stub + the compressed kernel payload (an objcopy-stripped vmlinux).

A bootloader cannot just jump into `vmlinux`: at boot there is no ELF loader, and the CPU/memory environment must be prepared by the setup/decompression stub first (the boot protocol expects this specific image format).

`bz` = "**big z**Image" — the image can be loaded high in memory, lifting the old zImage's size limit of roughly half a megabyte. It has nothing to do with bzip2 compression.
</details>

---

**Q8. (12 pts, essay)**
Trace what happens in the kernel after `sudo insmod mydrv.ko param=3`, from the syscall to `MODULE_STATE_LIVE`. Your answer must include, in the correct order: the syscall used; signature check; ELF/vermagic validation; the `UNFORMED`→`COMING`→`LIVE` state transitions and which processing happens between them (symbol resolution, taint marking, parameter parsing); and the exact condition under which the whole load is rolled back at the last step.

<details><summary>Model answer</summary>

1. `insmod` calls **`finit_module(fd, "param=3", 0)`** → `load_module()` (`kernel/module/main.c`).
2. **`module_sig_check()`**: unsigned module ⇒ rejected only under `CONFIG_MODULE_SIG_FORCE`; otherwise loaded with `TAINT_UNSIGNED_MODULE`.
3. **ELF validation** (`elf_validity_cache_copy`): the `.ko` is a relocatable ELF; header/section integrity is verified. Immediately after, **`check_modinfo()`** (called via `early_mod_check()`) compares the `.modinfo` **vermagic** string (target kernel version + SMP/preempt flags) against the running kernel; a mismatch is rejected with `-ENOEXEC`.
4. **`layout_and_allocate()`**: final memory layout; module enters the list as **`MODULE_STATE_UNFORMED`**. `module_augment_kernel_taints()` marks `TAINT_OOT_MODULE` (out-of-tree) and runs the license check (proprietary ⇒ `TAINT_PROPRIETARY_MODULE`).
5. **Symbol resolution + relocation** (`resolve_symbol()` per undefined symbol, honoring `gplok`); failure ⇒ "Unknown symbol", load aborted. Then **`complete_formation()`** ⇒ **`MODULE_STATE_COMING`**.
6. **`parse_args()`** parses `param=3` into the `module_param` variable — *before* init runs — and sysfs nodes appear under `/sys/module/mydrv/parameters/`.
7. **`do_init_module()`** runs `do_one_initcall(mod->init)`. **If the init function returns negative, the load is rolled back** (state → GOING, memory freed, syscall returns the error; the module never appears in `lsmod`). If it returns 0 ⇒ **`MODULE_STATE_LIVE`**, and the module's `__init` sections are freed.
</details>

---

**Q9. (8 pts, short answer)**
`module_init(my_init)` appears in a driver source file that can be built either with `CONFIG_MYDRV=y` or `=m`.
(a) What does the macro expand to in each case, and who calls `my_init` in each case?
(b) Why does `module_exit` have *no effect* in the `=y` case?

<details><summary>Model answer</summary>

(a) Built-in (`#ifndef MODULE`): `module_init(x)` → `__initcall(x)` — the function pointer is placed in an initcall section and invoked during boot by **`do_initcalls()`**. Modular (`#ifdef MODULE`): it defines **`init_module`** as an alias of `my_init`; the module loader resolves this standard symbol into `mod->init` and calls it via `do_one_initcall()` in `do_init_module()` at insertion time.
(b) A built-in can never be removed from a running kernel, so there is no unload event to run cleanup for; the exit path is only reachable for loadable modules (`rmmod` → `delete_module(2)` → `mod->exit()`).
</details>

---

**Q10. (6 pts, essay)**
A vendor ships a binary-only module with `MODULE_LICENSE("Proprietary")`. Describe every consequence enforced by v6.12 when a user loads it: the dmesg message pattern, the taint bit, the symbol-linking restriction and where it is enforced, and what happens to a *GPL* module that later uses a symbol exported by this proprietary module.

<details><summary>Model answer</summary>

- `module_license_taint_check()`: "Proprietary" is not in `license_is_gpl_compatible()`'s list ⇒ `pr_warn("...: module license 'Proprietary' taints kernel.")` and **`TAINT_PROPRIETARY_MODULE`** ('P') is set (kernel-wide and per-module). Bug reports from this kernel are effectively unsupportable upstream.
- Symbol restriction: in `resolve_symbol()` the lookup is made with `gplok = false` (because the module carries the proprietary taint), so every **`EXPORT_SYMBOL_GPL`** symbol is invisible — the load fails with "Unknown symbol" if any GPL-only symbol is referenced. Plain `EXPORT_SYMBOL` symbols remain linkable.
- Contagion: `inherit_taint()` — a module that consumes symbols exported *by* a proprietary module inherits `TAINT_PROPRIETARY_MODULE` itself (logged as "inheriting taint"); a module already using GPL-only symbols is refused such linking entirely.
</details>

---

**Q11. (10 pts, essay)**
Describe the boot sequence from `start_kernel()` to a running `systemd`, naming: the function that creates PIDs 1 and 2 and *in which order and why* (quote or paraphrase the source comment's reasoning); what the boot context itself becomes; the ordered list of binaries the kernel tries to execute as init; and what happens if none can be executed.

<details><summary>Model answer</summary>

`start_kernel()` (`init/main.c`) finishes subsystem initialization and calls **`rest_init()`**, which creates **PID 1 first** via `user_mode_thread(kernel_init, ...)` and **PID 2 second** via `kernel_thread(kthreadd, ...)`. Order rationale (source comment): init must be spawned first *so that it obtains pid 1*, but kernel_init will want to create kthreads, which would oops if kthreadd doesn't exist yet — so `kernel_init` blocks on the `kthreadd_done` completion, which `rest_init` completes after creating kthreadd. The boot context itself becomes the **idle task (PID 0, swapper)**.

`kernel_init` then tries, in order: initramfs `/init` (`ramdisk_execute_command`), the command-line `init=` value (`execute_command`), `/sbin/init`, `/etc/init`, `/bin/init`, `/bin/sh`. On success the exec'ed program (systemd on modern distros) is the ancestor of all user processes. If all fail: `panic("No working init found. ...")`. Caveat: if an *explicit* `init=` program fails to exec, the kernel panics immediately with `"Requested init %s failed (error %d)."` and never tries the later candidates; a kernel built with `CONFIG_DEFAULT_INIT` also tries that value between `init=` and `/sbin/init`.
</details>

---

**Q12. (6 pts, design)**
You are writing a kernel function that acquires three resources in order (memory allocation, a lock, a device reference) and can fail after each. Write the skeleton in idiomatic kernel style, and explain in two sentences why the kernel's coding style prefers this pattern over (a) nested `if` blocks and (b) repeating cleanup code at each failure site.

<details><summary>Model answer</summary>

```c
	buf = kmalloc(len, GFP_KERNEL);
	if (!buf)
		return -ENOMEM;
	err = mutex_lock_interruptible(&dev->lock);
	if (err)
		goto out_free;
	err = get_device_ref(dev);
	if (err)
		goto out_unlock;
	/* ... use ... */
	return 0;

out_unlock:
	mutex_unlock(&dev->lock);
out_free:
	kfree(buf);
	return err;
```

Rationale: (a) nested `if`s push the success path ever deeper and make the release order implicit in indentation, which does not scale past two resources; (b) duplicating cleanup at each failure site is the classic source of leak/double-free bugs when the function is later modified. The label ladder centralizes teardown in exact reverse acquisition order, with descriptive label names (`out_unlock`, not `err2`), per coding-style §7 "Centralized exiting of functions".
</details>

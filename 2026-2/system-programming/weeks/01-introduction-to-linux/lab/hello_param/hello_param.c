// SPDX-License-Identifier: GPL-2.0
/*
 * hello_param.c — W1 lab: module lifecycle + module_param + printk levels.
 *
 * Based on LKMPG ("The Linux Kernel Module Programming Guide",
 * https://sysprog21.github.io/lkmpg/) hello-world / command-line-argument
 * examples, updated for kernel 6.x.
 *
 * Try:
 *   sudo insmod hello_param.ko
 *   sudo insmod hello_param.ko whom=\"Linus\" howmany=3
 *   sudo insmod hello_param.ko shout=1
 *   sudo insmod hello_param.ko howmany=99        # init fails -> load fails
 *   cat /sys/module/hello_param/parameters/howmany
 */
#include <linux/init.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/moduleparam.h>
#include <linux/sched.h>	/* current */

static char *whom = "kernel world";
static int howmany = 1;
static bool shout;

/* perm != 0 => the parameter appears under /sys/module/hello_param/parameters/ */
module_param(whom, charp, 0444);
MODULE_PARM_DESC(whom, "Whom to greet");
module_param(howmany, int, 0644);	/* 0644: root can change it at runtime */
MODULE_PARM_DESC(howmany, "How many greetings (1..10)");
module_param(shout, bool, 0444);
MODULE_PARM_DESC(shout, "Greet at KERN_ALERT instead of KERN_INFO");

static int __init hello_param_init(void)
{
	int i;

	if (howmany < 1 || howmany > 10) {
		pr_err("hello_param: howmany=%d out of range [1,10]\n", howmany);
		return -EINVAL;	/* insmod fails; the module is unwound */
	}

	for (i = 0; i < howmany; i++) {
		if (shout)
			pr_alert("hello_param: (%d/%d) HELLO, %s!\n",
				 i + 1, howmany, whom);
		else
			pr_info("hello_param: (%d/%d) hello, %s\n",
				i + 1, howmany, whom);
	}

	/* Whose context are we running in? (There is no "module thread".) */
	pr_info("hello_param: init ran in the context of \"%s\" (pid %d)\n",
		current->comm, current->pid);
	return 0;
}

static void __exit hello_param_exit(void)
{
	/* If root wrote to /sys/.../howmany, the new value shows up here. */
	pr_info("hello_param: goodbye %s (howmany is now %d), unloaded by \"%s\"\n",
		whom, howmany, current->comm);
}

module_init(hello_param_init);
module_exit(hello_param_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("coursebook W1 lab");
MODULE_DESCRIPTION("W1: module_param + printk log-level demo");
MODULE_VERSION("0.1");

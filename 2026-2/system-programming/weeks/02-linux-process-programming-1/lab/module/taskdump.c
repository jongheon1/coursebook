// SPDX-License-Identifier: GPL-2.0
/*
 * taskdump.c — walk the task list with for_each_process(), exercise `current`.
 *
 * Written against Linux 6.x APIs (verified on v6.12 sources):
 *   - task state lives in p->__state (renamed from `state` in 5.14); we use
 *     the task_state_to_char() helper (static inline in <linux/sched.h>)
 *     which folds __state and exit_state into the familiar R/S/D/T/Z/I char.
 *   - for_each_process() is in <linux/sched/signal.h>; it iterates the
 *     init_task.tasks list (thread-group leaders only) and requires
 *     rcu_read_lock() because the task list is RCU-protected.
 *   - real_parent is __rcu, so it is read with rcu_dereference().
 *   - init_task is EXPORT_SYMBOL'd (init/init_task.c), so a module may use it.
 *
 * Load:  sudo insmod taskdump.ko ; sudo dmesg | tail -40
 * Unload: sudo rmmod taskdump
 */
#include <linux/init.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/sched.h>
#include <linux/sched/signal.h>	/* for_each_process, get_nr_threads */
#include <linux/sched/task.h>	/* init_task declaration */

static int __init taskdump_init(void)
{
	struct task_struct *p;
	int leaders = 0, threads = 0;

	/* `current` is whatever task is executing this code: insmod. */
	pr_info("taskdump: loaded by \"%s\" (pid %d, tgid %d)\n",
		current->comm, current->pid, current->tgid);
	pr_info("taskdump: sizeof(task_struct)=%zu, THREAD_SIZE=%lu\n",
		sizeof(struct task_struct), (unsigned long)THREAD_SIZE);

	rcu_read_lock();
	for_each_process(p) {
		struct task_struct *parent = rcu_dereference(p->real_parent);
		int nr = get_nr_threads(p);

		pr_info("taskdump: pid=%-6d tgid=%-6d state=%c %s comm=%-16s threads=%-3d parent=%s(%d)\n",
			p->pid, p->tgid,
			task_state_to_char(p),
			(p->flags & PF_KTHREAD) ? "[K]" : "   ",
			p->comm, nr, parent->comm, parent->pid);
		leaders++;
		threads += nr;
	}
	rcu_read_unlock();

	pr_info("taskdump: walked %d thread-group leaders, %d threads total\n",
		leaders, threads);
	return 0;
}

static void __exit taskdump_exit(void)
{
	pr_info("taskdump: unloaded by \"%s\" (pid %d)\n",
		current->comm, current->pid);
}

module_init(taskdump_init);
module_exit(taskdump_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("CAS3107 Week 02 lab");
MODULE_DESCRIPTION("Dump pid/tgid/state/comm/parent for every process via for_each_process()");

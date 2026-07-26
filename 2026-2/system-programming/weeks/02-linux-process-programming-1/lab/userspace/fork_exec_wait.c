/*
 * fork_exec_wait.c — process lifecycle: fork, zombie window, wait, exec.
 *
 * Linux only (uses /proc-backed ps). Run inside the lab VM (see Week 00).
 *
 * Phase 1: fork a child that exits immediately, delay the wait() on purpose,
 *          and show with ps(1) that the child sits in state Z (EXIT_ZOMBIE)
 *          until the parent reaps it.
 * Phase 2: the classic fork + exec + wait pattern.
 */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

static void run_ps(pid_t pid)
{
	char cmd[128];
	int rc;

	snprintf(cmd, sizeof(cmd), "ps -o pid,ppid,state,comm -p %d", (int)pid);
	rc = system(cmd);
	if (rc != 0)
		printf("(ps found nothing for pid %d — process fully released)\n",
		       (int)pid);
}

int main(void)
{
	pid_t zchild, xchild;
	int status;

	printf("parent: pid=%d\n", (int)getpid());

	/* ---- Phase 1: zombie observation ---- */
	zchild = fork();
	if (zchild < 0) {
		perror("fork");
		return 1;
	}
	if (zchild == 0)
		_exit(42);	/* child dies immediately; parent has not waited yet */

	sleep(1);		/* child is now EXIT_ZOMBIE: only task_struct + pid remain */
	printf("--- before wait(): expect state Z (zombie) ---\n");
	run_ps(zchild);

	if (waitpid(zchild, &status, 0) < 0) {
		perror("waitpid");
		return 1;
	}
	printf("reaped zombie %d: exit code=%d (WIFEXITED=%d)\n",
	       (int)zchild, WEXITSTATUS(status), WIFEXITED(status));

	printf("--- after wait(): the pid is gone ---\n");
	run_ps(zchild);

	/* ---- Phase 2: fork + exec + wait ---- */
	xchild = fork();
	if (xchild < 0) {
		perror("fork");
		return 1;
	}
	if (xchild == 0) {
		/* exec replaces the address space; pid/fd survive (README §8) */
		execlp("uname", "uname", "-sr", (char *)NULL);
		perror("execlp");	/* reached only if exec failed */
		_exit(127);
	}
	if (waitpid(xchild, &status, 0) < 0) {
		perror("waitpid");
		return 1;
	}
	printf("child %d ran 'uname -sr', exit status=%d\n",
	       (int)xchild, WEXITSTATUS(status));

	return 0;
}
